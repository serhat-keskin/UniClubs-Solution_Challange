from django.forms import ModelForm
# from .models import Topic
# from django.contrib.auth.models import User  #ESKİ DEFAULT USER MODEL
# from .models import User #yeni custom user model
from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır

#region eski user form

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name','username', 'email', 'password1', 'password2']

#endregion

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name','surname', 'email', 'phone', 'password1', 'password2']
# class UpdateUserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar','name','surname', 'email', 'phone']
#         # exclude = ['password']
