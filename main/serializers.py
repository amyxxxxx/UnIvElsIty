from rest_framework import serializers
from .models import To_do_list

class To_do_listSerializer(serializers.ModelSerializer):

    class Meta:
        model = To_do_list
        fields = '__all__'