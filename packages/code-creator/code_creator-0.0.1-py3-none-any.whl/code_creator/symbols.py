from typing import Union, TypeAlias


symbol_t: TypeAlias = str
symbol_degree_t: TypeAlias = tuple[symbol_t, int]
tag_t: TypeAlias = str


class Symbol(object):
    # class var
    _all_sym_insts: set['Symbol'] = set()  # insts: instances
    _all_sym_chars: set[symbol_t] = set()  # chars: characters
    _sym_reg: dict[str, 'Symbol'] = dict()  # sym: symbol

    # instance var
    base_sym: symbol_t = None
    comment: str | None = None

    def __init__(self, base_sym: symbol_t, comment: str | None = None):
        if not isinstance(base_sym, str): raise AssertionError('Symbol can only be str!')
        if ' ' in base_sym: raise AssertionError('whitespaces are not allowed within symbols!')
        if base_sym in self.__class__._all_sym_chars: raise AssertionError('exists already!')

        self.base_sym = base_sym
        self.comment = comment

        self.__class__._all_sym_insts.add(self)
        self.__class__._all_sym_chars.add(base_sym)
        self.__class__._sym_reg[base_sym] = self

    def __del__(self) -> None:
        cls = self.__class__
        if not (self.base_sym is None):
            cls._all_sym_chars.remove(self.base_sym)
            cls._all_sym_insts.remove(self)
            del cls._sym_reg[self.base_sym]

    @classmethod
    def exists(cls, item: symbol_t) -> bool: return item in cls._all_sym_chars

    @classmethod
    def get(cls, item: symbol_t) -> Union['Symbol', None]: return cls._sym_reg.get(item, None)

    def __str__(self) -> str: return self.base_sym

    def d(self, *dargs: symbol_degree_t) -> str:
        dargs = [f'{darg[0]}:{darg[1]}' for darg in dargs if darg[1] > 0]
        if len(dargs) == 0: return str(self)
        return f'D[{", ".join(dargs)}] {str(self)}'
