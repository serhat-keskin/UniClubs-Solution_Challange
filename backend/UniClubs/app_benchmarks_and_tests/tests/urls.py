from django.conf import settings #settings.py dosyasını import ediyoruz
from django.urls import path
from . import tests

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('test_1/', tests.test_static_and_media_test, name='static_and_media_test'),
    path('test_2/', tests.localization, name='localization_1'),
    path('test_3/', tests.localization_2, name='localization_2'),
    path('test_4/', tests.localization_3, name='localization_3'),
    path('test_5/', tests.dropdown_list_w_checkbox, name='dd'),
    path('test_6/', tests.dropdown_list_w_checkbox_2, name='dd2'),
    path('test_7/', tests.dropdown_list_w_checkbox_3, name='dd3'),
    path('test_8/', tests.createClub, name='a'),
    path('test_9/<str:pk>/', tests.createEvent, name='b'),
    # path('test_5/', test_5.as_view(), name='test_2'),
    # path('test_6/', test_6.as_view(), name='test_2'),
    # path('test_7/', test_7.as_view(), name='test_2'),
    # path('test_8/', test_8.as_view(), name='test_2'), 
]

# urlpatterns = i18n_patterns(
#     path('test_4/', testTemplateView, name='test_4'),
#     path('test_5/', localization, name='test_5'),
#     # path('test_5/', test_5.as_view(), name='test_2'),
#     # path('test_6/', test_6.as_view(), name='test_2'),
#     # path('test_7/', test_7.as_view(), name='test_2'),
#     # path('test_8/', test_8.as_view(), name='test_2'), 
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
        # path('test_3/', UploadFile.as_view(), name='test_3'),

    ]

