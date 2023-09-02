from rest_framework import serializers

from .models import InfectionReport, Inventory, Resource, Survivor


class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class InfectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfectionReport
        fields = '__all__'
