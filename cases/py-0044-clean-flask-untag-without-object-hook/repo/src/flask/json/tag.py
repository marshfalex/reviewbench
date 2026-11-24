# Excerpt of src/flask/json/tag.py from an upstream project; code outside the functions below is omitted.
from __future__ import annotations
import typing as t
from base64 import b64decode
from base64 import b64encode
from datetime import datetime
from uuid import UUID
from markupsafe import Markup
from werkzeug.http import http_date
from werkzeug.http import parse_date
from ..json import dumps
from ..json import loads



class TaggedJSONSerializer:
    # [... omitted ...]

    def loads(self, value: str) -> t.Any:
        """Load data from a JSON string and deserialized any tagged objects."""
        return loads(value, object_hook=self.untag)
