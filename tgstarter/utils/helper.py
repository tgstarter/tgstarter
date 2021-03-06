from typing import (
    Any,
    List,
    Callable,
    Optional,
    Union,
    Dict,
)
import enum
from enum import Enum
from textwrap import dedent

from lxml import html
import jinja2
from aiogram import types


auto: Callable[..., Enum] = enum.auto


def delete_indentation(text: str) -> str:
    text = dedent(text)
    if (text[0], text[-1]) == ('\n', '\n'):
        return text[1:-1]
    else:
        return text


def clear_text(source: str) -> str:
    element = html.fromstring(source)
    return element.text_content()


def string_fits(source: str, max_length: int = 4096) -> bool:
    text = clear_text(source)
    return len(text) <= max_length


def user_fullname(first_name: str, last_name: Optional[str] = None) -> str:
    if not last_name:
        return first_name
    else:
        return f'{first_name} {last_name}'


def function_fullname(function: Callable) -> str:
    return f'{function.__module__}.{function.__name__}'


def get_template_function(jinja2_env: jinja2.Environment) -> Callable[[str], jinja2.Template]:
    def template(source: str) -> jinja2.Template:
        return jinja2_env.from_string(source=dedent(source))

    return template


def button_from_source(button: Union[str, Dict[str, Any]]) -> types.KeyboardButton:
    if isinstance(button, str):
        return types.KeyboardButton(text=button)
    elif isinstance(button, types.KeyboardButton):
        return button
    else:
        assert False


def ReplyKeyboardMarkup(
    *source: Union[
        str,
        types.KeyboardButton,
        List[Union[str, types.KeyboardButton]]
    ],
    resize_keyboard: bool = True,
    **kwargs: Any
) -> types.ReplyKeyboardMarkup:
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, **kwargs)
    for item in source:
        if isinstance(item, list):
            reply_markup.row(
                *[
                    button_from_source(button) for button in item
                ]
            )
        else:
            reply_markup.add(button_from_source(item))

    return reply_markup


def InlineKeyboardMarkup(
    *source: Union[types.InlineKeyboardButton, List[types.InlineKeyboardButton]],
    **kwargs: Any
) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup(**kwargs)
    for item in source:
        if isinstance(item, list):
            inline_keyboard.row(*item)
        elif isinstance(item, types.InlineKeyboardButton):
            inline_keyboard.add(item)
        else:
            assert False

    return inline_keyboard


class Item:
    def __init__(self, value: Any = None) -> None:
        self._value = value

    def __get__(self, instance: Any, owner: Any) -> str:
        return self._value or ''

    def __set_name__(self, owner: Any, name: str) -> None:
        if self._value is None:
            self._value = name


class NamedEnum(Enum):

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[Any]) -> str:
        return name


class FlagEnum(NamedEnum):
    def __str__(self) -> str:
        return str(self.value)
