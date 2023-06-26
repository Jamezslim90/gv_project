from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU_APP:
    DEBUG = True
    
if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["127.0.0.1", "gv-platform.herokuapp.com"]
   
else:
    ALLOWED_HOSTS = ["*", "gvproject.up.railway.app"]



# Application definition

INSTALLED_APPS = [
    
    # 'jazzmin',
    'daphne',
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third Party Apps
    'smart_selects',
    'django_celery_results',
    'django_celery_beat',
    'django_extensions',
    'channels',
    'cloudinary',
    
    # 'multiselectfield',
    'taggit',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_comments_xtd',
    'django_comments',
    'easy_thumbnails',
    'django_ckeditor_5',
    'django_social_share',
    'imagekit',
    #'storages',
      
    #Local Apps
    "pages.apps.PagesConfig",
    "accounts.apps.AccountsConfig",
    "doctors.apps.DoctorsConfig",
    "service.apps.ServiceConfig",
    "blog.apps.BlogConfig",
    "marketplace.apps.MarketplaceConfig",
    "orders.apps.OrdersConfig",
    "clients.apps.ClientsConfig",
    "vaccinations.apps.VaccinationsConfig",
    "laboratories.apps.LaboratoriesConfig",
    "notifications.apps.NotificationsConfig",
    "chatapp"
   
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
                # 'accounts.context_processors.get_google_api',
                'marketplace.context_processors.get_cart_counter',
                'marketplace.context_processors.get_cart_amounts',
                'doctors.context_processors.docnotifications',
                'clients.context_processors.get_notification',
                'clients.context_processors.cusnotifications'
            ],
        },
    },
]

WSGI_APPLICATION = 'gv_project.wsgi.application'
ASGI_APPLICATION=  'gv_project.asgi.application'


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


# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=600)
# #DATABASES['default'] = dj_database_url.config(default='postgres://...'}
# DATABASES['default'].update(db_from_env)
# AUTH_USER_MODEL = 'accounts.User'


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

USE_L10N = False

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

# STORAGES = {
    
#     # Enable WhiteNoise's GZip and Brotli compression of static assets:
#     # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
#     },
# }


WHITENOISE_KEEP_ONLY_HASHED_FILES = False
WHITENOISE_MANIFEST_STRICT = False


MEDIA_URL = '/media/' # new
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # new
STATICFILES_STORAGE = (
    "django_forgiving_collecstatic.storages.ForgivingManifestStaticFilesStorage"
)

#STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'


# Flash messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

CRISPY_TEMPLATE_PACK = "bootstrap5"
# CRISPY_TEMPLATE_PACK = 'uni_form'

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'


# Celery settings
CELERY_BROKER_URL = os.environ['REDIS_URL']
#CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "Africa/Lagos"
CELERY_TASK_TRACK_STARTED = True
#CELERY_TASK_TIME_LIMIT = 30 * 60

CACHES = {
    
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}   

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CSRF_TRUSTED_ORIGINS = ['https://.*','https://gv-platform.herokuapp.com','https://127.0.0.1', 'https://gvproject.up.railway.app']




# channels settings

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


#Email settings

#EMAIL_BACKEND= 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EHU")
EMAIL_HOST_PASSWORD = config("EHP")
DEFAULT_FROM_EMAIL = config("DFE")
DEFAULT_FROM_EMAIL = 'GetVet Platform  <getvetplatform@gmail.com>'
#EMAIL_TIMEOUT = 120


DATE_INPUT_FORMATS = [
    
    "%Y-%m-%d",  # '2006-10-25'
]

TIME_INPUT_FORMATS = [
    "%H:%M:%S",  # '14:30:59'
   
]

#GOOGLE_API_KEY=config("GOOGLE_AK")
#FLUTTERWAVE_PK=config("Flutterwave_public_key")


PAYSTACK_PK= config("Paystack_public_key")
MONNIFY_PK= config("Monnify_public_key")

#AWS Credentials    

# AWS_ACCESS_KEY_ID = config('AKID')
# AWS_SECRET_ACCESS_KEY = config('SAK')
# AWS_STORAGE_BUCKET_NAME = ('SBN')
# AWS_S3_SIGNATURE_NAME = 's3v4',
# AWS_S3_REGION_NAME = config('S3RN')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL =  'public-read'
# AWS_LOCATION = 'static'
# AWS_MEDIA_LOCATION = 'media'

# #AWS_S3_CUSTOM_DOMAIN = 'https://dztglolvroaqv.cloudfront.net' #gvproject
# AWS_S3_CUSTOM_DOMAIN = "https://d1iqb74dkfltx9.cloudfront.net"

# STATIC_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_S3_VERITY = True
# #DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}}
# # STORAGES = {"staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}}


# Cloudinary Config Setting
#Account jamezslim90@gmail.com
CLOUDINARY_STORAGE = {
    
    'CLOUD_NAME': 'dz1ms5vxu',
    'API_KEY': '478289689677965',
    'API_SECRET': 'cmNVNBip6BfuNCW9TMz8Fq3dk-4',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

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

# Easy Thumbnail

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (200, 200), 'crop': True},
    },
}


#Django-Jet

JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

DATE_FORMAT = "d/m/Y"
# JAZZMIN_SETTINGS = {

#         "site_title": "GetVet Platform",
#         "site_header": "GetVet",
#         "site_brand": "GetVet Admin",
#         #"site_logo": "assets/img/brand/dark.svg",
#         #"login_logo": "assets/img/brand/dark.svg",
#         #"site_icon": "assets/img/brand/dark.svg",
#          # Welcome text on the login screen
#         "welcome_sign": "Welcome to GetVet ",
#         # Copyright on the footer
#         "copyright": "GetVet Ltd",

#         # The model admin to search from the search bar, search bar omitted if excluded
#         "search_model": "auth.User",


# }


