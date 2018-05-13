from rest_framework import serializers
from core.models import Step

class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        exclude = ()