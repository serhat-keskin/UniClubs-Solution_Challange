from datetime import date
from django.db import models
# from django.contrib.auth.models import User   ### artık default django user modelini kullanmıyoruz
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from simple_history.models import HistoricalRecords
from simple_history import register


#region Eski User Modeli

# class User(AbstractUser):  # Orijinal User modelinin bütün özelliklerini alır. orijinal olan yerine bunu kullanması için settins.py de AUTH_USER_MODEL = 'app_base.User' yazılmalı
#     name = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(max_length=255, unique=True)
#     bio = models.TextField(blank=True, null=True)

#     avatar = models.ImageField(null=True, default='images/avatars/avatar.svg', upload_to='images/avatars')

#     USERNAME_FIELD = 'email'  # username yerine email kullanmak için
#     REQUIRED_FIELDS = ['username']  

#endregion

# class MyCustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have an username')

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

# class MyCustomUserManager(BaseUserManager):
#     def create_user(self, email,name,surname, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not name:
#             raise ValueError('Users must have an name')
#         if not surname:
#             raise ValueError('Users must have an surname')       

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.name = name
#         user.surname = surname
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email,name,surname, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,name=name,surname=surname
#         )
#         user.is_admin = True
#         user.is_superuser = True
#         user.is_staff = True

#         user.save(using=self._db)
#         return user
    
# class User(AbstractBaseUser):
#     name = models.CharField(max_length=255, blank=False, null=False)
#     surname = models.CharField(max_length=255, blank=False, null=False)
#     email = models.EmailField(max_length=255, unique=True)
#     phone = models.CharField(max_length=255, blank=True, null=True)
#     avatar = models.ImageField(null=True, default='public/defaults/avatar.svg', upload_to='private/images/avatars')

#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     history = HistoricalRecords()

#     USERNAME_FIELD = 'email'  # username yerine email kullanmak için
#     REQUIRED_FIELDS = ['name','surname']  

#     objects =  MyCustomUserManager() ## MycustomUserManager'ı aslında BaseUserManager'ın bir alt sınıfı olarak düşünebiliriz. BaseUserManager'ın içindeki create_user ve create_superuser metodlarını override ederek kullanıyoruz. Bu sayede BaseUserManager'ın içindeki metodları kullanabiliyoruz.
#     # objects = BaseUserManager()
#     # @property
#     # def is_staff(self):
#     #     return self.is_admin 
#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

              
#     def __str__(self):
#         fullname=self.name + ' ' + self.surname
#         return fullname

# class Topic(models.Model):
#     name=models.CharField(max_length=100)

#     is_active=models.BooleanField(default=True)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.name

# class Announcement(models.Model):
#     topic= models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, related_name="announcement")
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     photo=models.ImageField(null=True, default='public/defaults/avatar.svg', upload_to='private/images/icons/announcements')

#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)

#     is_active = models.BooleanField(default=True)
#     history = HistoricalRecords()

#     class Meta:  #varsayılan filtreleme configini yapar
#         ordering = ['-created','-updated']  #önce created sonra updated e göre sıralıyor başra '-' olursa azalan sıralama veya tam tersi olur deneyrek anlarsın

#     def __str__(self):
#         return self.name

# class DocumentType(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.name
    
# class Document(models.Model):
#     document = models.FileField(upload_to="private/documents", null=True, blank=False)
#     document_type = models.ForeignKey(DocumentType,on_delete=models.SET_NULL,null=True,blank=False)
#     user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='dosya', null=False, blank=False)
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.document.name
