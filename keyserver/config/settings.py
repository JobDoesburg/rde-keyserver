import os
from os import path
from pathlib import Path

import saml2
from saml2 import xmldsig
from saml2 import saml

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")

BASE_URL = os.environ.get("DJANGO_BASE_URL")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "djangosaml2",
    "qr_code",
    "config",
    "keyserver",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosaml2.middleware.SamlSessionMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR.parent / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# SAML2
SAML_SESSION_COOKIE_NAME = "saml_session"
SESSION_COOKIE_SECURE = not DEBUG
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)
LOGIN_URL = "/saml/login/"
LOGOUT_REDIRECT_URL = "/saml/login/"
LOGIN_REDIRECT_URL = "/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SAML_USE_NAME_ID_AS_USERNAME = True
SAML_ATTRIBUTE_MAPPING = {
    "eduPersonTargetedID": ("username",),
    "mail": ("email",),
    "givenName": ("first_name",),
    "sn": ("last_name",),
}
SAML_CONFIG = {
    "xmlsec_binary": "/usr/bin/xmlsec1",
    "entityid": BASE_URL,
    "allow_unknown_attributes": True,
    "service": {
        "sp": {
            "name": "SURF RDE KeyServer POC",
            "name_id_format": saml.NAMEID_FORMAT_PERSISTENT,
            "endpoints": {
                "assertion_consumer_service": [
                    (f"{BASE_URL}/saml/acs/", saml2.BINDING_HTTP_POST),
                ],
                "single_logout_service": [
                    (f"{BASE_URL}/saml/ls/", saml2.BINDING_HTTP_REDIRECT),
                    (f"{BASE_URL}/saml/ls/post", saml2.BINDING_HTTP_POST),
                ],
            },
            "signing_algorithm": xmldsig.SIG_RSA_SHA256,
            "digest_algorithm": xmldsig.DIGEST_SHA256,
            "force_authn": False,
            "name_id_format_allow_create": True,
            "required_attributes": ["eduPersonTargetedID", "givenName", "sn", "mail"],
            "want_response_signed": False,
            "want_assertions_signed": True,
            "allow_unsolicited": True,
        },
    },
    "metadata": {
        "remote": [
            {
                "url": os.environ.get("DJANGO_SAML_IDP_METADATA_URL"),
            },
        ],
    },
    "debug": 1 if DEBUG else 0,
    "key_file": path.join(BASE_DIR, "config", "saml", "private.key"),
    "cert_file": path.join(BASE_DIR, "config", "saml", "public.cert"),
    "encryption_keypairs": [
        {
            "key_file": path.join(BASE_DIR, "config", "saml", "private.key"),
            "cert_file": path.join(BASE_DIR, "config", "saml", "public.cert"),
        }
    ],
    "contact_person": [
        {
            "given_name": "Job",
            "sur_name": "Doesburg",
            "company": "SURF",
            "email_address": "job.doesburg@surf.nl",
            "contact_type": "technical",
        },
        {
            "given_name": "Job",
            "sur_name": "Doesburg",
            "company": "SURF",
            "email_address": "job.doesburg@surf.nl",
            "contact_type": "administrative",
        },
    ],
    "organization": {
        "name": [("SURF RDE KeyServer POC", "nl"), ("SURF RDE KeyServer POC", "en")],
        "display_name": [
            ("SURF RDE KeyServer POC", "nl"),
            ("SURF RDE KeyServer POC", "en"),
        ],
        "url": [
            (BASE_URL, "nl"),
            (BASE_URL, "en"),
        ],
    },
}
