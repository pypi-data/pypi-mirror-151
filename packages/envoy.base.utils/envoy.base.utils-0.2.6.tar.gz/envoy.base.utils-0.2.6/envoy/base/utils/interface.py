
import pathlib
from typing import (
    AsyncGenerator, ItemsView, Iterator, KeysView, List,
    Optional, Set, Tuple, Type, Union, ValuesView)

import aiohttp
from packaging import version as _version

import abstracts

from aio.api import github as _github

from envoy.base.utils import typing


class IInventories(metaclass=abstracts.Interface):
    """Manage Sphinx project documentation inventories."""

    def __init__(self, project: "IProject") -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[_version.Version]:
        raise NotImplementedError

    def __getitem__(self, k: _version.Version) -> pathlib.Path:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def inventories(self) -> typing.InventoryDict:
        """Mapping of `version` -> `path` for inventory files."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def paths(self) -> Iterator[pathlib.Path]:
        """Inventory file paths."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def versions(self) -> typing.VersionDict:
        """Mapping of `minor_version` -> `version` for inventories."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def versions_path(self) -> pathlib.Path:
        """Path to the inventory versions file."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def changes_for_commit(self, change: typing.ProjectChangeDict) -> Set[str]:
        """Changes to add/commit for a given change dictionary."""
        raise NotImplementedError

    @abstracts.interfacemethod
    async def sync(self) -> typing.SyncResultDict:
        """Synchronize the latest available inventories."""
        raise NotImplementedError


class IChangelogEntry(metaclass=abstracts.Interface):
    """A changelog entry."""

    def __init__(self, section: str, entry: typing.ChangeDict) -> None:
        raise NotImplementedError

    @abstracts.interfacemethod
    def __gt__(self, other: "IChangelogEntry") -> bool:
        raise NotImplementedError

    @abstracts.interfacemethod
    def __lt__(self, other: "IChangelogEntry") -> bool:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def area(self) -> str:
        """Tag/area for this entry."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def change(self) -> str:
        """Description of the change for this entry."""
        raise NotImplementedError


class IChangelog(metaclass=abstracts.Interface):
    """A changelog."""

    def __init__(self, version: _version.Version, path: pathlib.Path) -> None:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def data(self) -> typing.ChangelogDict:
        """Changes grouped by change type."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def entry_class(self) -> Type[IChangelogEntry]:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def path(self) -> pathlib.Path:
        """Path to this changelog."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def release_date(self) -> str:
        """Datestamp of this changelog."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def version(self) -> str:
        """Version of this changelog."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def entries(self, section: str) -> List[IChangelogEntry]:
        """Changelog entries."""
        raise NotImplementedError


class IChangelogs(metaclass=abstracts.Interface):
    """Manage project changelogs."""

    def __init__(self, project: "IProject") -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[_version.Version]:
        raise NotImplementedError

    def __getitem__(self, k: _version.Version) -> IChangelog:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def changelog_class(self) -> Type[IChangelog]:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def changelog_paths(self) -> typing.ChangelogPathsDict:
        """Mapping of changelog versions to changelog file paths."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def changelogs(self) -> typing.ChangelogsDict:
        """Ordered mapping of changelog versions to changelog objects."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def current(self) -> _version.Version:
        """The current (most recent or active) changelog."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def date_format(self) -> str:
        """Changelog date format."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def datestamp(self) -> str:
        """Formatted current UTC date."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def is_pending(self) -> bool:
        """Flag indicating whether the current changelog is set to
        `Pending`."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def sections(self) -> typing.ChangelogSectionsDict:
        """Changelog groupings/sections."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def changes_for_commit(self, change: typing.ProjectChangeDict) -> Set[str]:
        """Changes to add/commit for a given change dictionary."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def items(self) -> ItemsView[_version.Version, IChangelog]:
        raise NotImplementedError

    @abstracts.interfacemethod
    def keys(self) -> KeysView[_version.Version]:
        raise NotImplementedError

    @abstracts.interfacemethod
    async def sync(self) -> None:
        """Synchronize the latest available changelogs."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def values(self) -> ValuesView[IChangelog]:
        raise NotImplementedError

    @abstracts.interfacemethod
    def write_current(self) -> None:
        """Create the `current.yaml` changelog file from a template."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def write_date(self) -> None:
        """Set the date in the `current.yaml` changelog file."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def write_version(self, version: _version.Version) -> None:
        """Write the `current.yaml` file to the current version."""
        raise NotImplementedError


class IProject(metaclass=abstracts.Interface):

    def __init__(
            self,
            path: Union[pathlib.Path, str] = ".",
            version: Optional[_version.Version] = None,
            github: Optional[_github.IGithubAPI] = None,
            repo: Optional[_github.IGithubRepo] = None,
            github_token: Optional[str] = None,
            session: Optional[aiohttp.ClientSession] = None) -> None:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def archived_versions(self) -> Tuple[_version.Version, ...]:
        """Non/archived version logic."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def changelogs(self) -> IChangelogs:
        """Project changelogs."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def changelogs_class(self) -> Type[IChangelogs]:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def dev_version(self) -> Optional[_version.Version]:
        """Returns the current version iff its a dev version."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def inventories(self) -> IInventories:
        """Project inventories."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def inventories_class(self) -> Type[IInventories]:
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def is_dev(self) -> bool:
        """Flag indicating whether the project is in "dev" mode."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def is_main_dev(self) -> bool:
        """If the patch version is `0` and its a dev branch then we are on
        `main`"""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def minor_version(self) -> _version.Version:
        """Minor version for the current version."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def minor_versions(self) -> typing.MinorVersionsDict:
        """Ordered mapping `minor_version` -> `patch_versions` for the
        project."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def path(self) -> pathlib.Path:
        """Path to the project root."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def rel_version_path(self) -> pathlib.Path:
        """Path to the project version file."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def repo(self) -> _github.IGithubRepo:
        """Project github repo."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def session(self) -> aiohttp.ClientSession:
        """HTTP client session used for retrieving project data."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def stable_versions(self) -> Tuple[_version.Version, ...]:
        """Currently supported stable versions."""
        raise NotImplementedError

    @property  # type:ignore
    @abstracts.interfacemethod
    def version(self) -> _version.Version:
        """Current project version."""
        raise NotImplementedError

    @abstracts.interfacemethod
    async def commit(
            self,
            change: typing.ProjectChangeDict,
            msg: str) -> AsyncGenerator:
        """Commit a set of changes."""
        raise NotImplementedError

    @abstracts.interfacemethod
    async def dev(self) -> typing.ProjectDevResultDict:
        """Switch the project to "dev" mode."""
        raise NotImplementedError

    @abstracts.interfacemethod
    def is_current(self, version: _version.Version) -> bool:
        """Check if a version is the current one."""
        raise NotImplementedError

    @abstracts.interfacemethod
    async def release(self) -> typing.ProjectReleaseResultDict:
        """Switch the project to "release" mode."""
        raise NotImplementedError

    @abstracts.interfacemethod
    async def sync(self) -> typing.ProjectSyncResultDict:
        """Synchronize project resources."""
        raise NotImplementedError
