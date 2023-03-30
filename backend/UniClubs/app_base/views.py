from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q,Count #filtreleme opsiyonları için import ettik
from django.contrib import messages  #hata mesajlarını bu kütüphane ile yazdırıyoruz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır
from django.http import HttpResponse
from . import models as uc_models
from . import forms as uc_forms
# from django.contrib.auth.models import User  #ESKİ DEFAULT USER MODEL
from .models import User #yeni custom user model
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.core.files.base import ContentFile  #file handle
import requests, json, copy, datetime, traceback
from django.utils import timezone

# region LOCALIZATION
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as __
from django.utils import translation
# endregion LOCALIZATION

def home(request):
    # allrooms_count = uc_models.Room.objects.all().count()
    allclubs_count = uc_models.Club.objects.all().count()
    q = request.GET.get('q') if request.GET.get('q') != None else ''    #home templateinden urle q parametresiyle yönlendirilen requestteki 'q' parametresini alıyoruz
    clubs= uc_models.Club.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    ) #TODO kulüplerde filtreleme yapılacak
    # rooms= uc_models.Room.objects.filter(
    #         Q(topic__name__icontains = q) |
    #         Q(name__icontains = q) |
    #         Q(description__icontains = q)
    #         )  # __icontains harf eşleşmesi var mı diye bakar büyük küçük harf duyarlılığı yoktur (__contains büyük küçük harf duyarlılığı vardır), 
    #         #'Q' ile filtreleme koşulları yazabiliriz and(&) ve or(|) lar kullanabiliriz
    # room_count=rooms.count()
    # room_messages = uc_models.Message.objects.filter(Q(room__topic__name__icontains = q))  
    club_count = clubs.count()
    topics= uc_models.Topic.objects.all()[0:5]
    events = uc_models.Event.objects.all()
    announcements = uc_models.Announcement.objects.all()

    # room_messages = uc_models.Message.objects.all().order_by('-created')[:6]  #room ile ilişkili mesajları alıyoruz bu sytnax bize set of messages'ı verir
    context = { 'clubs': clubs,'topics': topics, 'club_count': club_count,
     'allclubs_count': allclubs_count, 'events': events, 'announcements': announcements}
    return render(request,'app_base/home.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: #eğer kullanıcı giriş yapmışsa home a yönlendir
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Bu Kullanıcı adıyla kayıtlı bir kullanıcı yok')
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.info(request, 'Username OR password is incorrect')

        user = authenticate(request, email=email, password=password)  # authenticate methodu argüman olarak yollanan credentialslarla eşleşen bir user objesi varsa onu return eder
        if user is not None:   #eğer user objesi varsa login ediyoruz böylece db de ve browserda session oluşuyor ve kullanıcı giriş yapmış oluyor ardından home page'e yönlendiriyoruz
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Kullanıcı adı veya şifre yanlış')
    context = {"page": page}
    return render(request,'app_base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    if request.user.is_authenticated: #eğer kullanıcı giriş yapmışsa home a yönlendir
        return redirect('home')
    page = 'register'
    form = uc_forms.MyUserCreationForm()
    if request.method == 'POST':
        form = uc_forms.MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #kullanıcıyı hemen kaydetmeyip commit=False ile biraz bekletiyoruz gerekli checklerden sonra kaydediyoruz
            user.username = user.email.lower()
            user.save()
            login(request, user) #kullanıcıyı kaydettikten sonra login ediyoruz
            # form.save()
            # user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            return redirect('home')
        else:
            messages.error(request, 'Kayıt sırasında bir hata oluştu')
    context = {"page": page, 'form': form}
    
    return render(request,'app_base/login_register.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    clubs= user.club.all()
    events = uc_models.Event.objects.all()
    announcements = uc_models.Announcement.objects.all()
    # rooms= user.host.all()  #related_name i host olan field ile ilişkili roomları alıyoruz !!!!
    # room_messages = user.message_set.all()
    # topics= uc_models.Topic.objects.all()
    # context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}

    topics= uc_models.Topic.objects.all()
    context= {'user': user, 'clubs': clubs, 'topics': topics, 'events': events, 'announcements': announcements}
    return render(request,'app_base/user_profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = uc_forms.UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = uc_forms.UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    context = {'form': form}
    return render(request,'app_base/update_user.html',context)

#region ===========< ROOM >===========

# def room(request,pk):
#     room=uc_models.Room.objects.get(id=pk)
#     room_messages = room.message_set.all().order_by('-created')  #room ile ilişkili mesajları alıyoruz bu sytnax bize set of messages'ı verir
#     participants = room.participants.all()
#     if request.method == 'POST':
#         message = request.POST.get('body') #room.html sayfasındaki ilgili input tagindeki name'i 'body' olan gelen inputun değerini alıyoruz
#         if message:
#             uc_models.Message.objects.create(
#                 user=request.user,
#                 body=message,
#                 room=room
#                 )
#             room.participants.add(request.user) #mesaj yollayan otomatik olarak odaya kayıtoluyor
#             # room.participants.remove(request.user)  #kullanıcıyı siler

#             return redirect('room', pk=pk)
#             # room.message_set.create(user=request.user, message=message)
#     context = { 'room': room, 'room_messages': room_messages, 'participants': participants }
#     return render(request,'app_base/room/room.html',context)

# @login_required(login_url='login')
# def createRoom(request):
#     form = uc_forms.RoomForm()
#     topics= uc_models.Topic.objects.all()
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)  #topic objesi varsa getiriyor topic yoksa oluşturuyoruz oluştuysa created=True oluşmadıysa created=False

#         uc_models.Room.objects.create(
#             host=request.user,
#             topic=topic,
#             name=request.POST.get('name'),
#             description=request.POST.get('description'),
#             )
#         return redirect('home')
       
#     context = { 'form': form, 'topics': topics }
#     return render(request,'app_base/room/room_form.html',context)

# @login_required(login_url='login')
# def updateRoom(request,pk):
#     room=uc_models.Room.objects.get(id=pk)
#     topics= uc_models.Topic.objects.all()
#     room_topics_str=''
#     room_topics=list(room.topic.all())
#     for topic in room_topics:
#         room_topics_str += topic.name + ', '
#     room_topics_str = room_topics_str[:-2]
#     print(room_topics_str)
#     form = uc_forms.RoomForm(instance=room)  #instance=room ile formun içine verileri yazdırıyoruz passliyoruz
#     if request.user != room.host:
#         return HttpResponse('Bu odanın sahibi değilsiniz')
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = uc_models.Topic.objects.get_or_create(name=topic_name)  #topic objesi varsa getiriyor topic yoksa oluşturuyoruz oluştuysa created=True oluşmadıysa created=False
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')
#         # form = RoomForm(request.POST,instance=room)
#         # if form.is_valid():
#         #     form.save()
#         #     return redirect('home') #url in özel adını pass leyerek yönledirebiliriz
   
#     context = { 'form': form, 'topics': topics, 'room': room, 'room_topics_str': room_topics_str }
#     return render(request,'app_base/room/room_form.html',context)

# @login_required(login_url='login')
# def deleteRoom(request,pk):
#     room=uc_models.Room.objects.get(id=pk)
#     if request.user != room.host:
#         return HttpResponse('Bu odanın sahibi değilsiniz')
        
#     if request.method == 'POST':
#         room.delete()
#         return redirect('home')
#     context = { 'obj': room }
#     return render(request,'app_base/delete.html',context)

# @login_required(login_url='login')
# def deleteMessage(request,pk):
#     message=uc_models.Message.objects.get(id=pk)
#     if request.user != message.user:
#         return HttpResponse('Bu mesajı silme yetkiniz yok')
#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')
#     context = { 'obj': message }
#     return render(request,'app_base/delete.html',context)
#endregion

#region ===========< CLUB >===========

#region ===========< eski v0.1 >===========

# def club(request,pk):
#     # clubvalue=None
#     # for club in clubs:
#     #     if club.id==int(pk):
#     #         clubvalue=club
#     # context = { 'clubdata': clubvalue }
#     club=uc_models.Club.objects.get(id=pk)
#     events=list(uc_models.Event.objects.filter(related_clubs=club))
#     members=list(club.related_users.filter())
#     print(members)
#     for member in members:
#         print(member)
#         print(member.id)
#         print(member.username)
#     context = { 'club': club , 'events': events, 'members': members}
#     return render(request,'app_base/club.html',context)

# @login_required(login_url='login')
# def createClub(request):
#     form = ClubForm()
#     if request.method == 'POST':
#         form = ClubForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home') #url in özel adını pass leyerek yönledirebiliriz
#     context = { 'form': form }
#     return render(request,'app_base/club_form.html',context)

# @login_required(login_url='login')
# def updateClub(request,pk):
#     club=uc_models.Club.objects.get(id=pk)
#     form = ClubForm(instance=club)  #instance=room ile formun içine verileri yazdırıyoruz passliyoruz
#     if request.method == 'POST':
#         form = ClubForm(request.POST,instance=club)
#         if form.is_valid():
#             form.save()
#             return redirect('home') #url in özel adını pass leyerek yönledirebiliriz
#     context = { 'form': form }
#     return render(request,'app_base/club_form.html',context)

# @login_required(login_url='login')
# def deleteClub(request,pk):
#     club=uc_models.Club.objects.get(id=pk)
#     if request.method == 'POST':
#         club.delete()
#         return redirect('home')
#     context = { 'item': club }
#     return render(request,'app_base/delete.html',context)

#endregion

def club(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    club_events=list(uc_models.Event.objects.filter(club=club))
    print(club_events)
    participants=club.participants.all()

    # club_events2 = club.message_set.all().order_by('-created')  #club ile ilişkili mesajları alıyoruz bu sytnax bize set of messages'ı verir
    # participants2 = club.participants.all()

    if request.method == 'POST':
        # message = request.POST.get('body') #club.html sayfasındaki ilgili input tagindeki name'i 'body' olan gelen inputun değerini alıyoruz
        # if message:
        #     uc_models.Message.objects.create(
        #         user=request.user,
        #         body=message,
        #         club=club
        #         )
            club.participants.add(request.user) #mesaj yollayan otomatik olarak odaya kayıtoluyor
            # club.participants.remove(request.user)  #kullanıcıyı siler

            return redirect('club', pk=pk)
            # club.message_set.create(user=request.user, message=message)
    context = { 'club': club, 'club_events': club_events, 'participants': participants }
    return render(request,'app_base/club/club.html',context)

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
    return render(request,'app_base/club/forms/club_form.html',context)

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
    return render(request,'app_base/club/forms/club_form.html',context)

@login_required(login_url='login')
def deleteClub(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    if request.user != club.leader:
        return HttpResponse('Bu Kulübün sahibi değilsiniz')
        
    if request.method == 'POST':
        club.delete()
        return redirect('home')
    context = { 'obj': club }
    return render(request,'app_base/delete.html',context)


def event(request,pk):
    event=uc_models.Event.objects.get(id=pk)
    club=event.club
    participants=event.club.participants.all()

    # if request.method == 'POST':
    #     event.participants.add(request.user) #mesaj yollayan otomatik olarak odaya kayıtoluyor
    #     # club.participants.remove(request.user)  #kullanıcıyı siler
    #     return redirect('event', pk=pk)

    context = { 'event': event, 'participants': participants, 'club': club }
    return render(request,'app_base/club/event/event.html',context)

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
        instance.save()
      
        return redirect('event', pk=instance.id)
    context = { 'form': form , 'topics': topics, 'club': club, 'is_edit_page': is_edit_page}
    return render(request,'app_base/club/forms/event/event_form.html',context)   

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
    return render(request,'app_base/club/forms/event/event_form.html',context)

@login_required(login_url='login')
def deleteEvent(request,pk):
    event=uc_models.Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    context = { 'obj': event }
    return render(request,'app_base/delete.html',context)

@login_required(login_url='login')    
def joinClub(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    club.participants.add(request.user)
    return redirect('club',pk=pk)

def announcement(request,pk):
    announcement=uc_models.Announcement.objects.get(id=pk)
    club=announcement.club
    participants=announcement.club.participants.all()

    # if request.method == 'POST':
    #     event.participants.add(request.user) #mesaj yollayan otomatik olarak odaya kayıtoluyor
    #     # club.participants.remove(request.user)  #kullanıcıyı siler
    #     return redirect('event', pk=pk)

    context = { 'announcement': announcement, 'participants': participants, 'club': club }
    return render(request,'app_base/club/announcement/announcement.html',context)

@login_required(login_url='login')
def createAnnouncement(request,pk):
    club=uc_models.Club.objects.get(id=pk)
    form = uc_forms.AnnouncementForm()
    is_edit_page=False

    if request.method == 'POST':
        instance =uc_models.Announcement()
        instance.name = request.POST.get('name')
        instance.description = request.POST.get('description')
        instance.date = request.POST.get('date')
        if request.FILES.get('photo') is not None:
            instance.photo=request.FILES.get('photo')
        instance.club = club
        instance.save()
        return redirect('announcement', pk=instance.id)
    context = { 'form': form , 'club': club, 'is_edit_page': is_edit_page}
    return render(request,'app_base/club/forms/announcement/announcement_form.html',context)

@login_required(login_url='login')
def updateAnnouncement(request,pk):
    announcement=uc_models.Announcement.objects.get(id=pk)
    club=announcement.club
    form = uc_forms.AnnouncementForm(instance=announcement)
    is_edit_page=True
    if request.method == 'POST':
        announcement.name = request.POST.get('name')
        announcement.description = request.POST.get('description')
        announcement.date = request.POST.get('date')
        if request.FILES.get('photo') is not None:
            announcement.photo=request.FILES.get('photo')
        announcement.save()
        return redirect('announcement', pk=pk)
    context = { 'form': form, 'announcement': announcement, 'club': club, 'is_edit_page': is_edit_page}
    return render(request,'app_base/club/forms/announcement/announcement_form.html',context)

@login_required(login_url='login')
def deleteAnnouncement(request,pk):
    announcement=uc_models.Announcement.objects.get(id=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('home')
    context = { 'obj': announcement }
    return render(request,'app_base/delete.html',context)



#endregion


#region mobil görünümde çıkan 2 butonun kodları?

#region  yeni

def topicsPage(request):
    total_room=0
    total_club=0
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = uc_models.Topic.objects.filter(name__icontains=q)
    for topic in topics:
        total_club += topic.club.count()

    context = { 'topics': topics, 'total_club': total_club }
    return render(request,'app_base/club/topic/mobile_topics_page.html',context)

def eventPage(request):
    events = uc_models.Event.objects.all()
    context = { 'events': events }
    return render(request,'app_base/club/event/mobile_event_page.html',context)

def announcementPage(request):
    announcements = uc_models.Announcement.objects.all()
    context = { 'announcements': announcements }
    return render(request,'app_base/club/announcement/mobile_announcement_page.html',context)
#endregion
#region  eski

# def topicsPage(request):
#     total_room=0
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     topics = uc_models.Topic.objects.filter(name__icontains=q)
#     for topic in topics:
#         total_room += topic.room_set.count()

#     context = { 'topics': topics, 'total_room': total_room }
#     return render(request,'app_base/topics.html',context)

# def activityPage(request):
#     room_messages = uc_models.Message.objects.all()
#     context = {'room_messages': room_messages }
#     return render(request,'app_base/activity.html',context)

#endregion

#endregion

#region ===========< STATISTICS >===========
class statistics(View):
    template_name = "app_base/club/statistic/club_statistics.html"
    def get(self,request):
        return render(request,self.template_name)
    


class statisticsofclubs(View):
    template_name = "app_base/club/statistic/memberorder.html"
    def get(self,request):
        clubmembernumberorder = uc_models.Club.objects.annotate(num_participants=Count('participants')).order_by('-num_participants')
        return render(request,self.template_name,{'clubmembernumberorder': clubmembernumberorder})


class statisticsofevents(View):
    template_name = "app_base/club/statistic/eventorder.html"
    def get(self,request):
        #code that calculates date a month ago
        month_ago = timezone.now() - timezone.timedelta(days=30)
        #Query that returns the count of all clubs Foreign key that is events after month_ago
        clubeventnumberorder = uc_models.Club.objects.annotate(num_event=Count('event', filter=Q(event__created__gte=month_ago))).order_by('-num_event')
        return render(request,self.template_name,{'clubeventnumberorder': clubeventnumberorder})
        
#endregion


def adminhome(request):
    return render(request,'app_base/admin_panel/index.html')