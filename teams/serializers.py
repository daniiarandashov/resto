from rest_framework import serializers

from rest_framework.relations import SlugRelatedField
from .models import Cook

class CookSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='first_name',read_only=True)
    # author = SlugRelatedField(slug_field='feedback_text',read_only=True)

    def create(self, validated_data):
        if self.context.get('user_id',None):
            validated_data['user_id']=self.context.get('user_id')
        else:
            validated_data['user_id']=self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = Cook
        fields = '__all__'