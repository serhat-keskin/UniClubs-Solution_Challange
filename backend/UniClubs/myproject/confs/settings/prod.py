from .base import *

print(
    "###################################################################################\n"
    "##########################  PROD ayarları yükleniyor...  ##########################\n"
    "###################################################################################\n"
    )

CURRENT_ENVIRONMENT = "PROD"

print("### .env.prod yükleniyor...")
dotenv.read_dotenv(os.path.join(BASE_DIR, '.env.prod'))
print("### .env.prod yüklendi!!!\n")

DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_base.apps.AppBaseConfig', 
    'app_portfolio.apps.AppPortfolioConfig',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    'django_extensions',
    'simple_history',
    'drf_spectacular'
]

MIDDLEWARE = [
    'simple_history.middleware.HistoryRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',  ##olabildiğince yukarıda olmalı çünkü bu sıralamanın önemi var sıralamaya göre çalışıyor
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #locale middleware, taraycının dil tercihlerini alıyor.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = os.environ['PROD_ALLOWED_HOSTS'].split(',')
ALLOWED_HOSTS.extend(my_default_hosts)
print("#### ALLOWED_HOSTS are... ####\n")
for i, host in enumerate(ALLOWED_HOSTS):
    print(f"# {i}.ALLOWED_HOST is: {host}##")
print("\n#### ALLOWED_HOSTS end... ####\n")

INTERNAL_IPS = [
    "127.0.0.1"
]
# region SECURITY ETC

SECRET_KEY = secrets.token_urlsafe(50)   

# region CORS

# CORS_ALLOWED_ORIGINS=
# CORS_ALLOWED_ORIGIN_REGEXES=
CORS_ALLOW_ALL_ORIGINS=False

# endregion CORS

CSRF_COOKIE_SECURE = True #to avoid transmitting the CSRF cookie over HTTP accidentally. ## HTTPS olmak zorunda yoksa hata verir. HTTP kullanıyorsan False yap.
SESSION_COOKIE_SECURE = True #to avoid transmitting the session cookie over HTTP accidentally. ## aynı şekilde HTTPS olmak zorunda yoksa hata verir. HTTP kullanıyorsan False yap.
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False ### True yapmayı unutma #TODO 

SECURE_HSTS_SECONDS = 86400  # 1 day
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# endregion

X_FRAME_OPTIONS = 'DENY' # iframe kullanımını engeller

# region Database
DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['PROD_DB_NAME'],
        'USER': os.environ['PROD_DB_USER'],
        'PASSWORD': os.environ['PROD_DB_PASSWORD'],
        'HOST': os.environ['PROD_DB_HOST'],
    }
}
# endregion Database

# region Bucket Storage

MY_CREDENTIALS_PATH=os.path.join(BASE_DIR, os.environ['PROD_CREDENTIALS_PATH'])

GS_BUCKET_NAME = os.environ['PROD_BUCKET_NAME']
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(MY_CREDENTIALS_PATH)
GS_FILE_OVERWRITE=True
GS_MAX_MEMORY_SIZE=1048576
GS_EXPIRATION=timedelta(seconds=86400)

# STATIC_ROOT = "deneme"
# MEDIA_ROOT ="deneme"
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/' #default staticfiles uygulaması hata vermesin diye ekledim ###! AYRICA NUCKET ADRESİNİN NEREDEN BAŞLAYACAĞINI BELİRTİYOR
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/' ###! BUCKET ADRESİNİN NEREDEN BAŞLAYACAĞINI BELİRTİYOR

# Set "static" folder #gcs_utils dosyasında tanımladığım bucket pathlerini kullanmasını sağlıyoruz
STATICFILES_STORAGE = 'myproject.confs.gcs_utils.Static'
print("## STATICFILES_STORAGE: ",STATICFILES_STORAGE)
# Set "media" folder #gcs_utils dosyasında tanımladığım bucket pathlerini kullanmasını sağlıyoruz
DEFAULT_FILE_STORAGE = 'myproject.confs.gcs_utils.Media'
print("## DEFAULT_FILE_STORAGE: ",DEFAULT_FILE_STORAGE)

# endregion Bucket Storage

# region Email
EMAIL_HOST = str(os.environ["PROD_EMAIL_HOST"])
EMAIL_HOST_USER= str(os.environ["PROD_EMAIL_HOST_USER"])
EMAIL_HOST_PASSWORD= str(os.environ["PROD_EMAIL_HOST_PASS"])
EMAIL_PORT = int(os.environ["PROD_EMAIL_PORT"])
EMAIL_USE_SSL = True
# endregion Email

WSGI_APPLICATION = 'myproject.confs.wsgi.prod.application'

SPECTACULAR_SETTINGS = {
    "TITLE": "UniClubs",
    "DESCRIPTION": "Platform with unique features for all Clubs",
    "VERSION": "0.6.1",
}

print(
    "\n###################################################################################\n"
    "##########################   PROD ayarları yüklendi !!!  ##########################\n"
    "###################################################################################\n\n"
    )
