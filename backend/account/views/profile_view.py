from rest_framework.views import APIView
from rest_framework.response import Response
from ..api.serializer import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from utilss.user_message import *
from django.conf import settings

User = get_user_model()

class ProfileView(APIView):
    serializer_class = ProfileSerializer
    parser_class = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(io._success('Profile edited successfully.'))
    
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
        
class PhotoUrlView(APIView):

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user= user)
        serializer = ProfileImageSerializer(data = list(profile.get_profile_images()), many=True, context={"request":request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    

# adding address updating and deleting
class AddressView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        address = Address.objects.filter(user = user).order_by('-id')
        if address.exists():
            serializer = self.serializer_class(address, many=True)
            return Response(serializer.data)
        else:
            return Response(io._error('You have not set an address yet.'))

    def post(self, request):
        #  add address from map should add to it.
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(io._success('Address added successfully.'))
    
    def put(self, request):
        request.data._mutable=True
        address_id = request.data.pop('address_id')[0]
        address = Address.objects.get(id = address_id)
        serializer = self.serializer_class(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(io._success('Your address Updated successfully.'))
    
    def delete(self, request):
        address = Address.objects.get(id = request.data['address_id'])
        address.delete()
        return Response(io._success('Address deleted successfully.'))




class UploadResumeView(APIView):
    serializer_class = UploadResumeSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):

        try:
            resume = PdfResume.objects.get(user=request.user)
            serializer = self.serializer_class(resume)
            return Response({'file': settings.DOMAIN_URL + serializer.data['file']})
        except:
            io._error('You have not uploaded your resume.')

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(io._success("Your resume uploaded successfully."))
        



