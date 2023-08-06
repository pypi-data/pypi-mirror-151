import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, List, TypeVar, cast

TFunc = TypeVar("TFunc", bound=Callable[..., Any])

def pathfix(func: TFunc) -> TFunc:
    """
    Decorator to help with transitioning to using :class:`pathlib.Path` in
    functions that currently accept `str` or :class:`os.PathLike` as an
    argument. Functions decorated with `@pathfix` will automatically have
    any arguments typed as :class:`pathlib.Path` converted to that type if
    they are called using a non-`Path` data type. For example:

    .. code-block:: python

        @pathfix
        def do_something(file: Path) -> None:
            if file.exists():
                print(f"{file} exists")

        # This now works
        do_something("/tmp/foo.txt")
    """

    def inner(*args: Any, **kwargs: Any) -> Any:
        # spec = inspect.getfullargspec(func)
        # print(spec)

        sig = inspect.signature(func)
        # print(sig.parameters)
        # print(f"args in: {args}")

        _args: List[Any] = []
        for name, val in zip(sig.parameters, args):
            if sig.parameters[name].annotation == Path:
                _args.append(Path(val))
            else:
                _args.append(val)
        # print(f"args out: {_args}")

        # print(f"kwargs in: {kwargs}")
        for argname, argvalue in kwargs.items():
            if argname in sig.parameters and sig.parameters[argname].annotation == Path:
                kwargs[argname] = Path(argvalue)
        # print(f"kwargs out: {kwargs}")

        return func(*_args, **kwargs)

    return cast(TFunc, inner)


if __name__ == "__main__":
    @pathfix
    def thingie(path: Path, path2: str, int1: int, path3: Any, path4: Path, path5: Path) -> None:
        if path.exists():
            print("whuff")
        print(f"path: {type(path)}")
        print(f"path2: {type(path2)}")
        print(f"path3: {type(path3)}")
        print(f"path4: {type(path4)}")
        print(f"path5: {type(path5)}")
        print(f"int1: {type(int1)}")


    # ignore mypy/pylance errors for the following, since the whole point is to
    # test to make things do the right things when the inputs are weird/wrong
    if not TYPE_CHECKING:
        thingie("/tmp/path", 2, 14, path3="/tmp/path3", path4="/tmp/path4",
                path5=Path("/tmp/path5"))
