"""Rstcheck configuration functionality."""
import configparser
import contextlib
import enum
import pathlib
import re
import typing as t

import pydantic

from . import _extras


if _extras.TOMLI_INSTALLED:  # pragma: no cover
    import tomli


CONFIG_FILES = [".rstcheck.cfg", "setup.cfg"]
if _extras.TOMLI_INSTALLED:  # pragma: no cover
    CONFIG_FILES = [".rstcheck.cfg", "pyproject.toml", "setup.cfg"]


class ReportLevel(enum.Enum):
    """Report levels supported by docutils."""

    INFO = 1
    WARNING = 2
    ERROR = 3
    SEVERE = 4
    NONE = 5


ReportLevelMap = {
    "info": 1,
    "warning": 2,
    "error": 3,
    "severe": 4,
    "none": 5,
}
"""Map docutils report levels in text form to numbers."""


DEFAULT_REPORT_LEVEL = ReportLevel.INFO


class RstcheckConfigFile(pydantic.BaseModel):  # pylint: disable=no-member
    """Rstcheck config file.

    :raises ValueError:: If setting has incorrect value or type
    :raises pydantic.error_wrappers.ValidationError:: If setting is not parsable into correct type
    """

    report_level: t.Optional[ReportLevel]
    ignore_directives: t.Optional[t.List[str]]
    ignore_roles: t.Optional[t.List[str]]
    ignore_substitutions: t.Optional[t.List[str]]
    ignore_languages: t.Optional[t.List[str]]
    # NOTE: Pattern type-arg errors pydanic: https://github.com/samuelcolvin/pydantic/issues/2636
    ignore_messages: t.Optional[t.Pattern]  # type: ignore[type-arg]

    @pydantic.validator("report_level", pre=True)
    @classmethod
    def valid_report_level(cls, value: t.Any) -> t.Optional[ReportLevel]:  # noqa: ANN401
        """Validate the report_level setting.

        :param value: Value to validate
        :raises ValueError: If ``Value`` is not a valid docutils report level
        :return: Instance of ``ReportLevel`` or None if emptry string.
        """
        if value is None:
            return None

        if isinstance(value, ReportLevel):
            return value

        if value == "":
            return DEFAULT_REPORT_LEVEL

        if isinstance(value, bool):
            raise ValueError("Invalid report level")

        if isinstance(value, str):
            if value.casefold() in set(ReportLevelMap):
                return ReportLevel(ReportLevelMap[value.casefold()])

            with contextlib.suppress(ValueError):
                value = int(value)

        if isinstance(value, int) and 1 <= value <= 5:
            return ReportLevel(value)

        raise ValueError("Invalid report level")

    @pydantic.validator(
        "ignore_directives", "ignore_roles", "ignore_substitutions", "ignore_languages", pre=True
    )
    @classmethod
    def split_str(cls, value: t.Any) -> t.Optional[t.List[str]]:  # noqa: ANN401
        """Validate and parse the following ignore_* settings.

        - ignore_directives
        - ignore_roles
        - ignore_substitutions
        - ignore_languages

        Comma separated strings are split into a list.

        :param value: Value to validate
        :raises ValueError: If not a ``str`` or ``List[str]``
        :return: List of things to ignore in the respective category
        """
        if value is None:
            return None

        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]

        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return [v.strip() for v in value if v.strip()]

        raise ValueError("Not a string or list of strings")

    @pydantic.validator("ignore_messages", pre=True)
    @classmethod
    def join_regex_str(
        cls, value: t.Any  # noqa: ANN401
    ) -> t.Optional[t.Union[str, t.Pattern[str]]]:
        """Validate and concatenate the ignore_messages setting to a RegEx string.

        If a list ist given, the entries are concatenated with "|" to create an or RegEx.

        :param value: Value to validate
        :raises ValueError: If not a ``str`` or ``List[str]``
        :return: A RegEx string with messages to ignore or Pattern if it is one already
        """
        if value is None:
            return None

        if isinstance(value, re.Pattern):
            return value

        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return r"|".join(value)

        if isinstance(value, str):
            return value

        raise ValueError("Not a string or list of strings")


class RstcheckConfig(RstcheckConfigFile):  # pylint: disable=too-few-public-methods
    """Rstcheck config.

    :raises ValueError:: If setting has incorrect value or type
    :raises pydantic.error_wrappers.ValidationError:: If setting is not parsable into correct type
    """

    config_path: t.Optional[pathlib.Path]
    recursive: t.Optional[bool]


class _RstcheckConfigINIFile(
    pydantic.BaseModel  # pylint: disable=no-member
):  # pylint: disable=too-few-public-methods
    """Type for [rstcheck] section in INI file.

    The types apply to the file's data before the parsing by ``RstcheckConfig`` is done.

    :raises pydantic.error_wrappers.ValidationError:: If setting is not parsable into correct type
    """

    report_level: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member
    ignore_directives: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member
    ignore_roles: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member
    ignore_substitutions: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member
    ignore_languages: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member
    ignore_messages: pydantic.NoneStr = pydantic.Field(None)  # pylint: disable=no-member


def _load_config_from_ini_file(ini_file: pathlib.Path) -> t.Optional[RstcheckConfigFile]:
    """Load, parse and validate rstcheck config from a ini file.

    :param ini_file: INI file to load config from
    :raises FileNotFoundError: If the file is not found
    :return: instance of ``RstcheckConfigFile`` or ``None`` on missing config section
    """
    resolved_file = ini_file.resolve()

    if not resolved_file.is_file():
        raise FileNotFoundError(f"{resolved_file}")

    parser = configparser.ConfigParser()
    parser.read(resolved_file)

    if not parser.has_section("rstcheck"):
        return None

    config_values_raw = dict(parser.items("rstcheck"))
    config_values_checked = _RstcheckConfigINIFile(**config_values_raw)
    config_values_parsed = RstcheckConfigFile(**config_values_checked.dict())

    return config_values_parsed


class _RstcheckConfigTOMLFile(
    pydantic.BaseModel  # pylint: disable=no-member,
):  # pylint: disable=too-few-public-methods
    """Type for [tool.rstcheck] section in TOML file.

    The types apply to the file's data before the parsing by ``RstcheckConfig`` is done.

    :raises pydantic.error_wrappers.ValidationError:: If setting is not parsable into correct type
    """

    report_level: t.Optional[str] = pydantic.Field(None)
    ignore_directives: t.Optional[t.List[str]] = pydantic.Field(None)
    ignore_roles: t.Optional[t.List[str]] = pydantic.Field(None)
    ignore_substitutions: t.Optional[t.List[str]] = pydantic.Field(None)
    ignore_languages: t.Optional[t.List[str]] = pydantic.Field(None)
    ignore_messages: t.Optional[t.Union[str, t.List[str]]] = pydantic.Field(None)


def _load_config_from_toml_file(toml_file: pathlib.Path) -> t.Optional[RstcheckConfigFile]:
    """Load, parse and validate rstcheck config from a TOML file.

    .. warning::

        Needs tomli installed!
        Use toml extra.

    :param toml_file: TOML file to load config from
    :raises ValueError: If the file is not a TOML file
    :raises FileNotFoundError: If the file is not found
    :return: instance of ``RstcheckConfigFile`` or ``None`` on missing config section
    """
    _extras.install_guard("tomli")

    resolved_file = toml_file.resolve()

    if resolved_file.suffix.casefold() != ".toml":
        raise ValueError("File is not a TOML file")

    if not resolved_file.is_file():
        raise FileNotFoundError(f"{resolved_file}")

    with open(resolved_file, "rb") as toml_file_handle:
        toml_dict = tomli.load(toml_file_handle)

    optional_rstcheck_section = t.Optional[t.Dict[str, t.Any]]
    rstcheck_section: optional_rstcheck_section = toml_dict.get("tool", {}).get("rstcheck")

    if rstcheck_section is None:
        return None

    config_values_checked = _RstcheckConfigTOMLFile(**rstcheck_section)
    config_values_parsed = RstcheckConfigFile(**config_values_checked.dict())

    return config_values_parsed


def load_config_file(file_path: pathlib.Path) -> t.Optional[RstcheckConfigFile]:
    """Load, parse and validate rstcheck config from a file.

    .. caution::

        If a TOML file is passed this function need tomli installed!
        Use toml extra or install manally.

    :param file_path: File to load config from
    :raises FileNotFoundError: If the file is not found
    :return: instance of ``RstcheckConfigFile`` or ``None`` on missing config section
    """
    if file_path.suffix.casefold() == ".toml":
        return _load_config_from_toml_file(file_path)
    return _load_config_from_ini_file(file_path)


def load_config_file_from_dir(dir_path: pathlib.Path) -> t.Optional[RstcheckConfigFile]:
    """Search, load, parse and validate rstcheck config from a directory.

    Searches files from ``CONFIG_FILES`` in the directory. If a file is found, try to load the
    config from it. If is has no config, search further.

    :param dir_path: Directory to search
    :return: instance of ``RstcheckConfigFile`` or
        ``None`` if no file is found or no file has a rstcheck section
    """
    config = None

    for file_name in CONFIG_FILES:
        file_path = (dir_path / file_name).resolve()
        if file_path.is_file():
            config = load_config_file(file_path)
            if config is not None:
                break

    return config


def load_config_file_from_dir_tree(dir_path: pathlib.Path) -> t.Optional[RstcheckConfigFile]:
    """Search, load, parse and validate rstcheck config from a directory tree.

    Searches files from ``CONFIG_FILES`` in the directory. If a file is found, try to load the
    config from it. If is has no config, search further. If no config is found in the directory
    search its parents one by one.

    :param dir_path: Directory to search
    :return: instance of ``RstcheckConfigFile`` or
        ``None`` if no file is found or no file has a rstcheck section
    """
    config = None

    search_dir = dir_path.resolve()

    while True:
        config = load_config_file_from_dir(search_dir)

        if config is not None:
            break

        parent_dir = search_dir.parent.resolve()
        if parent_dir == search_dir:
            break
        search_dir = parent_dir

    return config


def load_config_file_from_path(
    path: pathlib.Path, *, search_dir_tree: bool = False
) -> t.Optional[RstcheckConfigFile]:
    """Analyse the path and call the correct config file loader.

    :param path: Path to load config file from; can be a file or directory
    :param search_dir_tree: If the directory tree should be searched;
        only applies if ``path`` is a directory;
        defaults to False
    :return: instance of ``RstcheckConfigFile`` or
        ``None`` if no file is found or no file has a rstcheck section
    """
    resolved_path = path.resolve()

    if resolved_path.is_file():
        return load_config_file(resolved_path)

    if resolved_path.is_dir():
        if search_dir_tree:
            return load_config_file_from_dir_tree(resolved_path)
        return load_config_file_from_dir(resolved_path)

    return None


def merge_configs(
    config_base: RstcheckConfig,
    config_add: t.Union[RstcheckConfig, RstcheckConfigFile],
    *,
    config_add_is_dominant: bool = True,
) -> RstcheckConfig:
    """Merge two configs into a new one.

    :param config_base: The base config to merge into
    :param config_add: The config that is merged into the ``config_base``
    :param config_add_is_dominant: If the ``config_add`` overwrites values of ``config_base``;
        defaults to True
    :return: New merged config
    """
    sub_config: t.Union[RstcheckConfig, RstcheckConfigFile] = config_base
    sub_config_dict = sub_config.dict()
    for setting in dict(sub_config_dict):
        if sub_config_dict[setting] is None:
            del sub_config_dict[setting]

    dom_config: t.Union[RstcheckConfig, RstcheckConfigFile] = config_add
    dom_config_dict = dom_config.dict()
    for setting in dict(dom_config_dict):
        if dom_config_dict[setting] is None:
            del dom_config_dict[setting]

    if config_add_is_dominant is False:
        sub_config_dict, dom_config_dict = dom_config_dict, sub_config_dict

    merged_config_dict = {**sub_config_dict, **dom_config_dict}

    return RstcheckConfig(**merged_config_dict)
