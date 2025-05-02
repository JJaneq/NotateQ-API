from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

def send_activation_email(user, request):
    print("Sending activation email...")
    domain = request.get_host()
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f'http://{domain}/activate/{uid}/{token}/'
    print(f"uid wygenerowane: {uid}")
    print(f"token wygenerowany: {token}")
    print(f"link: {activation_link}")
    send_mail(
        'Activation link',
        'Click the link to activate your account: ' + activation_link,
        settings.EMAIL_HOST_USER,
        [user.email],
    )