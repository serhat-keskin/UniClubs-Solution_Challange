from django.urls import path
from . import views 
urlpatterns = [
    path('',views.home, name='home'),  ##viewlara name vererek ileride bu name ile çağırabiliriz
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('user/<str:pk>/',views.userProfile, name='user_profile'),
    path('update_user/',views.updateUser, name='update_user'),

    
    # path('room/<str:pk>/',views.room, name="room"),
    # path('create_room/',views.createRoom, name="create_room"),
    # path('update_room/<str:pk>/',views.updateRoom, name="update_room"),
    # path('delete_room/<str:pk>/',views.deleteRoom, name="delete_room"),

    # path('delete_message/<str:pk>/',views.deleteMessage, name="delete_message"),

    path('club/<str:pk>/',views.club, name="club"),
    path('create_club/',views.createClub, name="create_club"),
    path('update_club/<str:pk>/',views.updateClub, name="update_club"),
    path('delete_club/<str:pk>/',views.deleteClub, name="delete_club"),
    path('join_club/<str:pk>/',views.joinClub, name="join_club"),

    path('event/<str:pk>/',views.event, name="event"),
    path('create_event/<str:pk>/',views.createEvent, name="create_event"),
    path('update_event/<str:pk>/',views.updateEvent, name="update_event"),
    path('delete_event/<str:pk>/',views.deleteEvent, name="delete_event"),

    path('announcement/<str:pk>/',views.announcement, name="announcement"),
    path('create_announcement/<str:pk>/',views.createAnnouncement, name="create_announcement"),
    path('update_announcement/<str:pk>/',views.updateAnnouncement, name="update_announcement"),
    path('delete_announcement/<str:pk>/',views.deleteAnnouncement, name="delete_announcement"),


    path('topics/', views.topicsPage, name="topics"),
    path('eventpage/', views.eventPage, name="mobile_event_page"),
    path('announcementpage/', views.eventPage, name="mobile_announcement_page"),

    path("statistics/", views.statistics.as_view(), name="statistics"),
    path("statistics/clubs/", views.statisticsofclubs.as_view(), name="statistics_clubs"),
    path("statistics/events/", views.statisticsofevents.as_view(), name="statistics_events"),

    path('admin/',views.adminhome, name='adminhome'),  ##viewlara name vererek ileride bu name ile çağırabiliriz

] 