from abc import abstractmethod, ABC
from typing import Union


class BaseParser(ABC):
    @abstractmethod
    def help(self, strs: list[str]) -> str:
        pass

    @abstractmethod
    def parse(self, strs: list[str]):
        pass


ArgsRequirement = Union['none', 'optional', 'required']


class CommandExecutor:
    def __init__(self, callback: callable, args: ArgsRequirement = 'none'):
        self.callback = callback
        self.require_args = args

    def help(self):
        if self.require_args == 'none':
            return ''
        elif self.require_args == 'optional':
            return '[args]'
        elif self.require_args == 'required':
            return '<args>'

    def execute(self, objs: tuple[str, Union[tuple[int], None]] = None, args: list[str] = None):
        self.callback(objs, args)


ParserType = Union[dict[str, Union[BaseParser, CommandExecutor]], CommandExecutor]


class CommandParser(BaseParser):
    def __init__(self, parser: ParserType = None):
        self.commands = parser or {}

    def help(self, strs: list[str]):
        if not strs:
            return f"/<{'/'.join(self.commands.keys())}>"
        _str = strs[0]
        if not _str:
            return f"/<{'/'.join(self.commands.keys())}>"
        if _str[0] == '/':
            if len(_str) > 1:
                _str = _str[1:]
            else:
                _str = ''
        if not _str:
            return f"/<{'/'.join(self.commands.keys())}>"
        else:
            for key, parser in self.commands.items():
                if _str[0] == key[0] and _str in key:
                    if isinstance(parser, BaseParser):
                        return f"/{key} " + parser.help(strs[1:] if len(strs) > 1 else [])
                    elif isinstance(parser, CommandExecutor):
                        return f"/{key} " + parser.help()
        return 'Unknown command.'

    def parse(self, act_str: list[str]):
        if not act_str:
            return
        act = act_str[0]
        if act[0] == '/':
            if len(act) > 1:
                act = act[1:]
            else:
                act = ''
        if act in self.commands:
            parser = self.commands[act_str[0]]
            if isinstance(parser, BaseParser):
                return parser.parse(act_str[1:])
            elif isinstance(parser, CommandExecutor):
                return parser.execute(args=act_str[1:])
        else:
            raise ValueError(f"Unknown command {act_str[0]}")


class ActParser(BaseParser):
    def __init__(self, parser: ParserType = None):
        self.acts = parser or {}

    def help(self, strs: list[str]):
        _str = strs[0] if strs else ''
        if not _str:
            return f"<{'/'.join(self.acts.keys())}>"
        else:
            for key, parser in self.acts.items():
                if _str in key:
                    if isinstance(parser, BaseParser):
                        return f"<{key}> " + parser.help(strs[1:] if len(strs) > 1 else [])
                    elif isinstance(parser, CommandExecutor):
                        return f"<{key}> " + parser.help()
        return ''

    def parse(self, act_str: list[str]):
        if act_str[0] in self.acts:
            parser = self.acts[act_str[0]]
            if isinstance(parser, BaseParser):
                return parser.parse(act_str[1:])
            elif isinstance(parser, CommandExecutor):
                return parser.execute(args=act_str[1:])
        else:
            raise ValueError(f"Unknown action {act_str[0]}")


class ObjParser(BaseParser):
    def __init__(self, parser: ParserType = None):
        if not isinstance(parser, CommandExecutor):
            raise TypeError(f"Parser must be CommandExecutor, not {type(parser)}")
        self.executor = parser
        self.objs = {'t', 'a', 'f', 's', 'e', 'l'}

    def help(self, strs: list[str]):
        print("hah", strs)
        _str = strs[0] if strs else ''
        if not _str:
            return f"@<{'/'.join(self.objs)}>"
        else:
            if _str[0] == '@':
                _str = _str[1:]
            if _str and _str[0] in self.objs:
                if _str[0] == 't':
                    if len(_str) >= 2 and _str[1] == '[':
                        if len(_str) >= 3 and _str[-1] == ']':
                            return '@' + _str + ' ' + self.executor.help()
                        return '@' + _str + '] ' + self.executor.help()
                    return '@' + _str + '[tid,...] ' + self.executor.help()
                else:
                    return '@' + _str + ' ' + self.executor.help()
        return ''

    def parse(self, obj_str: list[str]):
        """parse object string like @t[0] to object"""
        rest_list = obj_str[1:]
        obj_str = obj_str[0]
        if obj_str[0] == '@':
            obj_str = obj_str[1:]
        if obj_str[0] in self.objs:
            if len(obj_str) >= 3 and obj_str[1] == '[':
                tid = tuple(map(int, obj_str[2:-1].split(',')))
            else:
                tid = None
            self.executor.execute(objs=(obj_str[0], tid), args=rest_list)
        else:
            raise ValueError(f"Unknown object {obj_str[0]}")
