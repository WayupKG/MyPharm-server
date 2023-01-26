from .translite import get_english_translit as translit


def avatar_img(instance, filename: str) -> str:
    _filename: str = f'{translit(instance.get_full_name())}.{filename.split(".")[-1]}'
    return f'users/avatars/{_filename}'
