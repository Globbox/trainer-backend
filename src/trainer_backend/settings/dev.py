from .base import *  # noqa F403


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR.parent.parent, 'mail')
