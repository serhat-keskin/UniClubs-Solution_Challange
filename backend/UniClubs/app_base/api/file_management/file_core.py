from django.conf import settings
if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:

    import requests, json, copy, datetime, traceback
    from django.utils import timezone
    from django.db.models import Q,Count #filtreleme opsiyonları için import ettik
    from django.contrib import messages  #hata mesajlarını bu kütüphane ile yazdırıyoruz
    # from django.contrib.auth import authenticate, login, logout
    # from django.contrib.auth.decorators import login_required
    # from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır
    # from backend.app_base.models import User #yeni custom user model
    from app_base import models as gdsc_app_base_models

    from rest_framework.response import Response
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    from rest_framework_simplejwt.views import TokenObtainPairView
    from rest_framework import permissions
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.views import APIView
    from django.core.files.base import ContentFile  #file handle


    from .gc_storage import generate_download_signed_url_v4, generate_upload_signed_url_v4, upload_blob_from_memory, upload_blob_from_system 

    import chardet
    from io import BytesIO




    bucket_name= settings.GS_BUCKET_NAME

    class DownloadFile(APIView):
        # permission_classes = [IsAuthenticated]

        def get(self, request):
            blob_name = request.GET.get("blob_name")
            # blob_name=blob_name
            download_url=generate_download_signed_url_v4(blob_name=blob_name,bucket_name=bucket_name)
            return Response({"message": download_url})
            

    class UploadFile(APIView):  ##çalışmıyor
        # permission_classes = [IsAuthenticated]

        def put(self, request):
            file = request.FILES["file"]

            # file_content = file.read()

            file_content = ContentFile(file.read())

            # with open(file, 'rb') as f:
            #     file_content = f.read()



            file_name = file.name
            file_name_wout_ext=file.name.split(".")[0]        
            print("### file name: ", file_name)
            file_content_type = file.content_type
            print("### file content type: ", file_content_type)
            bucket_path=bucket_name+"/"+file_name
            test_blob_name="test_blob_name_3.jpg"
            post_url = generate_upload_signed_url_v4(bucket_name=bucket_name,blob_name=bucket_path,content_type=file_content_type)
            print("### post_url: ",post_url)
            files_dict = {"file": (bucket_path, file_content)}

            http_response = requests.put( 
                url=post_url,
                files=files_dict,
                headers={"Content-Type": file_content_type},
            )
            
            # print("### http_response request body: ",http_response.request.body,"\n")
            print("### http_response request headers: ",http_response.request.headers,"\n")
            print("### http_response dir : ",dir(http_response),"\n")
            print("### http_response: ",http_response,"\n")
            print("### http_response status_code : ",http_response.status_code,"\n")
            print("### http_response json: ",http_response.json,"\n")
            print("### http_response content : ",http_response.content,"\n")
            print("### http_response headers : ",http_response.headers,"\n")
            print("### http_response body(text) : ",http_response.text,"\n")
            response_content_type = http_response.headers['content-type']
            print("### response_content_type : ",response_content_type,"\n")

            # NOTE: 204 means success. No deep research is done on that. It is just working.
            # if http_response.status_code != 204:
            #     raise Exception("File upload failed")
            return Response(http_response.status_code)
else:
    print("\nCURRENT_ENVIRONMENT \"PROD\" VEYA \"DEV\" OLMADIĞI İÇİN file_core AYARLANMADI!\n")
    pass