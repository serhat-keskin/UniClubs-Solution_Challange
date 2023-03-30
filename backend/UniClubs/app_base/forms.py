from django.forms import ModelForm
from . import models as uc_models
# from django.contrib.auth.models import User  #ESKİ DEFAULT USER MODEL
from .models import User #yeni custom user model
from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır

#region eski user form

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name','username', 'email', 'password1', 'password2']

#endregion

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','surname', 'email', 'phone', 'password1', 'password2']
class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','surname', 'email', 'phone']
        # exclude = ['password']

# class RoomForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
#         exclude = ['host', 'participants']

class ClubForm(ModelForm):
    class Meta:
        model = uc_models.Club
        fields = '__all__'
        exclude = ['leader']
        # exclude = ['leader', 'participants']

class EventForm(ModelForm):
    class Meta:
        model = uc_models.Event
        fields = '__all__'
        # exclude = ['related_clubs']

class AnnouncementForm(ModelForm):
    class Meta:
        model = uc_models.Announcement
        fields = '__all__'
        # exclude = ['related_clubs']