from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Advocate, Company


class CompanySerializer(serializers.ModelSerializer):
    employee_count = SerializerMethodField(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'

    def get_employee_count(self, obj):
        count = obj.advocate_set.count()
        return count


class AdvocateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Advocate
        fields = ['username', 'bio', 'company', 'name', 'twitter', 'profile_picture']
