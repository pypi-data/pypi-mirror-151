from __future__ import annotations

import numpy as np

from typing import Any, TypeAlias, Union, Callable


class Ops(object):
    identity: str = 'identity'
    var: str = 'var'
    const: str = 'const'

    add: str = 'add'
    neg: str = 'neg'
    sub: str = 'sub'

    mul: str = 'mul'
    truediv: str = 'truediv'
    floordiv: str = 'floordiv'

    pow: str = 'pow'

    abspow: str = 'abspow'

    sin: str = 'sin'
    cos: str = 'cos'
    tan: str = 'tan'
    arctan2: str = 'arctan2'

    exp: str = 'exp'
    log: str = 'log'

    abs: str = 'abs'
    relu: str = 'relu'
    maximum: str = 'maximum'
    minimum: str = 'minimum'

    getitem: str = 'getitem'
    call: str = 'call'
    attrib: str = 'attrib'

    assign: str = 'assign'
    tupl_unload: str = 'ast'
    dict_unload: str = 'astast'


class Atom(object):
    _identifier: str | None = None
    use_identifier: bool = None
    op: str = None
    deps: tuple[Self, ...] = None

    val: float | int | bool | None

    callback: Callable[[Self], None] | None = None

    @classmethod
    def identity(cls, arg: Union[Self, int, float, bool, str], callback: Callable[[Self], None] | None = None) -> Self:
        if (callback is None) and hasattr(arg, 'callback'): callback = arg.callback
        arg = cls.ensure(arg, callback = callback)
        return cls(Ops.identity, (arg,), callback = arg.callback)

    @classmethod
    def var(cls, identifier: str | None = None, callback: Callable[[Self], None] | None = None) -> Self:
        return cls(Ops.var, tuple(), identifier = identifier, callback = callback)

    @classmethod
    def const(cls, val: int | float | bool | str, callback: Callable[[Self], None] | None = None):
        return cls(Ops.const, tuple(), val = val, callback = callback)

    @classmethod
    def ensure(cls, other: Union[Self, int, float, bool, str], callback: Callable[[Self], None] | None = None) -> Self:
        if isinstance(other, Atom):
            if not (other.callback is callback): raise AssertionError('callback mismatch!')
            return other
        return cls.const(val = other, callback = callback)

    def __init__(self,
                 op: str,
                 deps: tuple[Self, ...],
                 val: int | float | bool | str | None = None,
                 identifier: str | None = None,
                 callback: Callable[[Self], None] | None = None):
        self.identifier = identifier
        self.use_identifier = False if op != Ops.var else True
        self.op = op
        self.deps = deps
        if self.op != Ops.call:
            for dep in self.deps:
                if dep.op in (Ops.assign, Ops.tupl_unload, Ops.dict_unload):
                    raise AssertionError('assignments, ast, astast can only be used within calls!')

        self.val = val

        self.callback = callback
        if (self.callback is None) and (len(self.deps) > 0): self.callback = self.deps[0].callback
        for dep in self.deps:
            if not (dep.callback is self.callback): raise AssertionError('callback missmatch!')

        self.callback(self)

    @property
    def identifier(self) -> str: return self._identifier

    @identifier.setter
    def identifier(self, new_ident: str | None) -> None:
        if new_ident is None: self._identifier = None
        else:
            if not isinstance(new_ident, str): raise AssertionError('identifier need to be string!')
            for idx, letter in enumerate(new_ident.lower()):
                if letter in 'abcdefghijklmnopqrstuvwxyz_': continue
                elif (idx > 0) and (letter in '0123456789'): continue
                raise AssertionError(f'invalid char: "{new_ident[idx]}" within {new_ident}!')
            self._identifier = new_ident

    @property
    def paren_group(self) -> int:
        '''
            paren_group (parentheses group)
            0 - bivariate linear (+ [binary], - [binary])
            1 - univariate linear (- [unary])
            2 - product (*)
            3 - division (/, //) (special rule: 0, 2, 3 require parenthesis)  # note: 0, 2 not strictly necessary here!
            4 - (default) -or- nonlinear operations (var, const, sin, abs, ...) (special rule: no parenthesis at all)
            5 - other bivariate ops (%, **) (special rule: 5 require parenthesis)
        '''
        match self.op:
            case Ops.add: return 0
            case Ops.neg: return 1
            case Ops.sub: return 0
            case Ops.mul: return 2
            case Ops.truediv: return 3
            case Ops.floordiv: return 3
            case Ops.pow: return 5
        return 4

    def str(self, outer_paren_group: int | None = None, use_identifier: bool | None = None) -> str:
        cls = self.__class__
        
        if use_identifier is None: use_identifier = self.use_identifier
        if use_identifier:
            if self.identifier is None: raise AssertionError('use_identifier == True, but identifier is None!')
            return self.identifier

        match self.op:
            case Ops.identity: return self.deps[0].str(outer_paren_group = outer_paren_group)
            case Ops.var:
                if len(self.deps) == 1: return self.deps[0].str(outer_paren_group = outer_paren_group)
                elif len(self.deps) > 1: 
                    raise AssertionError(f'{cls.__name__}.var cannot have more then one dependency!')
                if not (self.val is None): return str(self.val)
                raise AssertionError(f'{cls.__name__}.var needs to use identifier, or have a dependency or a value!')
            case Ops.const: return str(self.val)

        out: str = ''
        u = self.deps[0].str(self.paren_group)
        w = None
        if len(self.deps) > 1: w = self.deps[1].str(self.paren_group)

        match self.op:
            case Ops.add: out = f'{u} + {w}'
            case Ops.neg: out = f'-{u}'
            case Ops.sub: out = f'{u} - {w}'

            case Ops.mul: out = f'{u}*{w}'
            case Ops.truediv: out = f'{u}/{w}'
            case Ops.floordiv: out = f'{u}//{w}'

            case Ops.pow: out = f'{u}**{w}'

            case Ops.attrib: out = f'{u}.{w}'

            case Ops.tupl_unload: out = f'*{u}'
            case Ops.dict_unload: out = f'**{u}'

        u = self.deps[0].str(None)
        w = None
        if len(self.deps) > 1: w = self.deps[1].str(None)

        match self.op:
            case Ops.abspow: out = f'abspow({u}, {w})'

            case Ops.sin: out = f'sin({u})'
            case Ops.cos: out = f'cos({u})'
            case Ops.tan: out = f'tan({u})'
            case Ops.arctan2: out = f'arctan2({u})'

            case Ops.exp: out = f'exp({u})'
            case Ops.log: out = f'log({u})'

            case Ops.abs: out = f'abs({u})'
            case Ops.relu: out = f'relu({u})'

            case Ops.assign: out = f'{u} = {w}'

        _tmp = None
        if self.op in (Ops.maximum, Ops.minimum): _tmp = ', '.join([dep.str(None) for dep in self.deps])
        match self.op:
            case Ops.maximum: out = f'maximum({_tmp})'
            case Ops.minimum: out = f'maximum({_tmp})'

        u = self.deps[0].str(self.paren_group)
        if self.op in (Ops.getitem, Ops.call): _tmp = ', '.join([dep.str(None) for dep in self.deps[1:]])
        match self.op:
            case Ops.getitem: out = f'{u}[{_tmp}]'
            case Ops.call: out = f'{u}({_tmp})'

        use_paren: bool = False
        if not (outer_paren_group is None):
            if self.paren_group == 5: use_paren = True
            elif self.paren_group == 4: use_paren = False
            elif (self.paren_group == 3) and (outer_paren_group in (0, 2, 3)): use_paren = True
            elif outer_paren_group > self.paren_group: use_paren = True
        if use_paren: out = f'({out:s})'
        return out

    def __str__(self) -> str:
        return self.str()

    def __pos__(self) -> Self:
        return self.__class__.identity(self)

    def __add__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.add, (self, other))

    def __radd__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other + self

    def __neg__(self) -> Self:
        cls = self.__class__
        return cls(Ops.neg, (self,))

    def __sub__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.sub, (self, other))

    def __rsub__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other - self

    def __mul__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.mul, (self, other))

    def __rmul__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other*self

    def __truediv__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.truediv, (self, other))

    def __rtruediv__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other/self

    def __floordiv__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.floordiv, (self, other))

    def __rfloordiv__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other//self

    def __pow__(self, other: Union[Self, int, float, bool, str]) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.pow, (self, other))

    def __rpow__(self, other: int | float | bool) -> Self:
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other**self

    def abspow(self, other: Union[Self, int, float, bool, str] = 2.0):
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.abspow, (self, other))

    def rabspow(self, other: int | float | bool):
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other.abspow(self)

    def sin(self):
        cls = self.__class__
        return cls(Ops.sin, (self,))

    def cos(self):
        cls = self.__class__
        return cls(Ops.cos, (self,))

    def tan(self):
        cls = self.__class__
        return cls(Ops.tan, (self,))

    def arctan2(self, other: Union[Self, int, float, bool, str]):
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.arctan2, (self, other))

    def atan2(self, *args, **kwargs):
        return self.arctan2(*args, **kwargs)

    def rarctan2(self, other: int | float | bool):
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return other.arctan2(self)

    def ratan2(self, *args, **kwargs):
        return self.rarctan2(*args, **kwargs)

    def exp(self):
        cls = self.__class__
        return cls(Ops.exp, (self,))

    def log(self):
        cls = self.__class__
        return cls(Ops.log, (self,))

    def __abs__(self):
        cls = self.__class__
        return cls(Ops.abs, (self,))

    def relu(self):
        cls = self.__class__
        return cls(Ops.relu, (self,))

    def maximum(self, *others: Union[Self, int, float, bool, str]):
        cls = self.__class__
        if not (self in others): args = [self]
        else: args = []
        args.extend([cls.ensure(other, callback = self.callback) for other in others])
        return cls(Ops.maximum, tuple(args))

    def max(self, *args):
        return self.maximum(*args)

    def minimum(self, *others: Union[Self, int, float, bool, str]):
        cls = self.__class__
        if not (self in others): args = [self]
        else: args = []
        args.extend([cls.ensure(other, callback = self.callback) for other in others])
        return cls(Ops.minimum, tuple(args))

    def min(self, *args):
        return self.minimum(*args)

    def __getitem__(self, *items: Union[Self, int, float, bool, str]):
        cls = self.__class__
        new_items = [cls.ensure(item, callback = self.callback) for item in items]
        return cls(Ops.getitem, (self, *new_items))

    def __call__(self, *args: Union[Self, int, float, bool, str]):
        cls = self.__class__
        new_args = [cls.ensure(arg, callback = self.callback) for arg in args]
        return cls(Ops.call, (self, *new_args))

    def attrib(self, attr: Union[Self, int, float, bool, str]):
        cls = self.__class__
        attr = cls.ensure(attr, callback = self.callback)
        return cls(Ops.attrib, (self, attr))

    def assign(self, other: Union[Self, int, float, bool, str]):
        cls = self.__class__
        other = cls.ensure(other, callback = self.callback)
        return cls(Ops.assign, (self, other))

    def tupl_unload(self):
        cls = self.__class__
        return cls(Ops.tupl_unload, (self,))

    def dict_unload(self):
        cls = self.__class__
        return cls(Ops.dict_unload, (self,))


class ExpressionGraph(object):

    ops: list[Atom] = None

    def __init__(self):
        self.ops = list()

    def callback(self, op: Atom):
        self.ops.append(op)
