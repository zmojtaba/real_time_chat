from django.urls import path, include
from .views.user_auth import *
from .views.profile_view import *
from rest_framework_simplejwt.views import (TokenRefreshView,)


app_name='account'

urlpatterns=[
    path('register/', UserRegistrationApiView.as_view(), name='register' ),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('login/', UserLoginView.as_view(), name='sign_in'),
    path('login/refresh/', TokenRefreshView.as_view(), name='sign_in_refresh'),

    # profile 
    path('profile/', ProfileView.as_view(), name='profile' ),
    path('profile-photo/', PhotoUrlView.as_view(), name='profile_photo' ),
    path('address/', AddressView.as_view(), name='address'),
    path('upload-resume/', UploadResumeView.as_view(), name='upload_resume'),
]
