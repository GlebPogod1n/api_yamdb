from django.core.mail import send_mail

from api_yamdb.settings import EMAIL


def send_code(email, confirmation_code):
    """Oтправляем код на почту пользователя."""

    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )
