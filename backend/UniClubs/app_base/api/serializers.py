from rest_framework.serializers import ModelSerializer
from app_base import models as gdsc_app_base_models
from django.db import models
from rest_framework import serializers



#####  gelen obj yi json a serialize edemediğimiz için (misal <objectname>.objects.get(id=1) / <objectname>.objects.all() ) bu serializer ları kullanıyoruz  ######

class ClubSerializer(ModelSerializer):
    class Meta:
        model = gdsc_app_base_models.Club
        fields = '__all__'

# Tüm modelleri model_list değişkenine al
model_list = [
    obj for name, obj in gdsc_app_base_models.__dict__.items()
    if isinstance(obj, models.Model)
]

# Tüm modeller için serializer oluştur
serializers_for_all = {}
for model in model_list:
    class_name = model.__name__ + 'Serializer'
    serializer_class = type(class_name, (serializers.ModelSerializer,), {'class Meta:': {'model': model, 'fields': '__all__'}})
    serializers_for_all[model] = serializer_class
