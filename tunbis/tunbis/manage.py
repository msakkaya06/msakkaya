import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tunbis.settings')
    print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))  # DJANGO_SETTINGS_MODULE'in değerini kontrol etmek için
    try:
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print("sys.argv:", sys.argv)  # sys.argv'nin değerini kontrol etmek için
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
