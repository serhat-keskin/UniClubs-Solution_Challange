from pathlib import Path
from datetime import timedelta #Some of Simple JWT’s behavior can be customized through settings variables in base.py
from google.oauth2 import service_account
import os,secrets,dotenv

my_default_hosts=["127.0.0.1", "localhost", "api.localhost", "dj.localhost","main.localhos", "pm.localhost", "dev-main.localhost", "dev-pm.localhost", "dev-api.localhost", "dev-dj.localhost" ]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), #has a shorter life span
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), #facebook gibi sitelerde sürekli login yapmamk için çok uzun tutulur  #pm sayfası için bu ayar değiştirilmeli, KISA OLMALI #TODO
    'ROTATE_REFRESH_TOKENS': True,#true oldugunda /refresh isteği attığımızda acces token'a ek olarak yeni bir refresh token verir böylece user sitede aktif olduğu sürece yenilenir yani refresh token life time'ı sürekli yenilenir süreden düşmez 
    'BLACKLIST_AFTER_ROTATION': True,# true olduğunda yenilenen refresh token dışındaki tokenı(eski tokeni) blackliste alır 
    # setting is set to True, You need to add 'rest_framework_simplejwt.token_blacklist', to your INSTALLED_APPS in the settings file to use this setting.
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'   ## gereksiz primary key uyarısı vermemesi için

# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'app_base.User'  # Django'ya hangi user modelini authenticate için kullanmasını söylüyoruz 

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

# region Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'tr-TR'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('tr', 'Türkçe'),
    ('en', 'English')
]

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

# endregion Internationalization

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'   ## burada templates klasörüne nasıl ulaşacağını,pathini tanımladık
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [ 
    ## !! LOCALDEKİ BU KONUMLARA BAKIP BURADAN BULDUĞU DOSYALARI SERVE EDİYOR
    ## !! DEFAULT STATIC FILELARIN DIŞINDA TOPLAMAK İSTEDİĞİN DIRECTORYLERI BURADAN AYARLIYORSUN (diretoylerin adının static vs olması şart değil)
    BASE_DIR / 'app_base' / 'static_files', ## Burada kendimiz oluşturduğumuz static dosyalarımızın olduğu dir'i tanımladık
    BASE_DIR / 'app_portfolio' / 'static_files', ## Burada app_portfolio uygulamasının static dosyalarının olduğu dir'i tanımladık
    BASE_DIR / 'app_benchmarks_and_tests' / 'static_files', ## Burada app_benchmarks_and_tests uygulamasının static dosyalarının olduğu dir'i tanımladık
    # BASE_DIR / 'istedigin/path',
    # BASE_DIR / 'istediğin/path2',
]  ## burada static klasörüne nasıl ulaşacağını,pathini tanımladık

print( f"\n### BASE_DIR is: {BASE_DIR} ###\n"
        "\n#### TEMPLATES are... ####\n")
for i, path in enumerate(TEMPLATES):
    print(f"# {i}.TEMPLATE is: {path}##\n")

print( "###################################################################################\n"
    "##########################   BASE ayarları yüklendi !!!  ##########################\n"
    "###################################################################################\n")