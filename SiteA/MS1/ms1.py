import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ms1_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # If no management args are provided, default to running the dev server
    # on port 5051. Otherwise pass through supplied args so commands like
    # `migrate` work as expected.
    args = sys.argv
    if len(args) == 1:
        args = [args[0], 'runserver', '0.0.0.0:5051', '--noreload']
    execute_from_command_line(args)

if __name__ == '__main__':
    main()