from django.utils.translation import gettext_lazy as _

GENDER_MEN: str = 'men'
GENDER_WOMEN: str = 'women'
DEFAULT_ERROR_MESSAGES = {
    'invalid_email': {'email': _("Пользователь с такой электронной почтой не существует.")},
    'invalid_password': {
        'password': _('Пожалуйста, введите правильный пароль. Обратите внимание, что пароль чувствителен к регистру.')
    },
    'inactive': {'is_active': _("Ваша учетная запись находится на рассмотрении.")},
    'invalid_password_confirm': {'password_confirm': _("Пароли не совпадают")},
    'invalid_activated_code': {'activated_code': _('Разовый код недействительно.')},
    'no_activated_code': {'activated_code': _('Такой разовый код не найдено.')},
}