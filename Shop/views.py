import cryptocode
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from Shop.models import Product, Profile, Message
from Shop.serializers import ProductSerializer, ProfileSerializer, UserSerializer, MessageSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    if not Profile.objects.filter(mobile__exact=request.data['mobile']):
        # img = request.data['img']
        # profile_type = request.data['profile_type']
        mobile = request.data['mobile']
        username = request.data['username']
        password = request.data['password']
        # address = request.data['address ']
        user = User(username=username)
        user.save()
        pro = Profile.objects.create(
            # img=img,
            # profile_type=profile_type,
            mobile=mobile,
            username=username,
            password=password,
            # address=address
        )
        pro.user = user
        pro.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'is_user': True}, status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    mobile = request.data["mobile"]
    password = request.data["password"]
    try:
        pro = Profile.objects.get(mobile__exact=mobile)
        if pro.password == password:
            return Response(data="OK", status=status.HTTP_200_OK)
        return Response(data="Password is incorrect", status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({'is_user': False}, status=status.HTTP_401_UNAUTHORIZED)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pro = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            message = serializer.create(validated_data=request.data)
            message.profile = pro
            message.save()
            return Response(data="send message", status=status.HTTP_201_CREATED)
        return Response(data="Please enter correct", status=status.HTTP_403_FORBIDDEN)
