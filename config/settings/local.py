from .base import *  # noqa: F403,F401

DEBUG = True
ALLOWED_HOSTS = csv_env('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,consult-notes.akshajs.org')
if 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')
if 'consult-notes.akshajs.org' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('consult-notes.akshajs.org')

CSRF_TRUSTED_ORIGINS = csv_env('DJANGO_CSRF_TRUSTED_ORIGINS', 'https://consult-notes.akshajs.org')
if 'https://consult-notes.akshajs.org' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append('https://consult-notes.akshajs.org')
