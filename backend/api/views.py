from django.shortcuts import render

from .models import *
from .serializers import MyTokenObtainPairSerializer, UserSerializer, RegisterSerializer, TransactionSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterUserView(generics.CreateAPIView):
    qs = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


class TransactionView(generics.CreateAPIView):
    qs = Transaction.objects.all()      # linter may flag error, but it's ok
    permission_classes = ([AllowAny])
    serializer_class = TransactionSerializer


# TODO: completing this.
# only logged in users can access dashboard and retrieve transaction data
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        context = f"Hey, {request.user}, you are getting a GET response."
        return Response({'response' : context}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get("text")
        context = f"Hey, {request.user}, your text is {text}"
        return Response({'response' : context}, status=status.HTTP_200_OK)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)
