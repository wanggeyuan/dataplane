#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataPlane.settings")
    
    # 检查参数数量是否正确
    if len(sys.argv) >= 4 and sys.argv[1] == "runserver":
        port = sys.argv[2]
        device_name = sys.argv[3]
        os.environ["DEVICE_NAME"] = device_name
        # 保持原始的runserver命令和端口参数
        execute_args = sys.argv[:3]
    else:
        print("请指定设备名称,例如: python manage.py runserver 8001 S1")
        sys.exit(1)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(execute_args)


if __name__ == "__main__":
    main()
