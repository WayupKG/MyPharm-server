from .translite import get_english_translit as translit


def avatar_img(instance, filename: str) -> str:
    _translit = translit(instance.get_full_name())
    _filename: str = f'{_translit}.{filename.split(".")[-1]}'
    return f'users/{_translit}/avatars/{_filename}'


def company_logo_img(instance, filename: str) -> str:
    _filename: str = f'logo.{filename.split(".")[-1]}'
    return f'companies/{translit(instance.title)}/{_filename}'


def company_contract_file(instance, filename: str) -> str:
    _translit = translit(instance.title)
    _filename: str = f'{_translit}.{filename.split(".")[-1]}'
    return f'companies/{_translit}/contract/{_filename}'


def medicine_img(instance, filename: str) -> str:
    _filename: str = f'{translit(instance.title)}.{filename.split(".")[-1]}'
    return f'medicines/{translit(instance.category.title)}/{_filename}'
