import logging
import os
import re

ODOO_MODULE_RE = re.compile(r"""
    \s*                                       # some starting space
    \/(\*|\/).*\s*                            # // or /*
    @odoo-module                              # @odoo-module
    (\s+alias=(?P<alias>[\w.]+))?             # alias=web.AbstractAction (optional)
    (\s+default=(?P<default>False|false|0))?  # default=False or false or 0 (optional)
""", re.VERBOSE)


REQUIRE_RE = re.compile(r"""
    require\s*                 # require
    \(\s*                      # (
    (?P<quote>["'`])(?P<path>[^"'`]*?)(?P=quote)
    \s*\)                      # )
""", re.MULTILINE | re.VERBOSE)


ODOO_DEFINE_RE = re.compile(r"""
    odoo\s*\.\s*define\s*
    \(\s*
    (?P<quote>["'`])(?P<path>[^"'`]*?)(?P=quote)
""", re.MULTILINE | re.VERBOSE)


IMPORT_BASIC_RE = re.compile(r"""
    ^
    (?P<space>\s*)                      # space and empty line
    import\s+                           # import
    (?P<object>{(\s*\w+\s*,?\s*)+})\s*  # { a, b, c as x, ... }
    from\s*                             # from
    (?P<quote>["'`])(?P<path>[^"'`]+)(?P=quote)   # "file path" ("some/path")
""", re.MULTILINE | re.VERBOSE)


_logger = logging.getLogger(__name__)


class JSModule:
    def __init__(self, name, alias=None, default=True, dependencies=None):
        self.name = name
        self.alias = alias or None
        self.default = default
        self.dependencies = set(dependencies or [])

    @classmethod
    def from_file(cls, path, file):
        if not os.path.isfile(path):
            return None

        with open(path) as fp:
            content = fp.read()

        # Old odoo.define format
        defines = ODOO_DEFINE_RE.findall(content)
        if defines:
            if len(defines) > 1:
                _logger.warning("Multiple odoo.define in single JS %s", file)

            define = defines[0][1]
            requires = [x[1] for x in REQUIRE_RE.findall(content)]
            return cls(file, alias=define, dependencies=requires)

        # Newer odoo-module format
        module = ODOO_MODULE_RE.findall(content)
        if module:
            alias, default = module[0][2::2]
            imports = [x[-1] for x in IMPORT_BASIC_RE.findall(content)]
            return cls(file, alias=alias, default=not default, dependencies=imports)

        return None
