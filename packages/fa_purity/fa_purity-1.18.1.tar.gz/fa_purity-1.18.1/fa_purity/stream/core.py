from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    _iter_factory,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
import functools
from typing import (
    Callable,
    Generic,
    Iterable,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class _Stream(
    Generic[_T],
):
    _new_iter: Cmd[Iterable[_T]]


class Stream(_Stream[_T]):
    def __init__(self, obj: _Stream[_T]):
        super().__init__(obj._new_iter)

    def map(self, function: Callable[[_T], _R]) -> Stream[_R]:
        draft: _Stream[_R] = _Stream(
            self._new_iter.map(lambda i: iter(map(function, i)))
        )
        return Stream(draft)

    def reduce(self, function: Callable[[_R, _T], _R], init: _R) -> Cmd[_R]:
        return self._new_iter.map(
            lambda i: functools.reduce(function, i, init)
        )

    def bind(self, function: Callable[[_T], Stream[_R]]) -> Stream[_R]:
        def _action(act: CmdUnwrapper) -> Iterable[_R]:
            items = act.unwrap(self.map(function)._new_iter)
            unchained = iter(act.unwrap(i._new_iter) for i in items)
            return _iter_factory.chain(unchained)

        draft: _Stream[_R] = _Stream(new_cmd(_action))
        return Stream(draft)

    def filter(self, function: Callable[[_T], bool]) -> Stream[_T]:
        draft = _Stream(
            self._new_iter.map(lambda i: iter(filter(function, i)))
        )
        return Stream(draft)

    def find_first(self, criteria: Callable[[_T], bool]) -> Cmd[Maybe[_T]]:
        return self._new_iter.map(
            lambda i: _iter_factory.find_first(criteria, i)
        ).map(Maybe.from_optional)

    def chunked(self, size: int) -> Stream[FrozenList[_T]]:
        draft = _Stream(
            self._new_iter.map(lambda i: _iter_factory.chunked(i, size))
        )
        return Stream(draft)

    def transform(self, function: Callable[[Stream[_T]], _R]) -> _R:
        return function(self)

    def to_list(self) -> Cmd[FrozenList[_T]]:
        return self._new_iter.map(tuple)

    def unsafe_to_iter(self) -> Cmd[Iterable[_T]]:
        # if possible iterables should not be used directly
        return self._new_iter
