import django
import os
from django.core.mail import send_mail


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adoptme.settings')  # Replace with your project name
django.setup()


def test_email() :
    print("executed")
    try : 
        send_mail(
            'Test Subject',
            'this is a test email',
            'admin@fetishia.store',
            ['danielrichardo103@gmail.com'],
            fail_silently=False
        )
        print("email berhasil dikirim")
    except:
        print("email gagal dikirim")

if __name__ == '__main__':
    test_email()