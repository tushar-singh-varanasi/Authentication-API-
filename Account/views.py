from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerilizer,Userloginserilaizer,UserProfileSerializer,UserChangepasswordSerilizer,SendPasswordResetserializer,UserPasswordReseSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.
#generate token 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistration(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        Serilizer=UserSerilizer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        user=Serilizer.save()
        token=get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration Successfuly'},
        status=status.HTTP_201_CREATED)
        
        
class UserLogin(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        Serilizer=Userloginserilaizer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        email=Serilizer.data.get('email')
        password=Serilizer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_error':['Email or password not match']}},status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        Serilizer=UserProfileSerializer(request.user)
        return Response(Serilizer.data,status=status.HTTP_200_OK)

class UserChangePassword(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        Serilizer=UserChangepasswordSerilizer(data=request.data, context={'user':request.user})
       
        if Serilizer.is_valid(raise_exception=True):
            return Response({'msg':'password change successfuly'},status.HTTP_200_OK)
        return Response(Serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmail(APIView):
    # renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        Serilizer=SendPasswordResetserializer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        return Response({'msg':'password resent link send please check your email'},status=status.HTTP_200_OK)



class UserPasswordReset(APIView):
     def post(self,request,uid,token,format=None):
        Serilizer=UserPasswordReseSerializer(data=request.data,context={'uid':uid,'token':token})
        Serilizer.is_valid(raise_exception=True)
        return Response({'msg':'password reset successfully'},status=status.HTTP_200_OK)
