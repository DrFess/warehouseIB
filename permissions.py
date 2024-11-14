from settings import ADMINS


def administrator_permissions(func):
    """Декоратор для проверки прав доступа администратора"""
    def wrapper(telegram_id, *args, **kwargs):
        if telegram_id in ADMINS:
            return func(*args, **kwargs)
        else:
            return "Вы не являетесь администратором"
    return wrapper
