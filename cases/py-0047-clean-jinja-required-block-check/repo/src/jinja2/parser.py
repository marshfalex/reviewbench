# Excerpt of src/jinja2/parser.py from an upstream project; code outside the functions below is omitted.
import typing
import typing as t
from . import nodes
from .exceptions import TemplateAssertionError
from .exceptions import TemplateSyntaxError
from .lexer import describe_token
from .lexer import describe_token_expr



class Parser:
    # [... omitted ...]

    def parse_block(self) -> nodes.Block:
        node = nodes.Block(lineno=next(self.stream).lineno)
        node.name = self.stream.expect("name").value
        node.scoped = self.stream.skip_if("name:scoped")
        node.required = self.stream.skip_if("name:required")

        # common problem people encounter when switching from django
        # to jinja.  we do not support hyphens in block names, so let's
        # raise a nicer error message in that case.
        if self.stream.current.type == "sub":
            self.fail(
                "Block names in Jinja have to be valid Python identifiers and may not"
                " contain hyphens, use an underscore instead."
            )

        node.body = self.parse_statements(("name:endblock",), drop_needle=True)

        # enforce that required blocks only contain whitespace or comments
        # by asserting that the body, if not empty, is just TemplateData nodes
        # with whitespace data
        if node.required and not all(
            isinstance(child, nodes.TemplateData) and child.data.isspace()
            for body in node.body
            for child in body.nodes  # type: ignore
        ):
            self.fail("Required blocks can only contain comments or whitespace")

        self.stream.skip_if("name:" + node.name)
        return node
