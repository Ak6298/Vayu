import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vayu_brahman.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com'}
)
user.set_password('1234')
user.save()

print('created_or_updated=', created)
print('username=', user.username)
print('password_ok=', user.check_password('1234'))
