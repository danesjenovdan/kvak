from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hz_13%qy^^2(e1!t#hloa3)$&6$=llxm_*)js7$tq57jg2=b(9"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Reload dev server on component file changes
COMPONENTS["reload_on_file_change"] = True


# debug toolbar settings
def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "RESULTS_CACHE_SIZE": 500,
}
