from rest_framework import serializers

from .models import Survivor


class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = '__all__'
