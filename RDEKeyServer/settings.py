from os import path

import saml2
import saml2.saml

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nta2^r4xet@@6r#*ue*%a8(4v2&_2%&6%xe1euxm_(lx1#zay^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

BASE_URL = "http://localhost:8000"

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
    "RDEDocuments",
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

ROOT_URLCONF = "RDEKeyServer.urls"

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

WSGI_APPLICATION = "RDEKeyServer.wsgi.application"


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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# SAML2
SAML_SESSION_COOKIE_NAME = "saml_session"
SESSION_COOKIE_SECURE = False  # False for development
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)
LOGIN_URL = "/saml/login/"
LOGOUT_REDIRECT_URL = "/saml/login/"
LOGIN_REDIRECT_URL = "/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SAML_USE_NAME_ID_AS_USERNAME = True
BASEDIR = path.dirname(path.abspath(__file__))
SAML_ATTRIBUTE_MAPPING = {
    "uid": ("username",),
    "mail": ("email",),
    "givenName": ("first_name",),
    "sn": ("last_name",),
}
SAML_CONFIG = {
    "xmlsec_binary": "/usr/local/bin/xmlsec1",
    "entityid": "http://localhost:8000/saml/metadata/",
    "allow_unknown_attributes": True,
    "service": {
        "sp": {
            "name": "SURF RDE KeyServer POC",
            "name_id_format": saml2.saml.NAMEID_FORMAT_TRANSIENT,
            "endpoints": {
                "assertion_consumer_service": [
                    ("http://localhost:8000/saml/acs/", saml2.BINDING_HTTP_POST),
                ],
                "single_logout_service": [
                    ("http://localhost:8000/saml/ls/", saml2.BINDING_HTTP_REDIRECT),
                    ("http://localhost:8000/saml/ls/post", saml2.BINDING_HTTP_POST),
                ],
            },
            "signing_algorithm": saml2.xmldsig.SIG_RSA_SHA256,
            "digest_algorithm": saml2.xmldsig.DIGEST_SHA256,
            "force_authn": False,
            "name_id_format_allow_create": True,
            "required_attributes": ["uid", "givenName", "sn", "mail"],
            # "optional_attributes": ["eduPersonAffiliation"],
            "want_response_signed": True,
            "authn_requests_signed": True,
            "logout_requests_signed": True,
            "want_assertions_signed": True,
            "only_use_keys_in_metadata": True,
            "allow_unsolicited": True,
        },
    },
    "metadata": {
        "remote": [
            {"url": "https://samltest.id/saml/idp"}, # https://metadata.surfconext.nl/idp-metadata.xml
        ],
    },
    "debug": 1,
    "key_file": path.join(BASEDIR, "saml", "private.key"),
    "cert_file": path.join(BASEDIR, "saml", "public.cert"),
    "encryption_keypairs": [
        {
            "key_file": path.join(BASEDIR, "saml", "private.key"),
            "cert_file": path.join(BASEDIR, "saml", "public.cert"),
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
            ("http://localhost:8000", "nl"),
            ("http://localhost:8000", "en"),
        ],
    },
}
