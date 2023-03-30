from django.urls import path
from . import views
from .file_management import file_core
from django.conf import settings #settings.py dosyasını import ediyoruz


from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
###
urlpatterns = [
    path('',views.getRoutes, name='routes'),
    path('clubs/',views.getClubs , name='clubs'),
    path('clubs/<str:pk>',views.getClub),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), #Project Configuration
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #Project Configuration
   
]

if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:
    urlpatterns += [
        path('file/upload', file_core.UploadFile.as_view()),
        path('file/download', file_core.DownloadFile.as_view())
    ]


