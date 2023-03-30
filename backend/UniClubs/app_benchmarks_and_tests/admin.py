from django.apps import apps
from django.contrib import admin

# # Register all models with the admin site
# for model in apps.get_models():
#     excluded_models = ["OutstandingToken","BlacklistedToken"]
#     print("## model: ",model)
#     print("## str model: ",model.__name__)
#     if not admin.site.is_registered(model) and model.__name__ not in excluded_models: #admin'e kayıt olup olmamışmı kontrol eder bazı 3rd party uygulamalar sonradan tekrar kaydetmeye çalışıyor bu da hataya sebep oluyor bunun için excluded apps diye bir list oluşturduk
#         admin.site.register(model)

# Register all models with the admin site for specific app
app_models = apps.get_app_config('app_benchmarks_and_tests').get_models()
all_installed_apps = apps.get_app_configs()

print("\n##################### ADMIN REGISTERATION(admin.py) #####################\n")
print("\n################### <<< app_benchmarks_and_tests >>> ####################\n")
for model in app_models:
    if not admin.site.is_registered(model): #performans için sorgu kaldırılabilir
        admin.site.register(model)
        print(f"{model.__name__} registered successfully.")
    else:
        print(f"{model.__name__} is already registered.")
print("\n########################################################################\n")
# # Dynamically register models with the admin site via list defined by us    
# models_to_register = [models.User, models.Club, models.Event, models.Room, models.Message, models.Topic, models.EventxClub, models.Announcement]

# for model in models_to_register:
#     admin.site.register(model)

# from . import models    ## kötü yöntem
# admin.site.register(models.<yourmodel>)
