from datetime import date
from django.db import models
# from django.contrib.auth.models import User   ### artık default django user modelini kullanmıyoruz
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
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

class MyCustomUserManager(BaseUserManager):
    def create_user(self, email,name,surname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have an name')
        if not surname:
            raise ValueError('Users must have an surname')       

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.name = name
        user.surname = surname
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name,surname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,name=name,surname=surname
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=False, null=False)
    surname = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(null=True, default='defaults/user_avatar.svg', upload_to='private/images/avatars') ## her türlü default media storage kısmına yükleniyor bu durumda 'media/' prefixi default olarak gelip burada işlem yapıyor

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    history = HistoricalRecords()

    USERNAME_FIELD = 'email'  # username yerine email kullanmak için
    REQUIRED_FIELDS = ['name','surname']  

    objects =  MyCustomUserManager() ## MycustomUserManager'ı aslında BaseUserManager'ın bir alt sınıfı olarak düşünebiliriz. BaseUserManager'ın içindeki create_user ve create_superuser metodlarını override ederek kullanıyoruz. Bu sayede BaseUserManager'ın içindeki metodları kullanabiliyoruz.
    # objects = BaseUserManager()
    # @property
    # def is_staff(self):
    #     return self.is_admin 
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

              
    def __str__(self):
        fullname=self.name + ' ' + self.surname
        return fullname


class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='angara', null=True, blank=True)
    identity_no= models.CharField(max_length=255, blank=True, null=True)
    faculty= models.CharField(max_length=50, blank=True, null=True)
    department= models.CharField(max_length=50, blank=True, null=True)
    grade= models.CharField(max_length=50, blank=True, null=True)
    student_no= models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address= models.CharField(max_length=255, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


class Country(models.Model):
    name=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    language_code=models.CharField(max_length=100)
    native_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
class School(models.Model):
    name=models.CharField(max_length=255, blank=True, null=True)
    country=models.ForeignKey(Country, on_delete=models.SET_DEFAULT,default=1, related_name='school', blank=True, null=True)
    address=models.CharField(max_length=255, blank=True, null=True)
    phone=models.CharField(max_length=255, blank=True, null=True)
    staffs=models.ManyToManyField(User, related_name='schoolstaff', blank=True)
    admins=models.ManyToManyField(User, related_name='schooladmin', blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
# class Module(models.Model):
#     schools = models.ManyToManyField(School, related_name='module', blank=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     description= models.TextField(blank=True, null=True)

#     is_active = models.BooleanField(default=True)

class Topic(models.Model):
    name=models.CharField(max_length=100)

    is_active=models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
# class Room(models.Model):
#     school = models.ForeignKey(School, on_delete=models.SET_NULL, related_name="room", null=True)
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="host", null=True)  #related_name ile user objesinden room objesine ulaşabiliriz (user.room_set.all() gibi ama bu sefer isimlendirdiğimiz için user.hosts.all() olacak çünkü user.room_set.all() hangi fieldla ilşki kuracağını bilemez?)
#     topic= models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, related_name="room")  #TODO solarvis db de bazı fieldları on_delete=modeels.SET_NULL yapmamız gerek çünkü sil yapmamıza bir türlü izin vermiyor başke yerde bağlantısı olduğundan ?
#     participants = models.ManyToManyField(User, related_name="room", blank=True) #yukarıda host'da da User ile bağladığımız için related_name kullanmalıyız TODO (related_name detaylı araştır)
#     # topics= models.ManyToManyField(Topic,related_name="room")  #ilerisi için

#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)

#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)

#     is_active = models.BooleanField(default=True)
#     history = HistoricalRecords()

#     class Meta:  #varsayılan filtreleme configini yapar
#         ordering = ['-created','-updated']  #önce created sonra updated e göre sıralıyor başra '-' olursa azalan sıralama veya tam tersi olur deneyrek anlarsın

#     def __str__(self): #bu methodu yazmazsak admin panelinde room objeleri görünürken Room object (1) gibi görünür #TODO (objects.get() methodu ile obje getirdiğimizde bu objeyi yazdırmaya kalktığımızda bla bla object diyor ya acaba onu da handle ediyor mu, büyük ihtimalle user objelerinin gösterimini handle ediyor)
#         return self.name
# class Message(models.Model):
#     user= models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()

#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.body[0:50]

class Club(models.Model):
    school=models.ForeignKey(School, on_delete=models.SET_NULL, related_name="club", null=True)
    leader=models.ForeignKey(User, on_delete=models.SET_NULL, related_name="leader", null=True)
    participants = models.ManyToManyField(User, related_name='club', blank=True)  ### related_name='related_clubs' NEY İÇİN ÖĞREN BURADA KLASİK 'through' KULLANABİLİRDİK
    topic= models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, related_name='club')  
    # topics= models.ManyToManyField(Topic, related_name='club', blank=True) #ilerisi için

    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    logo=models.ImageField(null=True, default='defaults/logo.jpeg', upload_to='private/images/icons/clubs')

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:  #varsayılan filtreleme configini yapar
        ordering = ['-created','-updated']  #önce created sonra updated e göre sıralıyor başra '-' olursa azalan sıralama veya tam tersi olur deneyrek anlarsın

    def __str__(self):
        return self.name
        
class Event(models.Model):
    #code that sets many to many club relation
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, related_name='test', null=True)  ###ŞİMDİLİK KOLAYLIK OLSUN DİYE VAR NORMALDE SADECE 'related_clubs' İLE yapacağız gerçi etkinliğin birincil sahibi kulüp olarak da kullanabiliriz
    participants = models.ManyToManyField(User, related_name='event', blank=True)  ### related_name='related_clubs' NEY İÇİN ÖĞREN BURADA KLASİK 'through' KULLANABİLİRDİK
    related_clubs = models.ManyToManyField(Club, through='EventxClub', blank=True ,related_name='event')  ### through='EventClub' NEY İÇİN ÖĞREN BURADA KLASİK 'through' KULLANABİLİRDİK
    topic= models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, related_name='event')

    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    photo=models.ImageField(null=True, default='defaults/logo.jpeg', upload_to='private/images/icons/events')

    date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:  #varsayılan filtreleme configini yapar
        ordering = ['-created','-updated']  #önce created sonra updated e göre sıralıyor başra '-' olursa azalan sıralama veya tam tersi olur deneyrek anlarsın

class EventxClub(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True, null=True)
    updated=models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.event.name + ' - ' + self.club.name
    
    

class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements', null=True)
    topic= models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, related_name="announcement")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    photo=models.ImageField(null=True, default='defaults/logo.jpeg', upload_to='private/images/icons/announcements')

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:  #varsayılan filtreleme configini yapar
        ordering = ['-created','-updated']  #önce created sonra updated e göre sıralıyor başra '-' olursa azalan sıralama veya tam tersi olur deneyrek anlarsın

    def __str__(self):
        return self.name

