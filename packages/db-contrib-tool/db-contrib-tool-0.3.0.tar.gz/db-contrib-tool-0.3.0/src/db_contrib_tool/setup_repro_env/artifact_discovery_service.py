"""A service for finding artifacts."""
import re
from enum import Enum
from typing import Dict, NamedTuple, Optional

import inject
import structlog
from evergreen import Version

from db_contrib_tool.config import (
    SETUP_REPRO_ENV_CONFIG_FILE,
    DownloadTarget,
    SetupReproEnvConfig,
)
from db_contrib_tool.services.evergreen_service import EvergreenService
from db_contrib_tool.services.git_service import GitService
from db_contrib_tool.services.platform_service import PlatformService

LOGGER = structlog.get_logger(__name__)
BRANCH_FALLBACK = "master"
NON_VERSION_PROJECTS = {"mongodb-mongo-master", "mongodb-mongo-master-nightly"}
PROJECT_PREFIX = "mongodb-mongo-"
VERSION_PROJECT_RE = re.compile(r"mongodb-mongo-v(\d+\.\d+)")


class MissingBuildVariantError(Exception):
    """An error representing missing build variants."""

    pass


class EvgURLInfo(NamedTuple):
    """Wrapper around compile URLs with metadata."""

    urls: Dict[str, str]
    evg_version_id: str
    project_identifier: str


class RequestType(Enum):
    """
    How the mongo binaries are being requested.

    * git_commit: Get binaries from a specific commit.
    * git_branch: Get binaries from a specific git branch.
    * evg_version: Get binaries from a specific evergreen version.
    * evg_task: Get binaries from a specific evergreen task.
    * mongo_version: Get binaries for a release version of mongo (e.g. 4.4, 5.0, etc).
    """

    GIT_COMMIT = "git_commit"
    GIT_BRANCH = "git_branch"
    EVG_VERSION = "evg_version"
    EVG_TASK = "evg_task"
    MONGO_VERSION = "mongo_version"

    def __str__(self) -> str:
        """Display item as a string."""
        return self.value


class RequestTarget(NamedTuple):
    """
    Version of mongo binaries that was requested.

    * request_type: Type of the identifier.
    * identifier: Identifier used to find request.
    """

    request_type: RequestType
    identifier: str

    def __str__(self) -> str:
        """Display item as a string."""
        return f"{self.request_type}({self.identifier})"


class ArtifactDiscoveryService:
    """A service for finding artifacts."""

    @inject.autoparams()
    def __init__(
        self,
        evg_service: EvergreenService,
        platform_service: PlatformService,
        setup_repro_config: SetupReproEnvConfig,
        git_service: GitService,
    ) -> None:
        """
        Initialize the service.

        :param evg_service: Service for interacting with evergreen.
        :param platform_service: Service for discovering platform information.
        :param setup_repro_config: Configuration for setuping up a repro environment.
        :param git_service: Service for performing git workflows.
        """
        self.evg_service = evg_service
        self.platform_service = platform_service
        self.setup_repro_config = setup_repro_config
        self.git_service = git_service

    def find_artifacts(
        self,
        request: RequestTarget,
        requested_variant: Optional[str],
        target: DownloadTarget,
        ignore_failed_push: bool,
        starting_commit: Optional[str] = None,
    ) -> Optional[EvgURLInfo]:
        """
        Find the artifacts generated for the given request.

        :param request: Request of mongo instance to find.
        :param requested_variant: Name of build variant that was requested.
        :param target: Attributes of the build variant to download from.
        :param ignore_failed_push: Whether a failed push should raise an exception.
        :param starting_commit: When scanning multiple commits, start scanning after this commit.
        :return: Links to found artifacts.
        """
        urls_info = None
        if request.request_type == RequestType.EVG_VERSION:
            urls_info = self.find_artifact_urls_for_version(
                request.identifier, requested_variant, target, ignore_failed_push
            )

        elif request.request_type == RequestType.EVG_TASK:
            task = self.evg_service.get_task(request.identifier)
            if requested_variant is None:
                requested_variant = task.build_variant
            urls_info = self.find_artifact_urls_for_version(
                task.version_id, requested_variant, target, ignore_failed_push
            )

        elif request.request_type == RequestType.GIT_BRANCH:
            mongo_project = f"{PROJECT_PREFIX}{request.identifier}"
            try:
                urls_info = self.scan_for_artifact_urls(
                    mongo_project, requested_variant, target, ignore_failed_push, starting_commit
                )
            except MissingBuildVariantError:
                if mongo_project in NON_VERSION_PROJECTS:
                    other_project = list(NON_VERSION_PROJECTS.difference(mongo_project))[0]
                    LOGGER.info(
                        "Could not find expected build variant trying other project",
                        other_project=other_project,
                    )
                    urls_info = self.scan_for_artifact_urls(
                        other_project,
                        requested_variant,
                        target,
                        ignore_failed_push,
                        starting_commit,
                    )
                else:
                    raise

        elif request.request_type == RequestType.MONGO_VERSION:
            mongo_project = f"{PROJECT_PREFIX}v{request.identifier}"
            urls_info = self.scan_for_artifact_urls(
                mongo_project, requested_variant, target, ignore_failed_push
            )
            if urls_info is None:
                # This may be a new branch that hasn't had any artifacts built yet, so for that
                # case, we will fallback to searching the master branch for usable artifacts.
                self.handle_new_branch_fallback(
                    request.identifier, requested_variant, target, ignore_failed_push
                )

        elif request.request_type == RequestType.GIT_COMMIT:
            version_id = self.find_version_id_for_commit(request.identifier)
            if version_id is not None:
                urls_info = self.find_artifact_urls_for_version(
                    version_id, requested_variant, target, ignore_failed_push
                )
            else:
                raise ValueError(
                    f"Unable to find commit '{request.identifier}' in any evergreen projects"
                )

        else:
            raise ValueError(f"Unknown RequestType: '{request.request_type}'")

        return urls_info

    def handle_new_branch_fallback(
        self,
        mongo_version: str,
        requested_variant: Optional[str],
        target: DownloadTarget,
        ignore_failed_push: bool,
    ) -> Optional[EvgURLInfo]:
        """
        Handle the case a new branch does not have any built artifacts.

        In the case we are looking for artifacts on a new branch that has yet to build any
        artifacts, we will fallback to the master branch and look for the latest artifacts
        built before the branch split off.

        :param mongo_version: Version of mongo to target.
        :param requested_variant: Name of build variant that was requested.
        :param target: Attributes of the build variant to download from.
        :param ignore_failed_push: Whether a failed push should raise an exception.
        :return: Artifact URLs to use for new branch.
        """
        merge_base = self.git_service.get_merge_base_commit(mongo_version)
        if merge_base is None:
            LOGGER.warning("Unable to find merge-base commit", mongo_version=mongo_version)
            return None

        request = RequestTarget(request_type=RequestType.GIT_BRANCH, identifier=BRANCH_FALLBACK)
        return self.find_artifacts(
            request, requested_variant, target, ignore_failed_push, starting_commit=merge_base
        )

    def find_artifact_urls_for_version(
        self,
        version_id: str,
        buildvariant_name: Optional[str],
        target: DownloadTarget,
        ignore_failed_push: bool,
    ) -> Optional[EvgURLInfo]:
        """
        Find URLs for downloading artifacts from the given evergreen version.

        :param version_id: Version ID of evergreen version to target.
        :param buildvariant_name: Name of build variant to download from.
        :param target: Details about what platform/edition/architecture to target.
        :param ignore_failed_push: Can a failed push task be ignored.
        :return: Collection of URLs to download artifacts.
        """
        evg_version = self.evg_service.get_version(version_id)
        if evg_version is None:
            return None

        if not buildvariant_name:
            buildvariant_name = self.infer_build_variant(evg_version, target)
            if buildvariant_name is None:
                raise ValueError(f"Unable to find matching build variant for '{version_id}'.")

        if buildvariant_name not in evg_version.build_variants_map:
            raise MissingBuildVariantError(
                f"Buildvariant '{buildvariant_name}' not found in evergreen. "
                f"Available buildvariants can be found in {SETUP_REPRO_ENV_CONFIG_FILE}."
            )

        urls = self.evg_service.get_compile_artifact_urls(
            evg_version, buildvariant_name, ignore_failed_push=ignore_failed_push
        )

        if urls is not None:
            return EvgURLInfo(
                urls=urls.urls,
                evg_version_id=evg_version.version_id,
                project_identifier=evg_version.project_identifier,
            )
        return None

    def scan_for_artifact_urls(
        self,
        mongo_project: str,
        requested_variant: Optional[str],
        target: DownloadTarget,
        ignore_failed_push: bool,
        starting_commit: Optional[str] = None,
    ) -> Optional[EvgURLInfo]:
        """
        Scan through evergreen version to find the most recent artifacts to download.

        :param mongo_project: Name of mongo project in evergreen.
        :param buildvariant_name: Name of build variant to download from.
        :param target: Details about what platform/edition/architecture to target.
        :param ignore_failed_push: Can a failed push task be ignored.
        :param starting_commit: Only match versions previous to this commit.
        :return: URLs for artifacts in most recent version found.
        """
        found_starting_commit = False
        for evg_version in self.evg_service.get_version_iterator(mongo_project):
            # If a starting commit was provided, only search after that commit.
            if starting_commit is not None and found_starting_commit is False:
                if evg_version.revision != starting_commit:
                    continue
                found_starting_commit = True

            # Skip all versions until we get the revision we should start looking from
            urls = self.find_artifact_urls_for_version(
                evg_version.version_id,
                requested_variant,
                target,
                ignore_failed_push=ignore_failed_push,
            )
            if urls is not None:
                return urls

            LOGGER.debug("Unable to find URLs for version", version=evg_version.version_id)

        return None

    def infer_build_variant(self, evg_version: Version, target: DownloadTarget) -> Optional[str]:
        """
        Determine what build variant to target.

        :param evg_version: Evergreen version to download from.
        :param target: Details of what download to target.
        :return: Name of build variant to download from.
        """
        evg_project = evg_version.project_identifier
        LOGGER.debug("Found evergreen project", evergreen_project=evg_project)

        version = self.project_to_version(evg_project)
        if version is None:
            raise ValueError(f"Unable to determine version of project: '{evg_project}'")

        if not target.is_complete():
            target = self.get_download_target(version, target)

        LOGGER.debug("Searching for build variant", version=version, target=target)
        buildvariant_name = self.setup_repro_config.find_matching_build_variant(target, version)
        LOGGER.debug("Found buildvariant", buildvariant_name=buildvariant_name)
        return buildvariant_name

    def get_download_target(self, mongo_version: str, target: DownloadTarget) -> DownloadTarget:
        """
        Determine the download target that should be used.

        This will infer the platform if it is not specified.

        :param mongo_version: Mongo version being targetted.
        :param target: Download target to use as a base.
        :return: Download target to use.
        """
        target_platform = target.platform
        if target_platform is None:
            target_platform = self.platform_service.infer_platform(target.edition, mongo_version)

        return DownloadTarget(
            edition=target.edition, platform=target_platform, architecture=target.architecture
        )

    @staticmethod
    def project_to_version(project_identifier: str) -> Optional[str]:
        """
        Determine the given version based on the given project identifier.

        :param project_identifier: Project identifier to use.
        :return: Version of given project identifier.
        """
        if project_identifier in NON_VERSION_PROJECTS:
            return project_identifier.replace(PROJECT_PREFIX, "")

        version_match = VERSION_PROJECT_RE.match(project_identifier)
        if version_match is not None:
            return version_match.group(1)

        return None

    def find_version_id_for_commit(self, commit_hash: str) -> Optional[str]:
        """
        Given a commit hash, find the evergreen version that is associated with it.

        :param commit_hash: Git commit hash to search for.
        :return: Evergreen version id associated with the given git commit hash.
        """
        LOGGER.debug("Search evergreen projects for commit", commit_hash=commit_hash)
        evergreen_projects = self.evg_service.get_mongo_projects()
        for project in evergreen_projects:
            possible_version_id = f"{project}_{commit_hash}".replace("-", "_")
            LOGGER.debug(
                "Checking project for commit",
                project=project,
                possible_version_id=possible_version_id,
            )
            if self.evg_service.query_version_existence(possible_version_id):
                return possible_version_id

        return None
