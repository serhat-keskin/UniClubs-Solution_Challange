from .base import *

print(
    "###################################################################################\n"
    "##########################  LOCAL ayarları yükleniyor...  ##########################\n"
    "###################################################################################\n"
    )
try:
    print("### .env.dev yükleniyor...") #TODO .env.local ayarlanacak
    dotenv.read_dotenv(os.path.join(BASE_DIR, '.env.dev'))
    print("### .env.dev yüklendi!!!\n")
except Exception as e:
    print("### .env.dev yüklenemedi büyük ihtimalle dosya yok veya yanlış konumda!!!")
    print("### Error: ",e)

CURRENT_ENVIRONMENT = "LOCAL"
#hata vermesin diye bucket ayarları #TODO buna çözüm bul
# MY_CREDENTIALS_PATH=os.path.join(BASE_DIR, os.environ['DEV_CREDENTIALS_PATH'])
# GS_BUCKET_NAME = os.environ['DEV_BUCKET_NAME']
# GS_CREDENTIALS = service_account.Credentials.from_service_account_file(MY_CREDENTIALS_PATH)

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_base.apps.AppBaseConfig',
    'app_portfolio.apps.AppPortfolioConfig',
    'app_benchmarks_and_tests.apps.AppBenchmarksAndTestsConfig',
 
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    'django_extensions',
    'debug_toolbar',
    'simple_history',
    'drf_spectacular'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

print("### .env.local yükleniyor...")
dotenv.read_dotenv(os.path.join(BASE_DIR, '.env.local'))
print("### .env.local yüklendi!!!")

# ALLOWED_HOSTS = ['gdscostim.pythonanywhere.com', '127.0.0.1', 'localhost', '0.0.0.0','api.localhost', 'api.uniclubs.co', 'test-api.uniclubs.co']

ALLOWED_HOSTS = os.environ.get('LOCAL_ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS.extend(my_default_hosts)
print("\n#### ALLOWED_HOSTS are... ####\n")
for i, host in enumerate(ALLOWED_HOSTS):
    print(f"# {i}.ALLOWED_HOST is: {host}##")
print("\n#### ALLOWED_HOSTS end... ####\n")
INTERNAL_IPS = [
    "127.0.0.1", #localhost internal ip
    '172.17.0.1',  # or whatever IP address your Docker bridge NETWORK uses
    '172.18.0.1', # <your docker-compose file name>(u can find this via "docker network ls") NETWORK ip ## THIS IS THE ACTUAL SOLUTION for DJDT  
    # '172.19.0.2', # <my django container> internal ip
]

# region SECURITY ETC

SECRET_KEY = secrets.token_urlsafe(50)   

# region CORS

# CORS_ALLOWED_ORIGINS=
# CORS_ALLOWED_ORIGIN_REGEXES=
CORS_ALLOW_ALL_ORIGINS=True

# endregion CORS

CSRF_COOKIE_SECURE = True #to avoid transmitting the CSRF cookie over HTTP accidentally. ## HTTPS olmak zorunda yoksa hata verir. HTTP kullanıyorsan False yap.
SESSION_COOKIE_SECURE = True #to avoid transmitting the session cookie over HTTP accidentally. ## aynı şekilde HTTPS olmak zorunda yoksa hata verir. HTTP kullanıyorsan False yap.
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False ## development için kapalı https zorunlu yapıyor

SECURE_HSTS_SECONDS = 86400  # 1 day
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# endregion

X_FRAME_OPTIONS = 'DENY' # iframe kullanımını engeller

# region Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# endregion Database

# region Static, Media (LOCAL Bucket) Storage
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

##
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'all_the_static_files' ## bildiğin local bucket, burada toplanan bütün static fileların(default ve bizim belirlediğimiz STATICFILES_DIRS içerisindeki dir'ler) hangi dir'e aktarılcağını belirledik.
## STATIC_ROOT STATICFILES_DIRS içerisindeki dir'lerin içinde bir dir'de path'de olamaz mantıken daha dış daha üst bir konumda olmalı bu yüzden bu şekilde ayarladık. 
##

##
MEDIA_URL = '/media/'  # media dosyalarının urlsi, Bunu media pathine giden bir kestirme olarak düşün

MEDIA_ROOT = BASE_DIR / 'all_the_media_files' ## bildiğin local bucket, burada kullanıcıların vs yüklediği medya dosyalarının hangi dir'e aktarılcağını,yükleneceğini ayarladık.

##
# endregion Static, Media (LOCAL Bucket) Storage

# region Email
EMAIL_HOST = str(os.environ.get("LOCAL_EMAIL_HOST"))  #os.environ yerine os.environ.get yazmamamın sebebi ile bulamazsa hata vermesin diye
EMAIL_HOST_USER= str(os.environ.get("LOCAL_EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD= str(os.environ.get("LOCAL_EMAIL_HOST_PASS"))
EMAIL_PORT = int(os.environ.get("LOCAL_EMAIL_PORT", "0"))
EMAIL_USE_SSL = True
# endregion Email
WSGI_APPLICATION = 'myproject.confs.wsgi.prod.application'

SPECTACULAR_SETTINGS = {
    "TITLE": "UniClubs",
    "DESCRIPTION": "Platform with unique features for all Clubs",
    "VERSION": "0.6.1",
}

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.timer.TimerPanel',
# ]

DISABLE_PANELS= [
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel'
]

print(
    f"##################### STATIC/MEDIA URLS,ROOTS,DIRS #####################\n"
    f"# STATIC_URL is: {STATIC_URL} ###\n"
    f"# STATIC_ROOT is: {STATIC_ROOT} ###\n" 
    f"# MEDIA_URL is: {MEDIA_URL} ###\n"
    f"# MEDIA_ROOT is: {MEDIA_ROOT} ###\n")
print("\n#### STATICFILES_DIRS are... ####\n")
for i, path in enumerate(STATICFILES_DIRS):
    print(f"# {i}.STATICFILE_DIR is: {path}###\n")
print(f"#######################################################################\n")


print(
    "###################################################################################\n"
    "##########################   LOCAL ayarları yüklendi !!!  #########################\n"
    "###################################################################################\n\n"
    )
