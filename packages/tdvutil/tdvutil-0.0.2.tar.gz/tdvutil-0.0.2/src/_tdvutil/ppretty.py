# This is the `ppretty` module, with some local adjustments for things
# like allowing keys to be excluded by name, and slightly less irritating
# defaults.
#
# You can find the original code at https://github.com/symonsoft/ppretty
#
# I've attempted to do some actual typing on this, though some of it is almost
# certainly wrong, because I don't 100% understand the code.
#
# type: ignore
from functools import partial
from inspect import isroutine
from numbers import Number

# from typing import List, Optional, Dict, Tuple, Set, Union, Any, cast, Iterable
# from typing_extensions import reveal_type


def ppretty(obj, *, indent='    ', depth=4, width=72, seq_length=100,
            show_protected=False, show_private=False, show_static=False,
            show_properties=False, show_address=False, str_length=50,
            ignore=None):
    """Break down a python object into a human readable format.

    :param obj: An object to represent.
    :type obj: object
    :param indent: Fill string for indents.
    :type indent: str
    :param depth: Maximum depth of introspection
    :type depth: int
    :param width: Width of a line in the output string. May be exceeded when a representation doesn't fit.
    :type width: int
    :param seq_length: Maximum sequence length to examine for lists, sets, dicts, and class members.
    :type seq_length: int
    :param show_protected: Introspect protected members.
    :type show_protected: bool
    :param show_private: Introspect private members. To take effect show_protected must also be set to True. (FIXME: do this automatically)
    :type show_private: bool
    :param show_static: Introspect static members.
    :type show_static: bool
    :param show_properties: Introspect property members.
    :type show_properties: bool
    :param show_address: Show memory address.
    :type show_address: bool
    :param str_length: Maximum string length.
    :type str_length: int
    :param ignore: Names of key names to ignore. Just checks the base key name, with no facility for specifying a more complete path
    :type ignore: List[str] | Set[str]

    :return: The final textual representation of the object.
    :rtype: str
    """

    seq_brackets = {list: ('[', ']'), tuple: ('(', ')'), set: ('set([', '])'), dict: ('{', '}')}
    seq_types = tuple(seq_brackets.keys())

    ignore = set(ignore) if ignore else set()

    def inspect_object(current_obj, current_depth, current_width, seq_type_descendant=False):
        inspect_nested_object = partial(inspect_object,
                                        current_depth=current_depth - 1,
                                        current_width=current_width - len(indent))

        # Basic types
        if isinstance(current_obj, Number):
            return [repr(current_obj)]

        # Strings
        if isinstance(current_obj, str):
            if len(current_obj) <= str_length:
                return [repr(current_obj)]
            return [repr(current_obj[:int(str_length / 2)] + '...' + current_obj[int((1 - str_length) / 2):])]

        # Class object
        if isinstance(current_obj, type):
            module = current_obj.__module__ + '.' if hasattr(current_obj, '__module__') else ''
            return ["<class '" + module + current_obj.__name__ + "'>"]

        # None
        if current_obj is None:
            return ['None']


        # Format block of lines


        def format_block(lines, open_bkt='', close_bkt=''):
            new_lines = []  # new_lines will be returned if width exceeded
            one_line = ''  # otherwise, one_line will be returned.
            if open_bkt:
                new_lines.append(open_bkt)
                one_line += open_bkt
            for line in lines:
                new_lines.append(indent + line)
                if len(one_line) <= current_width:
                    one_line += line
            if close_bkt:
                if lines:
                    new_lines.append(close_bkt)
                else:
                    new_lines[-1] += close_bkt
                one_line += close_bkt

            return [one_line] if len(one_line) <= current_width and one_line else new_lines

        class SkipElement(object):
            pass

        class ErrorAttr(object):
            def __init__(self, e: Exception):
                self.e = e

        def cut_seq(seq):
            if current_depth < 1:
                return [SkipElement()]
            seq = list(seq) if isinstance(seq, tuple) else seq

            if len(seq) <= seq_length or seq_length == 0:
                return seq
            elif seq_length > 1:
                return seq[:int(seq_length / 2)] + [SkipElement()] + seq[int((1 - seq_length) / 2):]
            return [SkipElement()]

        def format_seq(extra_lines):
            r = []
            items = cut_seq(obj_items)

            for n, i in enumerate(items, 1):
                if type(i) is SkipElement:
                    r.append('...')
                else:
                    if type(current_obj) is dict or seq_type_descendant and isinstance(current_obj, dict):
                        (k, v) = i

                        if isinstance(k, str) and k in ignore:
                            r.append('...')
                            if n < len(items) or extra_lines:
                                r[-1] += ', '
                                continue
                        k = inspect_nested_object(k)
                        v = inspect_nested_object(v)
                        k[-1] += ': ' + v.pop(0)
                        r.extend(k)
                        r.extend(format_block(v))
                    elif type(current_obj) in seq_types or seq_type_descendant and isinstance(current_obj, seq_types):
                        r.extend(inspect_nested_object(i))
                    else:
                        (k, v) = i
                        if k in ignore:
                            continue
                        k = [k]
                        if type(v) is ErrorAttr:
                            e_message: str = '<Attribute error: ' + type(v.e).__name__
                            if hasattr(v.e, 'message'):
                                e_message = e_message + ': ' + getattr(v.e, 'message')
                            e_message += '>'
                            v = [e_message]
                        else:
                            v = inspect_nested_object(v)
                        k[-1] += ' = ' + v.pop(0)
                        r.extend(k)
                        r.extend(format_block(v))
                if n < len(items) or extra_lines:
                    r[-1] += ', '
            return format_block(r + extra_lines, *brackets)

        # Sequence types
        # Others objects are considered as sequence of members
        extra_lines = []
        if type(current_obj) in seq_types or seq_type_descendant and isinstance(current_obj, seq_types):
            if isinstance(current_obj, dict):
                obj_items = list(current_obj.items())
            else:
                obj_items = current_obj

            if seq_type_descendant:
                brackets = seq_brackets[[
                    seq_type for seq_type in seq_types if isinstance(current_obj, seq_type)].pop()]
            else:
                brackets = seq_brackets[type(current_obj)]
        else:
            obj_items = []
            for k in sorted(dir(current_obj)):
                if not show_private and k.startswith('_') and '__' in k:
                    continue
                if not show_protected and k.startswith('_'):
                    continue
                try:
                    v = getattr(current_obj, k)
                    if isroutine(v):
                        continue
                    if not show_static and hasattr(type(current_obj), k) and v is getattr(type(current_obj), k):
                        continue
                    if not show_properties and hasattr(type(current_obj), k) and isinstance(
                            getattr(type(current_obj), k), property):
                        continue
                except Exception as e:
                    v = ErrorAttr(e)

                obj_items.append((k, v))

            if isinstance(current_obj, seq_types):
                # If object's class was inherited from one of basic sequence types
                extra_lines += inspect_nested_object(current_obj, seq_type_descendant=True)

            try:
                if hasattr(current_obj, '__module__') and current_obj.__module__ is not None:
                    module = current_obj.__module__ + '.'
                else:
                    module = ''
            except Exception:
                print(f"blew up on type {type(current_obj.__module__)}")
                raise
            address = ' at ' + hex(id(current_obj)) + ' ' if show_address else ''
            brackets = (module + type(current_obj).__name__ + address + '(', ')')

        return format_seq(extra_lines)

    return '\n'.join(inspect_object(obj, depth, width))


if __name__ == '__main__':
    class B(object):
        def __init__(self, b) -> None:
            self.b = b

    class A(object):
        i = [-3, 4.5, ('6', B({'\x07': 8}))]

        def __init__(self, a) -> None:
            self.a = a

    class C(object):
        def __init__(self) -> None:
            self.a = {u'1': A(2), '9': [1000000000000000000000, 11, {
                (12, 13): {14, None}}], 15: [16, 17, 18, 19, 20]}
            self.b = 'd'
            self._c = C.D()
            self.e = C.D

        d = 'c'

        def foo(self) -> None:
            pass

        @property
        def bar(self) -> str:
            return 'e'

        class D(object):
            pass


    print(ppretty(C(), indent='    ', depth=8, width=41, seq_length=100,
                  show_static=True, show_protected=True, show_properties=True, show_address=True))
    print(ppretty(C(), depth=8, width=200, seq_length=4))

    class E(dict):
        def __init__(self) -> None:
            dict.__init__(self, yyy='xxx')
            self.www = 'Very long text Bla-Bla-Bla'

    print(ppretty(E(), str_length=19))

    print(ppretty({x: x for x in range(10)}))
