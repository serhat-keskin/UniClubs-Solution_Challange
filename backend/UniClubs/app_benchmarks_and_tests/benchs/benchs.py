from django.conf import settings #settings.py dosyasını import ediyoruz
import timeit
from rest_framework.views import APIView
from rest_framework.response import Response

# from app_base.api.file_management.gc_storage

# region TEMPLATE
# class bench(APIView):
#     def get(self, request):
#         return Response("bench_2")
# endregion

if settings.CURRENT_ENVIRONMENT in ["LOCAL"]:
   
    pass

if settings.CURRENT_ENVIRONMENT in ["DEV"]:

    pass

if settings.CURRENT_ENVIRONMENT in ["LOCAL", "DEV"]:

    pass

if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:
    pass
class test_importing(APIView):
    def get(self, request):
        def get_bucket_name_from_settings():
            from django.conf import settings
            return settings.GS_BUCKET_NAME

        def get_bucket_name_from_env():
            import os
            return os.environ['DEV_BUCKET_NAME']

        # Run each option 1 million times and time it
        num_iterations = 10

        t2 = timeit.timeit(get_bucket_name_from_env, number=num_iterations)
        t1 = timeit.timeit(get_bucket_name_from_settings, number=num_iterations)

        print(f"Time for get_bucket_name_from_settings: {t1}")
        print(f"Time for get_bucket_name_from_env: {t2}")
        results={
            "Time for get_bucket_name_from_settings": t1,
            "Time for get_bucket_name_from_env": t2
        }

        return Response(results)
    
