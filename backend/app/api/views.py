# from django.contrib.auth.models import User
from api.models import User, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import ProfileSerializer
from blog.serializers import UserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, _):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class UserProfiles(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile = Profile.objects.get_or_create(user_id=user)[0]
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile = Profile.objects.get_or_create(user_id=user)[0]
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
