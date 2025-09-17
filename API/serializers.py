from .models import *
from rest_framework import serializers

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

class JobcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = '__all__'

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'
        
class PartlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartsList
        fields = '__all__'