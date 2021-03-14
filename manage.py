#!/usr/bin/env python
# Stdlib:
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    current_path = Path(__file__).parent.resolve()
    settings_path = current_path / "config" / "settings"
    if not settings_path.exists():
        raise NotImplementedError
    local_settings = settings_path / "local_development.py"
    if local_settings.exists() and local_settings.is_file():
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "config.settings.local_development"
        )
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # grab_money directory.
    sys.path.append(str(current_path / "grab_money"))

    execute_from_command_line(sys.argv)
