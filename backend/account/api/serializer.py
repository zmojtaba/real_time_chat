from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from ..models.profile import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from django.contrib.auth import get_user_model



from utilss.user_auth import user_utils
from utilss.user_message import io




User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)
    class Meta:
        model = User
        fields =[ 'username', 'password', 'password1']
    


    def validate(self, attrs):

        user_utils.username_validation( attrs['username'] )

        if attrs.get('password') != attrs.get('password1'):
            io._error('Password does not match')
        try:
            validators.validate_password(password=attrs.get('password'))
        
        except exceptions.ValidationError as e:
            raise io._error( list(e.messages) )
        
        return super(UserRegistrationSerializer, self).validate(attrs)
    def create(self, validated_data):

        user_data = user_utils.detect_username(validated_data['username'])
        if user_data['email']:
            user = User.objects.create( 
                    username=validated_data['username'],            
                    email = user_data['email']
                )
        else: 
            user = User.objects.create(
                username = validated_data['username'],
                phone = user_data['phone']
            )

        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()



class UserLoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        user = User.objects.filter(username=attrs.get('username'))
        if not user:
            io._error("No active account found with the given credentials")

        try:
            data = super().validate(attrs)
            data['username'] = self.user.username

            return data
        except:
            io._error("Invalid password")



class ProfileImageSerializer(serializers.ModelSerializer):
    image  = serializers.CharField()
    class Meta:
        model = ProfileImage
        fields = ('image',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user', )
        
    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user_id'] = user.id
        address = Address.objects.create(**validated_data)
        Profile.objects.get(user= user).address.add(address)
        return address

class UploadResumeSerializer(serializers.ModelSerializer):
    # file  = serializers.FileField()
    class Meta:
        model = PdfResume
        fields = ('file', )

    def validate(self, attrs):
        if str(attrs.get('file')).split('.')[-1] != 'pdf':
            io._error('Please ensure that the resume file is saved in the PDF format.')

        return super(UploadResumeSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = self.context.get("request").user
        resume = PdfResume.objects.filter(user=user)
        if resume:
            resume.delete()

        validated_data['user'] = user
        resume = PdfResume.objects.create(**validated_data)
        return resume

class ProfileSerializer(serializers.ModelSerializer):
    images = serializers.CharField(source="get_profile_images")
    address = AddressSerializer(many=True)
    uploaded_resume = UploadResumeSerializer()
    class Meta:
        model = Profile
        fields = [ 'first_name', 'last_name', 'description', 'images', 'address', 'uploaded_resume' ] 

class EditProfileSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(allow_empty_file=True, use_url=True),
        write_only = True,
        required=False
    )

    def update(self, instance, validated_data):
        if validated_data.get('uploaded_images'):
            uploaded_images = validated_data.pop('uploaded_images')
            for image in uploaded_images:
                ProfileImage.objects.create(profile_id=instance.id, image=image)

        profile = Profile.objects.update(**validated_data)
        
        return profile

    class Meta:
        model = Profile
        fields = [ 'first_name', 'last_name', "description", 'uploaded_images' ]

    









