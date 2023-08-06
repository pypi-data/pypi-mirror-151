"""Docutils helper functions."""
import importlib
import typing as t

import docutils.nodes
import docutils.parsers.rst.directives
import docutils.parsers.rst.roles
import docutils.writers

from . import _extras


class IgnoredDirective(docutils.parsers.rst.Directive):  # pragma: no cover
    """Stub for unknown directives."""

    has_content = True

    def run(self) -> t.List:  # type: ignore[type-arg]
        """Do nothing."""
        return []


def ignore_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: docutils.parsers.rst.states.Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[t.List[str]] = None,
) -> t.Tuple[t.List, t.List]:  # type: ignore[type-arg] # pragma: no cover
    """Stub for unknown roles."""
    # pylint: disable=unused-argument,too-many-arguments
    return ([], [])


def clean_docutils_directives_and_roles_cache() -> None:  # pragma: no cover
    """Clean docutils' directives and roles cache by reloading their modules.

    Reloads:
    - docutils.parsers.rst.directives
    - docutils.parsers.rst.roles
    """
    importlib.reload(docutils.parsers.rst.directives)
    importlib.reload(docutils.parsers.rst.roles)


def ignore_directives_and_roles(directives: t.List[str], roles: t.List[str]) -> None:
    """Ignore directives and roles in docutils.

    :param directives: Directives to ignore
    :param roles: Roles to ignore
    """
    for directive in directives:
        docutils.parsers.rst.directives.register_directive(directive, IgnoredDirective)

    for role in roles:
        docutils.parsers.rst.roles.register_local_role(role, ignore_role)


class CodeBlockDirective(docutils.parsers.rst.Directive):
    """Code block directive."""

    has_content = True
    optional_arguments = 1

    def run(self) -> t.List[docutils.nodes.literal_block]:
        """Run directive.

        :return: Literal block
        """
        try:
            language = self.arguments[0]
        except IndexError:
            language = ""
        code = "\n".join(self.content)
        literal = docutils.nodes.literal_block(code, code)
        literal["classes"].append("code-block")
        literal["language"] = language
        return [literal]


def register_code_directive(
    *,
    ignore_code_directive: bool = False,
    ignore_codeblock_directive: bool = False,
    ignore_sourcecode_directive: bool = False,
) -> None:
    """Optionally register code directives.

    :param ignore_code_directive: If "code" directive should be ignored,
        so that the code block will not be checked; defaults to False
    :param ignore_codeblock_directive: If "code-block" directive should be ignored,
        so that the code block will not be checked; defaults to False
    :param ignore_sourcecode_directive: If "sourcecode" directive should be ignored,
        so that the code block will not be checked; defaults to False
    """
    if not _extras.SPHINX_INSTALLED:
        if ignore_code_directive is False:
            docutils.parsers.rst.directives.register_directive("code", CodeBlockDirective)
        # NOTE: docutils maps `code-block` and `sourcecode` to `code`
        if ignore_codeblock_directive is False:
            docutils.parsers.rst.directives.register_directive("code-block", CodeBlockDirective)
        if ignore_sourcecode_directive is False:
            docutils.parsers.rst.directives.register_directive("sourcecode", CodeBlockDirective)
