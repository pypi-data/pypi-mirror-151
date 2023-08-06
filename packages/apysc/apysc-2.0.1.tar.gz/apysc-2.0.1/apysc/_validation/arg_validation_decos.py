"""This module is for the argument validations' decorators.

Mainly the following decorators exist.

- not_empty_string
    - Set the validation to check that a specified argument's string
        is not empty.
- handler_args_num
    - Set the validation to check a specified handler argument's
        number.
- handler_options_type
    - Set the validation to check a specified handler-options
        argument's type.
- is_integer
    - Set the validation to check a specified argument's type
        is the `int` or `ap.Int`.
- num_is_gt_zero
    - Set the validation to check that a specified argument's value
        is greater than zero.
- is_easing
    - Set the validation to check a specified argument's type
        is the `ap.Easing`.
"""

import functools
import inspect
from inspect import Signature
from typing import Any
from typing import Callable
from typing import Dict
from typing import TypeVar

# pyright: reportInvalidTypeVarUse=false
_F = TypeVar('_F', bound=Callable)


def _extract_arg_value(
        *, args: Any, kwargs: Dict[str, Any],
        arg_position_index: int, arg_name: str,
        default_val: Any) -> Any:
    """
    Extract an argument value from a specified arguments' dictionary
    or list.

    Parameters
    ----------
    args : List[Any]
        A specified positional arguments' list.
    kwargs : Dict[str, Any]
        A specified keyword arguments' dictionary.'
    arg_position_index : int
        A target argument position index.
    arg_name : str
        A target argument name to check.
    default_val : Any
        A default value of a target argument.

    Returns
    -------
    value : Any
        An extracted any value.
    """
    value: Any = None
    if arg_name in kwargs:
        value = kwargs[arg_name]
    elif len(args) - 1 >= arg_position_index:
        value = args[arg_position_index]
    if value is None and default_val is not None:
        return default_val
    return value


def _get_arg_name_by_index(
        *, callable_: Callable, arg_position_index: int) -> str:
    """
    Get an argument name from a specified argument position index.

    Parameters
    ----------
    callable_ : Callable
        A target function or method.
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    arg_name : str
        A target argument name.
    """
    signature: Signature = inspect.signature(callable_)
    if len(signature.parameters) - 1 < arg_position_index:
        raise IndexError(
            'A specified function has no argument parameter '
            f'at the index of {arg_position_index}'
            f'\nActual argument length: {len(signature.parameters)}')
    arg_name: str = ''
    for i, (arg_name_, _) in enumerate(signature.parameters.items()):
        if i == arg_position_index:
            arg_name = arg_name_
    return arg_name


def _get_callable_and_arg_names_msg(
        *, callable_: Callable, arg_name: str) -> str:
    """
    Get a function or method and argument names' message
    for an additional error message.

    Parameters
    ----------
    callable_ : Callable
        A target function or method.
    arg_name : str
        A target argument name.

    Returns
    -------
    callable_and_arg_names_msg : str
        A function or method and argument names' message.
    """
    callable_and_arg_names_msg: str = (
        f'Target callable name: {callable_.__name__}'
        f'\nTarget argument name: {arg_name}'
    )
    return callable_and_arg_names_msg


def _get_default_val_by_arg_name(
        *, callable_: Callable, arg_name: str) -> Any:
    """
    Get a default value of a given name's argument.

    Parameters
    ----------
    callable_ : Callable
        A target function or method.
    arg_name : str
        A target argument name.

    Returns
    -------
    default_val : Any
        A default value of a given name's argument.
    """
    default_val: Any = None
    signature: Signature = inspect.signature(callable_)
    for target_arg_name, parameter in signature.parameters.items():
        if target_arg_name != arg_name:
            continue
        default_val = parameter.default
        break
    if default_val == inspect.Signature.empty:
        return None
    return default_val


def not_empty_string(*, arg_position_index: int) -> _F:
    """
    Set the validation to check that a specified argument's string
    is not empty.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            from apysc._validation.string_validation import \
                validate_not_empty_string
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            string: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index, arg_name=arg_name,
                default_val=default_val)

            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            validate_not_empty_string(
                string=string,
                additional_err_msg=(
                    'An argument\'s string value must not be empty.'
                    f'\n{callable_and_arg_names_msg}'
                ))
            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore


def handler_args_num(*, arg_position_index: int) -> _F:
    """
    Set the validation to check a specified handler argument's
    number.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            from apysc._validation.handler_validation import \
                validate_handler_args_num
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            handler: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index,
                arg_name=arg_name, default_val=default_val)
            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            validate_handler_args_num(
                handler=handler,
                additional_err_msg=callable_and_arg_names_msg)
            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore


def handler_options_type(*, arg_position_index: int) -> _F:
    """
    Set the validation to check a specified handler-options
    argument's type.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            from apysc._validation.handler_validation import \
                validate_options_type
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            options: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index, arg_name=arg_name,
                default_val=default_val)
            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            validate_options_type(
                options=options,
                additional_err_msg=callable_and_arg_names_msg)

            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore


def is_integer(*, arg_position_index: int) -> _F:
    """
    Set the validation to check a specified argument's type
    is the `int` or `ap.Int`.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            from apysc._validation.number_validation import validate_integer
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            integer: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index, arg_name=arg_name,
                default_val=default_val)

            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            validate_integer(
                integer=integer,
                additional_err_msg=callable_and_arg_names_msg)

            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore


def num_is_gt_zero(*, arg_position_index: int) -> _F:
    """
    Set the validation to check that a specified argument's value
    is greater than zero.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            from apysc._validation.number_validation import \
                validate_num_is_gt_zero
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            num: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index, arg_name=arg_name,
                default_val=default_val)

            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            validate_num_is_gt_zero(
                num=num, additional_err_msg=callable_and_arg_names_msg)

            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore


def is_easing(*, arg_position_index: int) -> _F:
    """
    Set the validation to check a specified argument's type
    is the `ap.Easing`.

    Parameters
    ----------
    arg_position_index : int
        A target argument position index.

    Returns
    -------
    _wrapped : Callable
        Wrapped callable object.
    """

    def wrapped(callable_: _F) -> _F:
        """
        Wrapping function for a decorator setting.

        Parameters
        ----------
        callable_ : Callable
            A target function or method to wrap.

        Returns
        -------
        inner_wrapped : Callable
            Wrapped callable object.
        """

        @functools.wraps(callable_)
        def inner_wrapped(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapping function for a decorator setting.

            Parameters
            ----------
            *args : list
                Target positional arguments.
            **kwargs : dict
                Target keyword arguments.

            Returns
            -------
            result : Any
                A return value(s) of a callable execution result.
            """
            import apysc as ap
            arg_name: str = _get_arg_name_by_index(
                callable_=callable_, arg_position_index=arg_position_index)
            default_val: Any = _get_default_val_by_arg_name(
                callable_=callable_, arg_name=arg_name)
            easing: Any = _extract_arg_value(
                args=args, kwargs=kwargs,
                arg_position_index=arg_position_index,
                arg_name=arg_name, default_val=default_val)

            callable_and_arg_names_msg: str = _get_callable_and_arg_names_msg(
                callable_=callable_, arg_name=arg_name)
            if not isinstance(easing, ap.Easing):
                raise TypeError(
                    'A specified easing argument\'s type is not the '
                    f'ap.Easing: {type(easing)}'
                    f'\n{callable_and_arg_names_msg}')

            result: Any = callable_(*args, **kwargs)
            return result

        return inner_wrapped  # type: ignore

    return wrapped  # type: ignore
