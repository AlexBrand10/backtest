from rest_framework import serializers

from .models import AppUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AppUserSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=1, max_value=120)
    country = serializers.CharField(max_length=80)

    class Meta:
        model = AppUser
        fields = ['id', 'name', 'email', 'age', 'country', 'createdAt']

    def validate_email(self, value):
        normalized = value.strip().lower()
        if AppUser.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError('El email ya está registrado')
        return normalized

    def validate_name(self, value):
        return value.strip()

    def validate_country(self, value):
        return value.strip()
