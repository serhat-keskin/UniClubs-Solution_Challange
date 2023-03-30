#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv



def main():
    print("## manage.py main fonksiyonu başladı")
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.confs.settings.prod') #settings flagini vermezsek otomatik olarak buradan geleni kullanıyor
    try:
        from django.core.management import execute_from_command_line
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
