from pathlib import Path
import os

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third Party Apps
    
    # 'multiselectfield',
    'taggit',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_comments_xtd',
    'django_comments',
    'easy_thumbnails',
    'django_ckeditor_5',
    'django_social_share',
    
    #Local Apps
    "pages.apps.PagesConfig",
    "accounts.apps.AccountsConfig",
    "doctors.apps.DoctorsConfig",
    "service.apps.ServiceConfig",
    "blog.apps.BlogConfig",
    "marketplace.apps.MarketplaceConfig",
]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'gv_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.get_doctor',
                'accounts.context_processors.get_user_profile',
                'accounts.context_processors.get_google_api',
                'marketplace.context_processors.get_cart_counter',
                'marketplace.context_processors.get_cart_amounts',
            ],
        },
    },
]

WSGI_APPLICATION = 'gv_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }



DATABASES = {

  'default': {
  'ENGINE': "django.db.backends.postgresql",
  'NAME': config("NAME"),
  'USER': config("USER"),
  'PASSWORD': config("PASSWORD"),
  'HOST': config("HOST"),
  'PORT': '7491'
  }
 
 }

AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = '/media/' # new
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # new

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Flash messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

CRISPY_TEMPLATE_PACK = "bootstrap5"
# CRISPY_TEMPLATE_PACK = 'uni_form'

#Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EHU")
EMAIL_HOST_PASSWORD = config("EHP")
DEFAULT_FROM_EMAIL = config("DFE")
DEFAULT_FROM_EMAIL = 'GetVet Platform  <getvetplatform@gmail.com>'

GOOGLE_API_KEY="AIzaSyCOugkkY9aMPcSlNONQfWQ7mLa1KVH58E4"

JAZZMIN_SETTINGS = {

        "site_title": "GetVet Platform",
        "site_header": "GetVet",
        "site_brand": "GetVet Admin",
        #"site_logo": "assets/img/brand/dark.svg",
        #"login_logo": "assets/img/brand/dark.svg",
        #"site_icon": "assets/img/brand/dark.svg",
         # Welcome text on the login screen
        "welcome_sign": "Welcome to GetVet ",
        # Copyright on the footer
        "copyright": "GetVet Ltd",

        # The model admin to search from the search bar, search bar omitted if excluded
        "search_model": "auth.User",


}


# ckeditor Config settings

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload"
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
    },
}


#django-comments-xtd

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = False