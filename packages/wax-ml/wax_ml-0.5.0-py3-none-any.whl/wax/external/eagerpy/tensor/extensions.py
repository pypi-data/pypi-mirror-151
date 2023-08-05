# Copyright 2021 The WAX-ML Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import functools
import typing
from typing import Any, Callable, Generic, TypeVar

from .. import norms
from .tensor import Tensor

T = TypeVar("T")


def extensionmethod(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        return f(self._instance, *args, **kwargs)

    return wrapper


class ExtensionMeta(type):
    def __new__(cls, name, bases, attrs):  # type: ignore
        if bases != ():
            # creating a subclass of ExtensionMethods
            # wrap the attributes with extensionmethod
            attrs = {
                k: extensionmethod(v) if not k.startswith("__") else v
                for k, v in attrs.items()
            }
        return super().__new__(cls, name, bases, attrs)


if hasattr(typing, "GenericMeta"):  # Python 3.6
    # workaround for https://github.com/python/typing/issues/449
    class GenericExtensionMeta(typing.GenericMeta, ExtensionMeta):  # type: ignore
        pass

else:  # pragma: no cover  # Python 3.7 and newer

    class GenericExtensionMeta(ExtensionMeta):  # type: ignore
        pass


class ExtensionMethods(metaclass=GenericExtensionMeta):
    def __init__(self, instance: Tensor):
        self._instance = instance


T_co = TypeVar("T_co", bound=Tensor, covariant=True)


class NormsMethods(Generic[T_co], ExtensionMethods):
    l0: Callable[..., T_co] = norms.l0
    l1: Callable[..., T_co] = norms.l1
    l2: Callable[..., T_co] = norms.l2
    linf: Callable[..., T_co] = norms.linf
    lp: Callable[..., T_co] = norms.lp
