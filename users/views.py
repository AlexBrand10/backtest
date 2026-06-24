from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, AppUser
from .serializers import AppUserSerializer, LoginSerializer
from .tokens import create_access_token


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].strip().lower()
        password = serializer.validated_data['password']

        account = Account.objects.filter(email__iexact=email).first()
        if account is None or not check_password(password, account.password):
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'token': create_access_token(account),
            'user': {'id': account.id, 'email': account.email, 'fullName': account.full_name},
        })


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = AppUserSerializer

    def get_queryset(self):
        queryset = AppUser.objects.all().order_by('-created_at', '-id')
        search = self.request.query_params.get('search', '').strip()
        country = self.request.query_params.get('country', '').strip()
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(email__icontains=search))
        if country:
            queryset = queryset.filter(country=country)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': 'El email ya está registrado'}, status=status.HTTP_409_CONFLICT)
