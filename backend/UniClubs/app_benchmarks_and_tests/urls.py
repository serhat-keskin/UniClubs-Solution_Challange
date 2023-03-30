from django.conf import settings #settings.py dosyasını import ediyoruz
from django.urls import path,include
from benchs.urls import urlpatterns as bench_urls
from tests.urls import urlpatterns as test_urls

from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('test/', include('benchmarks_and_tests.tests.urls')),
    path('bench/', include('benchmarks_and_tests.benchs.urls')),
]

# urlpatterns = i18n_patterns(  ##TODO BUNA GEREK YOK, EMİN OLDUKTAN SONRA DİĞER DOSYALARDAN DA KALDIR
#     path('test/', include('benchmarks_and_tests.tests.urls')),
#     path('bench/', include('benchmarks_and_tests.benchs.urls')),
# )

# region TEMPLATES FOR ENVIRONMENTS

# if settings.CURRENT_ENVIRONMENT in ["LOCAL"]:
#     urlpatterns += [
#         
#     ]

# if settings.CURRENT_ENVIRONMENT in ["DEV"]:
#     urlpatterns += [
#      
#     ]

# if settings.CURRENT_ENVIRONMENT in ["LOCAL", "DEV"]:
#     urlpatterns += [
#         
#     ]

# if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:
#     urlpatterns += [
#
#     ]

# endregion TEMPLATES FOR ENVIRONMENTS