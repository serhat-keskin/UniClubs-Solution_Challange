from django.contrib import admin
from django.apps import apps
from django.urls import path,include
from django.conf import settings #settings.py dosyasını import ediyoruz
from django.conf.urls.static import static #static dosyaları import ediyoruz


# from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Gunicorn ile inatla static serve etmek için ekledik (önerilmez)

# region LOCALIZATION

from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

### way 1

# urlpatterns = [  #çevrilmesini istemediğimiz url ler buraya
#     path('serhat/', admin.site.urls),
# ]
# urlpatterns += i18n_patterns(
#     path('', include('app_base.urls')),
#     path('api/', include('app_base.api.urls')),  
#     prefix_default_language=False)


### way 2 (best way) i18n urllerinin içindeki set_language urlini dahil ederek templatelerde bu url'i kullanarak dili set edebiliyoruz

urlpatterns = [  #çevrilmesini istemediğimiz url ler buraya
    path('i18n/', include('django.conf.urls.i18n')),
    path('uc-admin/', admin.site.urls),
    path('', include('app_portfolio.urls')),
    path('', include('app_base.urls')),
    path('api/', include('app_base.api.urls')), 
]

### way 3 (way2 + url translation)

# urlpatterns = [  
#     path('i18n/', include('django.conf.urls.i18n')), #i18n url lerini dahil ediyoruz
#     path('serhat/', admin.site.urls), #çevrilmesini istemediğimiz url ler buraya
# ]
# urlpatterns += i18n_patterns(
#     path('', include('app_base.urls')),
#     path(_('api/'), include('app_base.api.urls')),  ## '_' bu bir kısaltma gettext_lazy as _  !!! 
#     prefix_default_language=True)

# endregion LOCALIZATION

# region NO LOCALIZATION

# urlpatterns = [
#     path('serhat/', admin.site.urls),
#     path('', include('app_base.urls')),
#     path('api/', include('app_base.api.urls')),  
# ]

if settings.CURRENT_ENVIRONMENT in ["LOCAL", "DEV"]:
    urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
    ]

# endregion NO LOCALIZATION

# if settings.CURRENT_ENVIRONMENT in ["LOCAL", "DEV"]:
#     urlpatterns += i18n_patterns(
#     path('__debug__/', include('debug_toolbar.urls')),
#     prefix_default_language=True
#     )
if settings.CURRENT_ENVIRONMENT == "LOCAL":
    mediaStatic = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #static media pathini media root url ile bağlıyoruz
    print("### mediaStatic: ",mediaStatic)
    print("### settings.MEDIA_URL: ",settings.MEDIA_URL)
    print("### settings.MEDIA_ROOT: ",settings.MEDIA_ROOT)
    urlpatterns += mediaStatic

# region CUSTOM URLS
try:
    # way 1 #bu yöntem customize etmeye biraz daha müsait
    from app_benchmarks_and_tests.benchs import urls as benchmark_urls
    from app_benchmarks_and_tests.tests import urls as test_urls

    urlpatterns += [ # for no localization
        path('bench/', include(benchmark_urls)),
        path('test/', include(test_urls)),
    ]
    # urlpatterns += i18n_patterns(
    #     path('bench/', include(benchmark_urls)),
    #     path('test/', include(test_urls)),
    #     prefix_default_language=True
    # ) # localizasyon versiyonu

    print("\n##################### TEST/BENCH URL PATTERNS #####################")
    print("### BENCH URLS ###")
    for i, path in enumerate(benchmark_urls.urlpatterns):
        print(f"# {i} - BENCH URL: {path}")
    print("\n### TEST URLS ###")
    for i, path in enumerate(test_urls.urlpatterns):
        print(f"# {i} - TEST URL: {path}")
    print("###################################################################\n")

    # # way 2     -way 3 den farkı 2 urlslerin tek bir dosyada toplandığı urls i getiriyor
    # from benchmarks_and_tests.urls import urlpatterns as all_urlpatterns

    # urlpatterns.extend(all_urlpatterns)
    
    # # way 3
    # from benchmarks_and_tests.benchs.urls import urlpatterns as benchmark_urlpatterns
    # from benchmarks_and_tests.tests.urls import urlpatterns as test_urlpatterns

    # urlpatterns.extend(benchmark_urlpatterns)
    # urlpatterns.extend(test_urlpatterns)

except Exception as e:
    # If the module was not found, do nothing
    print("### 'benchmarks_and_tests' modülü bulunamadı")
    print("### error: ",e)
    pass
# endregion CUSTOM URLS

# region APP'LER
# app_configs = apps.get_app_configs()
# print("### app_configs: ",app_configs)
# app_names = [app_config.name for app_config in app_configs]
# print("### app_names: ",app_names)
# endregion APP'LER

print("\n##########################   URL PATTERNS ##########################")
for i, path in enumerate(urlpatterns):
    print(f"# {i} - URL: {path}")
print("###################################################################\n")

# for urlpattern in urlpatterns:
#     print("urlpattern: ", urlpattern)
#     print("urlpattern type: ", type(urlpattern))
 


# urlpatterns += staticfiles_urlpatterns() # Gunicorn ile inatla static serve etmek için ekledik (önerilmez)
# print("### urlpatterns with \"staticfiles_urlpatterns\": ",urlpatterns)




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