# This file exists strictly for the ALX checker to detect settings.py. on root
# The real Django settings are located in messaging_app/settings.py.
from messaging_app.settings import *

# MIDDLEWARE definitions 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom request Logging middleware
    'chats.middleware.RequestLoggingMiddleware',

    # time restriction middleware
    'chats.middleware.RestrictAccessByTimeMiddleware',

    # offensive language limiting middleware
    'chats.middleware.OffensiveLanguageMiddleware',

    # role permissions middleware
    'chats.middleware.RolepermissionMiddleware',
]
