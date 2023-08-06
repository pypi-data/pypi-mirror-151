# It's really really difficult to type the ppretty module, but if I
# start trying, even by just giving a type definition to the top level
# ppretty() function, everything else in the file complains because
# it thinks it should be type checking, but the rest isn't typed (or
# isn't typed in a way that it considers correct). So by moving the
# typing info to this .pyi stub, things external to ppretty can still
# do type checking when calling it, but doesn't trigger a ton of mypy/
# pylance errors in ppretty itself.
#
# Yeah, it's probably not worth this much effort, but here we are.

# pyright: reportInvalidStubStatement=false
from typing import List, Optional, Set, Union

def ppretty(obj: object, *, indent: str = "    ", depth: int = 4,
            width: int = 72, seq_length: int = 100,
            show_protected: bool = False, show_private: bool = False,
            show_static: bool = False, show_properties: bool = False,
            show_address: bool = False, str_length: int = 50,
            ignore: Optional[Union[List[str], Set[str]]] = None) -> str:
    pass
