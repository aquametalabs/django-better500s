from os.path import join, dirname
from django.conf import settings
import manage

BETTER_500_LOG_DIR = getattr(settings, "BETTER_500_LOG_DIR", join(dirname(manage.__file__), 'logs', 'better500s'))
BETTER_500_FROM_EMAIL = getattr(settings, "BETTER_500_FROM_EMAIL", getattr(settings, "DEFAULT_FROM_EMAIL", None))
BETTER_500_TO_EMAILS = getattr(settings, "BETTER_500_TO_EMAILS", getattr(settings, "ADMINS", None))
BETTER_500_UNCAUGHT_DIR = getattr(settings, "BETTER_500_UNCAUGHT_DIR", "UNCAUGHT")
BETTER_500_AJAX_URL = getattr(settings, "BETTER_500_AJAX_URL", "better-500-callback/")
BETTER_500_POST_URL = getattr(settings, "BETTER_500_POST_URL", "better-500-saved/")
BETTER_500_DEFAULT_RETURN_URL_NAME = getattr(settings, "BETTER_500_DEFAULT_RETURN_URL_NAME", "home")