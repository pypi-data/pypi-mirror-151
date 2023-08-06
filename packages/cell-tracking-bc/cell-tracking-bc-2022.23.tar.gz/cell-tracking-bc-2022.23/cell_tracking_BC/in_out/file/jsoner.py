# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import json
from enum import Enum as enum_t
from pathlib import Path as path_t
from typing import Any, Callable, Dict, Optional, Tuple, Union

try:
    import networkx as grph
except ModuleNotFoundError:
    grph = None
try:
    import numpy as nmpy
except ModuleNotFoundError:
    nmpy = None

from cell_tracking_BC.in_out.text.logger import LOGGER


builders_h = Dict[str, Callable[[Union[str, dict]], Any]]
description_h = Tuple[str, Any]
# /!\ When a module is not found, using bytes, the first type tested while JSONing, as the main module type is a safe
# way to "disable" it.
if grph is None:
    graph_t = bytes
else:
    graph_t = grph.Graph
if nmpy is None:
    array_t = bytes
else:
    array_t = nmpy.ndarray
object_h = Union[bytes, slice, str, list, tuple, dict, path_t, array_t, graph_t, Any]


_ERROR_MARKER = "!"  # Must be a character forbidden in type names
_TYPES_SEPARATOR = "@"  # Must be a character forbidden in type names


def JsonStringOf(instance: Any, /, *, true_type: Union[Any, type] = None) -> str:
    """"""
    if not ((true_type is None) or (type(true_type) is type)):
        true_type = type(true_type)

    return json.dumps(_JsonDescriptionOf(instance, 0, true_type=true_type))


def _JsonDescriptionOf(
    instance: Any, calling_level: int, /, *, true_type: type = None
) -> description_h:
    """"""
    # Test for high-level classes first since they can also be subclasses of standard classes below, but only if not
    # called from the instance.AsJsonString method, which would create infinite recursion.
    if (calling_level > 0) and hasattr(instance, "AsJsonString"):
        return _JsonDescriptionOf(
            instance.AsJsonString(),
            calling_level + 1,
            true_type=_AutomaticTrueType(instance, true_type),
        )

    if dtcl.is_dataclass(instance):
        # Do not use dtcl.asdict(self) since it recurses into dataclass instances which, if they extend a "container"
        # class like list or dict, will lose the contents.
        as_dict = {
            _fld.name: getattr(instance, _fld.name) for _fld in dtcl.fields(instance)
        }
        true_type = _AutomaticTrueType(instance, true_type)

        return _JsonDescriptionOf(as_dict, calling_level + 1, true_type=true_type)

    error = ""

    # /!\ Must be the first type to be tested (see unfoundable modules above)
    if isinstance(instance, bytes):
        base_type, jsonable = "bytes", instance.hex()
    elif isinstance(instance, enum_t):
        true_type = _AutomaticTrueType(instance, true_type)
        base_type, jsonable = "enum_Enum", _JsonDescriptionOf(
            instance.value, calling_level + 1
        )
    elif isinstance(instance, slice):
        base_type, jsonable = "slice", (instance.start, instance.stop, instance.step)
    elif isinstance(instance, (list, tuple)):
        base_type, jsonable = (
            type(instance).__name__,
            [_JsonDescriptionOf(_elm, calling_level + 1) for _elm in instance],
        )
    elif isinstance(instance, dict):
        # json does not accept non-str dictionary keys, hence the json.dumps
        base_type, jsonable = (
            "dict",
            {
                json.dumps(
                    _JsonDescriptionOf(_key, calling_level + 1)
                ): _JsonDescriptionOf(_vle, calling_level + 1)
                for _key, _vle in instance.items()
            },
        )
    elif isinstance(instance, path_t):
        base_type, jsonable = "pathlib_Path", str(instance)
    elif isinstance(instance, array_t):
        base_type, jsonable = "numpy_ndarray", (instance.tolist(), instance.dtype.name)
    elif isinstance(instance, graph_t):
        edges = grph.to_dict_of_dicts(instance)
        # /!\ Node attributes are added to the edges dictionary! This must be taken into account when deJSONing. Note
        # that several attempts to avoid this have been made, including one relying on repr(node), which is based on
        # hash(node). Since the hash function gives different results across Python sessions, this could not work.
        for node, attributes in instance.nodes(data=True):
            edges[node] = (attributes, edges[node])
        base_type, jsonable = (
            "networkx_Graph",
            (
                _JsonDescriptionOf(edges, calling_level + 1),
                type(instance).__name__,
            ),
        )
    else:
        base_type = type(instance).__name__
        try:
            _ = json.dumps(instance)
            jsonable = instance
        except TypeError:
            jsonable = None
            error = _ERROR_MARKER
            LOGGER.warn(f"{base_type}: UnJSONable type. Using None.")

    if true_type is None:
        true_type = ""
    else:
        true_type = true_type.__name__

    return f"{base_type}{_TYPES_SEPARATOR}{true_type}{error}", jsonable


def ObjectFromJsonString(jsoned: str, /, *, builders: builders_h = None) -> object_h:
    """"""
    return _ObjectFromJsonDescription(json.loads(jsoned), builders=builders)


def _ObjectFromJsonDescription(
    description: description_h,
    /,
    *,
    builders: builders_h = None,
) -> object_h:
    """"""
    types, instance = description
    base_type, true_type = types.split(_TYPES_SEPARATOR)
    if true_type.endswith(_ERROR_MARKER):
        true_type = true_type[: -_ERROR_MARKER.__len__()]
        error = True
    else:
        error = False
    if true_type.__len__() == 0:
        true_type = None
    if builders is None:
        builders = {}

    if error:
        LOGGER.warn(
            f"{base_type}{_TYPES_SEPARATOR}{true_type}: UnJSONable type. Returning None."
        )
        return None

    if base_type == "bytes":
        output = bytes.fromhex(instance)
    elif base_type == "enum_Enum":
        output = _ObjectFromJsonDescription(instance, builders=builders)
    elif base_type == "slice":
        output = slice(*instance)
    elif base_type in ("list", "tuple"):
        iterator = (
            _ObjectFromJsonDescription(_elm, builders=builders) for _elm in instance
        )
        if base_type == "list":
            output = list(iterator)
        else:
            output = tuple(iterator)
    elif base_type == "dict":
        output = {
            _ObjectFromJsonDescription(
                json.loads(_key), builders=builders
            ): _ObjectFromJsonDescription(_vle, builders=builders)
            for _key, _vle in instance.items()
        }
    elif base_type == "pathlib_Path":
        output = path_t(instance)
    elif base_type == "numpy_ndarray":
        data, dtype = instance
        output = nmpy.array(data, dtype=dtype)
    elif base_type == "networkx_Graph":
        edges_w_attributes, graph_type = instance
        edges_w_attributes = _ObjectFromJsonDescription(edges_w_attributes, builders=builders)
        graph_type = getattr(grph, graph_type)

        attributes = {}
        edges = {}
        for node, (node_attributes, edge) in edges_w_attributes.items():
            attributes[node] = node_attributes
            edges[node] = edge

        output = grph.from_dict_of_dicts(edges, create_using=graph_type)
        grph.set_node_attributes(output, attributes)
    else:
        output = instance

    if true_type in builders:
        output = builders[true_type](output)
    elif true_type is not None:
        output = None
        LOGGER.warn(f"{true_type}: Type without decoder. Returning None.")

    return output


def _AutomaticTrueType(instance: Any, true_type: Optional[type], /) -> type:
    """"""
    if true_type is None:
        return type(instance)

    # This was added to support passing a true type of an object built from a subclass instance. Usage example:
    # decomposition of an instance of a class with multiple inheritance into its components built from the instance
    # itself.
    if issubclass(type(instance), true_type):
        return true_type

    raise ValueError(
        f'{true_type.__name__}: Invalid true type specification for type "{type(instance).__name__}". Expected: None.'
    )
