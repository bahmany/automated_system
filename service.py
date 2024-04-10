#!/usr/bin/env python
import os
import os.path
import sys
import win32serviceutil

# This is my base path
base_path = os.path.dirname(os.path.abspath(__file__))
if not base_path in sys.path:
    sys.path.append(base_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsp.settings")
    
from django_windows_tools.service import DjangoService,test_commands

class Service(DjangoService):

    _base_path = base_path
    _svc_name_ = "django-rahsoon-service"
    _svc_display_name_ = "Django rahsoon background service"
    _config_filename = "service.ini"


if __name__ == "__main__":    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_commands(base_path)
    else:
        win32serviceutil.HandleCommandLine(Service)
