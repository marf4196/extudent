from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser , DataAndFiles
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer, RegisterSerializer, AdminUserIdentSerializer
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


class ProfileApiView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj



class UserDocAdminViewSet(viewsets.ViewSet):
    """User docs admin view set"""

    permission_classes = [IsAuthenticated]
    parser_classes = ( MultiPartParser, FormParser)
    serializer_class = AdminUserIdentSerializer
    queryset = UserIdentDocs.objects.filter(is_complete=False)
    
    def list(self, request):
        serializer = self.serializer_class(self.queryset,many=True )
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail":" Item Created !!"},status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def retrive(self,request,pk=None):
        doc_object = get_object_or_404(self.queryset,pk=pk)
        serializer = self.serializer_class(doc_object)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        doc_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc_object, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"item updated !!"})
        else:
            return Response({"detail":"data is not valid"})
        
        
    def partial_update(self, request, pk=None):
        doc_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc_object, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"item updated !!"})
        else:
            return Response({"detail":"data is not valid"})

