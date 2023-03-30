import timeit
import tempfile

import requests, json, copy, datetime, traceback #traceback kullan #TODO

from django.utils import timezone
from django.conf import settings
from django.db.models import Q,Count #filtreleme opsiyonları için import ettik
from django.contrib import messages  #hata mesajlarını bu kütüphane ile yazdırıyoruz
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır
# from backend.app_base.models import User #yeni custom user model
from app_base import models as gdsc_app_base_models
from django.contrib.auth.decorators import login_required
from app_base.models import User #yeni custom user model


from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.core.files.base import ContentFile  #file handle
from django.http import HttpResponse, JsonResponse
from app_base import models as uc_models
from app_base import forms as uc_forms
# region LOCALIZATION
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as __
from django.utils import translation
# endregion LOCALIZATION

import chardet
from io import BytesIO

from django.shortcuts import render,redirect


# region TEMPLATE
# class test(APIView):
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

    from app_base.api.file_management import gc_storage
    bucket_name= settings.GS_BUCKET_NAME
    class UploadFile(APIView):
    # permission_classes = [IsAuthenticated]

        def put(self, request):
            file = request.FILES["file"] #InMemoryUploadedFile_obj
            print("1### type of the file: ",type(file)) 
            
            # ContentFile_obj = ContentFile(file.read())
            # print("2### type of the file: ",type(ContentFile_obj))
            # print("2### DİR of the file: ",dir(ContentFile_obj))

            # file_bytesio_obj = BytesIO(file.read())
            # file_content_in_bytes = file_bytesio_obj.getvalue()

            # print("\n### file: ",file)
            # if (file==file_bytesio_obj):
            #     print("### file and file_bytes are equal")
            # print("### type of the file: ",type(file_bytes))
            # file_bytes_2 = ContentFile(file.read())

            # with open(file_bytesio_obj, 'rb') as f:
            #     file_bytes_3= f.read()
            # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            #     temp_file.write(file_bytesio_obj.read())
            #     temp_file.flush()
            #     temp_file.seek(0)
            #     file_bytes_3 = temp_file.read()


            # file_content_bytes = file.encode('utf-8')
            # encoding_type_2 = chardet.detect(file.read())
            # print("### encoding_type_2: ",encoding_type_2)
            # print("### encoding_type_2 main: ",encoding_type_2["encoding"])

            # Create an in-memory file-like object from the bytes

            # encoding_type = chardet.detect(file_obj)
            # print("### encoding_type: ",encoding_type)
            # print("### encoding_type main: ",encoding_type["encoding"])
            # file_content_string = file.read().decode(encoding_type["encoding"])



            file_name = file.name
            file_name_wout_ext=file.name.split(".")[0]        
            print("### file name: ", file_name)
            file_content_type = file.content_type
            print("### file content type: ", file_content_type)
            bucket_path="test2"+"/"+file_name

            gc_storage.upload_blob_from_memory(contents=file.read(),destination_blob_name=bucket_path,content_type=file_content_type,bucket_name=bucket_name)

            # region 1

            # post_url = generate_upload_signed_url_v4(bucket_name=bucket_name,blob_name=bucket_path,content_type=file_content_type)
            # print("### post_url: ",post_url)
            # files_dict = {"file": (bucket_path, file_bytes)}

            # http_response = requests.put( 
            #     url=post_url,
            #     files=files_dict,
            #     headers={"Content-Type": file_content_type},
            # )
            # print("### http_response request body: ",http_response.request.body,"\n")
            # print("### http_response request headers: ",http_response.request.headers,"\n")
            # print("### http_response dir : ",dir(http_response),"\n")
            # print("### http_response: ",http_response,"\n")
            # print("### http_response status_code : ",http_response.status_code,"\n")
            # print("### http_response json: ",http_response.json,"\n")
            # print("### http_response content : ",http_response.content,"\n")
            # print("### http_response headers : ",http_response.headers,"\n")
            # print("### http_response body(text) : ",http_response.text,"\n")
            # response_content_type = http_response.headers['content-type']
            # print("### response_content_type : ",response_content_type,"\n")

            # NOTE: 204 means success. No deep research is done on that. It is just working.
            # if http_response.status_code != 204:
            #     raise Exception("File upload failed")

            # endregion 1

            return Response("hello")
    pass

##########################################################################################################################################
############################################################ <<< ALL ENVS >>> ############################################################
##########################################################################################################################################


def test_static_and_media_test(request):
    test_variables=["test","21"]
    
    context = { 'test_variables': test_variables}
    return render(request,'app_benchmarks_and_tests/static_and_media_test.html',context)

def localization(request):
    # try:
    #     print("işte session translation key: " ,request.session[translation.LANGUAGE_SESSION_KEY])
    # except KeyError:
    #     translation.activate('tr') # sets the language
    #     request.session[translation.LANGUAGE_SESSION_KEY] = 'tr' ## sets the language in the session
    #     print("session translation key set to tr")
    # translation.activate('tr')

    # if translation.LANGUAGE_SESSION_KEY in request.session:
    #     print("session translation key exists and it will be deleted now")
    #     del request.session[translation.LANGUAGE_SESSION_KEY]

    return render(request, 'app_benchmarks_and_tests/localization_test.html')

def localization_2(request):
    # try:
    #     print("işte session translation key: " ,request.session[translation.LANGUAGE_SESSION_KEY])
    # except KeyError:
    #     translation.activate('tr') # sets the language
    #     request.session[translation.LANGUAGE_SESSION_KEY] = 'tr' ## sets the language in the session
    #     print("session translation key set to tr")
    # translation.activate('tr')

    # if translation.LANGUAGE_SESSION_KEY in request.session:
    #     print("session translation key exists and it will be deleted now")
    #     del request.session[translation.LANGUAGE_SESSION_KEY]

    return render(request, 'app_benchmarks_and_tests/localization_test_2.html')

def localization_3(request):
    # try:
    #     print("işte session translation key: " ,request.session[translation.LANGUAGE_SESSION_KEY])
    # except KeyError:
    #     translation.activate('tr') # sets the language
    #     request.session[translation.LANGUAGE_SESSION_KEY] = 'tr' ## sets the language in the session
    #     print("session translation key set to tr")
    # translation.activate('tr')

    # if translation.LANGUAGE_SESSION_KEY in request.session:
    #     print("session translation key exists and it will be deleted now")
    #     del request.session[translation.LANGUAGE_SESSION_KEY]

    return render(request, 'app_benchmarks_and_tests/localization_test_3.html')

def dropdown_list_w_checkbox(request):
    return render(request, 'app_benchmarks_and_tests/dropdown_list_w_checkbox.html')

def dropdown_list_w_checkbox_2(request):
    return render(request, 'app_benchmarks_and_tests/dropdown_list_w_checkbox_2.html')

def dropdown_list_w_checkbox_3(request):
    return render(request, 'app_benchmarks_and_tests/dropdown_list_w_checkbox_3.html')

@login_required(login_url='login')
def createClub(request):
    form = uc_forms.ClubForm()
    topics= uc_models.Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)  #topic objesi varsa getiriyor topic yoksa oluşturuyoruz oluştuysa created=True oluşmadıysa created=False
        print(topic.id)
        instance =uc_models.Club()
        instance.leader = request.user
        instance.name = request.POST.get('name')
        instance.description = request.POST.get('description')
        instance.topic=topic
        if request.FILES.get('logo') is not None:
            instance.logo=request.FILES.get('logo')  ### !!! modeldeki imagefield'ın adı neyse bize yollanen keyin adı da o oluyor bu senaryoda fieldın adı 'logo'ydu ardından bu şekilde resmi alıyoruz
        instance.save()
        instance.participants.add(request.user)
        return redirect('club', pk=instance.id)
       
    context = { 'form': form, 'topics': topics }
    return render(request,'app_benchmarks_and_tests/club_form_test.html',context)

@login_required(login_url='login')
def updateClub(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    topics= uc_models.Topic.objects.all()
    form = uc_forms.ClubForm(instance=club)  #instance=room ile formun içine verileri yazdırıyoruz passliyoruz
    # room_topics_str=''
    # room_topics=list(room.topic.all())
    # for topic in room_topics:
    #     room_topics_str += topic.name + ', '
    # room_topics_str = room_topics_str[:-2]
    # print(room_topics_str)
    if request.user != club.leader:
        return HttpResponse('Bu Kulübün sahibi değilsiniz')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)  #topic objesi varsa getiriyor topic yoksa oluşturuyoruz oluştuysa created=True oluşmadıysa created=False
        club.name = request.POST.get('name')
        club.topic = topic
        club.description = request.POST.get('description')
        if request.FILES.get('logo') is not None:
            club.logo=request.FILES.get('logo')
        club.save()
        return redirect('club', pk=pk)
        # form = clubForm(request.POST,instance=club)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home') #url in özel adını pass leyerek yönledirebiliriz
   
    context = { 'form': form, 'topics': topics, 'club': club}
    return render(request,'app_benchmarks_and_tests/club_form_test.html',context)

@login_required(login_url='login')
def createEvent(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    topics= uc_models.Topic.objects.all()
    form = uc_forms.EventForm()
    is_edit_page=False

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)
        instance =uc_models.Event()
        instance.name = request.POST.get('name')
        instance.description = request.POST.get('description')
        instance.date = request.POST.get('date')
        instance.topic = topic
        if request.FILES.get('photo') is not None:
            instance.photo=request.FILES.get('photo')
        instance.club = club
        
        print("related_clubs: ",request.POST.get('related_clubs'))
        # print("participants: ",request.POST.get('participants'))
        
        instance.save()
        # for participant in request.POST.get('participants').split(','):
        #     user = User.objects.get(id=participant)
        #     instance.participants.add(user)
        # if request.POST.get('participants') is not None:
        #     for participant in request.POST.get('participants').split(','):
        #         user = User.objects.get(id=participant)
        #         instance.participants.add(user)
        if request.POST.get('related_clubs') is not None:
            for related_club in request.POST.get('related_clubs').split(','):
                club = uc_models.Club.objects.get(id=related_club)
      

        return redirect('event', pk=instance.id)
    context = { 'form': form , 'topics': topics, 'club': club, 'is_edit_page': is_edit_page}
    return render(request,'app_benchmarks_and_tests/event_form_test.html',context)

@login_required(login_url='login')
def updateEvent(request,pk):
    event=uc_models.Event.objects.get(id=pk)
    club=event.club
    topics= uc_models.Topic.objects.all()
    form = uc_forms.EventForm(instance=event)  #instance=room ile formun içine verileri yazdırıyoruz passliyoruz
    is_edit_page=True
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)  #topic objesi varsa getiriyor topic yoksa oluşturuyoruz oluştuysa created=True oluşmadıysa created=False
        event.name = request.POST.get('name')
        event.topic = topic
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        if request.FILES.get('photo') is not None:
            event.photo=request.FILES.get('photo')
        event.save()
        return redirect('event', pk=pk)
    context = { 'form': form, 'topics': topics, 'event': event, 'club': club, 'is_edit_page': is_edit_page}
    return render(request,'app_benchmarks_and_tests/event_form_test.html',context)
