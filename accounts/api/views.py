from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import random
import requests

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, DataAndFiles
from rest_framework.renderers import (
    HTMLFormRenderer,
    JSONRenderer,
    BrowsableAPIRenderer,
)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer, RegisterSerializer, AdminUserIdentSerializer, UserIdentSerializer,UserWalletSerializer
from accounts.models import Profile, UserIdentDocs



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterApiView(generics.GenericAPIView):
    """Creates new user with the given info and credentials"""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Register class
        """
 # from django.contrib.auth import authenticate, login

# def my_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
        serializer = RegisterSerializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def retrive(self, request, pk=None):
        # fo viewing profile
        queryset = Profile.objects.filter(user=self.request.user)
        profile_obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(profile_obj)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        # add number for verifying profile
        queryset = Profile.objects.filter(user=self.request.user)
        profile_obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(profile_obj, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.data["user"] = self.request.user
            if serializer.data["phone_number"] != "":
                rand_integer = random.randint(100000, 999999)
                profile_obj.rand_int = rand_integer

                # url api kavenegar
                # url =""
                # payload = {"receptor":,"message":queryset.rand_int}
                # answer = requests.post(url,data=payload)
                # if requests.post["verify_number"] == profile_obj.rand_int:
                # profile_obj.is_verified = True
                profile_obj.save()
                # serializer.save()
                return Response({"details": "profile vrified"})


class UserDocAdminViewSet(viewsets.ViewSet):
    """User docs admin view set"""

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdminUserIdentSerializer
    queryset = UserIdentDocs.objects.filter(is_complete=False)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": " Item Created !!"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrive(self, request, pk=None):
        doc_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc_object)
        return Response(serializer.data)

    def update(self, request, pk=None):
        doc_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "item updated !!"})
        else:
            return Response({"detail": "data is not valid"})

    def partial_update(self, request, pk=None):
        doc_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "item updated !!"})
        else:
            return Response({"detail": "data is not valid"})


class ProfileDocsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserIdentSerializer

    def retrive(self, request, pk=None):
        queryset = Profile.objects.filter(user=request.user)
        profile_obj = get_object_or_404(queryset, pk=pk)
        if pk == profile_obj.id:
            if profile_obj.is_verified:
                serializer = self.serializer_class(profile_obj)
                return Response(serializer.data)
            else:
                return Response({"detail": "your profile is not verified yet"})

    def create(self, request):
        serializer = self.serializer_class(request.data, user=self.request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "your docs has been uploaded successfully"})
        else:
            return Response({"detail": "invalid data"})
class UserWalletViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWalletSerializer
    def retrieve(self, request):
        queryset = Profile.objects.get(user = self.request.user)
        profile_obj = get_object_or_404(queryset)
        serializer = self.serializer_class (profile_obj)
        
        return Response(serializer.data)