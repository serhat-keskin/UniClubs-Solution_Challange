from django.conf import settings #settings.py dosyasını import ediyoruz
from django.urls import path
from .benchs import *

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('bench_1/', test_importing.as_view(), name='bench_1'),
    # path('bench_3/', bench_3.as_view(), name='bench_3'),
    # path('bench_4/', bench_4.as_view(), name='bench_4'),
    # path('bench_5/', bench_5.as_view(), name='bench_5'),
]

# urlpatterns = i18n_patterns(
#     path('bench_1/', test_importing.as_view(), name='bench_1'),
#     # path('bench_3/', bench_3.as_view(), name='bench_3'),
#     # path('bench_4/', bench_4.as_view(), name='bench_4'),
#     # path('bench_5/', bench_5.as_view(), name='bench_5'),
# )

if settings.CURRENT_ENVIRONMENT in ["LOCAL"]:
    urlpatterns += [
        
    ]

if settings.CURRENT_ENVIRONMENT in ["DEV"]:
    urlpatterns += [
     
    ]

if settings.CURRENT_ENVIRONMENT in ["LOCAL", "DEV"]:
    urlpatterns += [
        
    ]

if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:
    urlpatterns += [

    ]

