# Excerpt of src/attr/_make.py from an upstream project; code outside the functions below is omitted.
import contextlib
import copy
import enum
import functools
import inspect
import itertools
import linecache
import sys
import types
import typing
from operator import itemgetter
from . import _compat, _config, setters
from ._compat import (
    PY_3_8_PLUS,
    PY_3_10_PLUS,
    _AnnotationExtractor,
    get_generic_base,
)
from .exceptions import (
    DefaultAlreadySetError,
    FrozenInstanceError,
    NotAnAttrsClassError,
    UnannotatedAttributeError,
)



def _is_slot_cls(cls):
    return "__slots__" in cls.__dict__


def _is_slot_attr(a_name, base_attr_map):
    """
    Check if the attribute name comes from a slot class.
    """
    return a_name in base_attr_map and _is_slot_cls(base_attr_map[a_name])
