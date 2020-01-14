"""
WSGI config for PixivProxy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from os.path import join,dirname,abspath 
import sys
        
PROJECT_DIR = dirname(dirname(abspath(__file__)))   
sys.path.insert(0,PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PixivProxy.settings')

application = get_wsgi_application()
