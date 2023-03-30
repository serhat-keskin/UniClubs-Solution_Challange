#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv



def main():
    print(
        "############################################################\n"
        "CHOOSE THE WORKING ENVIRONMENT\n"
        "OPTIONS: manage_dev.py, manage_local.py, manage_prod.py\n"
        "############################################################\n"
        "SAMPLE USAGE: python manage_dev.py runserver\n"
        "############################################################\n"
        )
    return
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.confs.settings.<yoursettings>') #settings flagini vermezsek otomatik olarak buradan geleni kullanıyor
    try:
        print("### test1")
        from django.core.management import execute_from_command_line
        print("### test2")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    print("## manage.py main fonksiyonu bitti (server durdurulduğunda tetiklenir)")


if __name__ == '__main__':
    main()
