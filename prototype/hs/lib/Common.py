from hs.lib.Symbols.Types import (Primitive)

class Common:
    class GlobalEntry:
        def __init__(self, key: str, value: str, type: any, scope: str = "LET", *, strict: bool = False, onChange: str or callable = None):
            self.key = key
            self.value = value
            self.type: Primitive = type
            self.scope = scope
            self.onChange = []

            """ Raise an error if re-assigned to a type not matching `self.type` """
            self.strict: bool = strict

            assert scope in ["LET", "CONST"], f"Invalid scope: \"{scope}\""

            self.addWatcher(onChange = onChange)

        def addWatcher(self, onChange: str or callable = None):
            if not onChange: return

            self.onChange.append(onChange)

        def triggerWatchers(self, oldValue, newValue):
            for watcher in self.onChange:
                if type(watcher) is str:
                    pass
                else:
                    watcher(oldValue, newValue)

    class GlobalList:
        def __init__(self):
            self._globals = dict()

        def __contains__(self, item: str) -> bool:
            return type(item) is str and item in self._globals

        def contains(self, item: str) -> bool:
            return type(item) is str and item in self._globals

        def add_watcher(self, item: str, watcher: str or callable):
            if not self.contains(item): return

            self._globals[item].addWatcher(watcher)

        def set(self, item: str, *, key: str = None, value: str = None, type: Primitive = None, scope: str = None, strict: bool = False) -> None:
            if not isinstance(item, str) or not self.contains(item):
                self._globals[item] = Common.GlobalEntry(key, value, type, scope)
                return

            entry = self._globals[item]
            entry: Common.GlobalEntry

            if key: entry.key = key
            if value:
                old,new = entry.value,value
                entry.triggerWatchers(old, new)
                entry.value = new
            if type: entry.type = type
            if scope: entry.scope = scope
            if strict: entry.strict = strict

        def get(self, item: str) -> 'Common.GlobalEntry':
            if item not in self._globals: return None

            return self._globals[item]