# Excerpt of pydantic/json_schema.py from an upstream project; code outside the functions below is omitted.
from __future__ import annotations as _annotations
import dataclasses
import inspect
import math
import re
import warnings
from collections import defaultdict
from copy import deepcopy
from dataclasses import is_dataclass
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Counter,
    Dict,
    Hashable,
    Iterable,
    NewType,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)
import pydantic_core
from pydantic_core import CoreSchema, PydanticOmit, core_schema, to_jsonable_python
from pydantic_core.core_schema import ComputedField
from typing_extensions import Annotated, Literal, TypeAlias, assert_never, deprecated, final
from pydantic.warnings import PydanticDeprecatedSince26
from ._internal import (
    _config,
    _core_metadata,
    _core_utils,
    _decorators,
    _internal_dataclass,
    _mock_val_ser,
    _schema_generation_shared,
    _typing_extra,
)
from .annotated_handlers import GetJsonSchemaHandler
from .config import JsonDict, JsonSchemaExtraCallable, JsonValue
from .errors import PydanticInvalidForJsonSchema, PydanticUserError



def model_json_schema(
    cls: type[BaseModel] | type[PydanticDataclass],
    by_alias: bool = True,
    ref_template: str = DEFAULT_REF_TEMPLATE,
    schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
    mode: JsonSchemaMode = 'validation',
) -> dict[str, Any]:
    """Utility function to generate a JSON Schema for a model.

    Args:
        cls: The model class to generate a JSON Schema for.
        by_alias: If `True` (the default), fields will be serialized according to their alias.
            If `False`, fields will be serialized according to their attribute name.
        ref_template: The template to use for generating JSON Schema references.
        schema_generator: The class to use for generating the JSON Schema.
        mode: The mode to use for generating the JSON Schema. It can be one of the following:

            - 'validation': Generate a JSON Schema for validating data.
            - 'serialization': Generate a JSON Schema for serializing data.

    Returns:
        The generated JSON Schema.
    """
    schema_generator_instance = schema_generator(by_alias=by_alias, ref_template=ref_template)
    if isinstance(cls.__pydantic_validator__, _mock_val_ser.MockValSer):
        cls.__pydantic_validator__.rebuild()
    assert '__pydantic_core_schema__' in cls.__dict__, 'this is a bug! please report it'
    return schema_generator_instance.generate(cls.__pydantic_core_schema__, mode=mode)
