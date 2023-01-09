from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import random
import requests

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, DataAndFiles
from rest_framework.renderers import (
    HTMLFormRenderer,
    JSONRenderer,
    BrowsableAPIRenderer,
)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer, RegisterSerializer, AdminUserIdentSerializer, UserIdentSerializer
from accounts.models import Profile, UserIdentDocs


class RegisterApiView(generics.GenericAPIView):
    """Creates new user with the given info and credentials"""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Register class
        """

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
        serializer = self.serializer_class(profile_obj, partial=True)
        serializer.initial_data["user"] = self.request.user
        if serializer.initial_data["phone_number"] != "":
            if serializer.is_valid(raise_exception=True):
                rand_integer = random.randint(0, 999999)
                queryset.rand_int = rand_integer
                queryset.save()
                # url api kavenegar
                # url =""
                # payload = {"receptor":,"message":queryset.rand_int}
                # answer = requests.post(url,data=payload)
                # if requests.post["verify_number"] == queryset.rand_int:
                    # profile_obj.is_verified = True
                    # profile_obj.save()
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


    def retrive(self, request,pk=None):
        queryset = Profile.objects.all()
        profile_obj = get_object_or_404(queryset, pk=pk)
        if profile_obj.is_verified ==True:
            serializer = self.serializer_class(profile_obj)
            return Response(serializer.data)
        else:
            return Response({"detail":"your profile is not verified yet"})

    def create(self,request):
        serializer = self.serializer_class(request.data, user=self.request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail":"your docs has been uploaded successfully"})
        else:
            return Response({"detail":"invalid data"})