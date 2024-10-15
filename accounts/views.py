from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Role, Users, Chat
from .serializers import RoleSerializer, UsersSerializer, ChatSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .serializers import UsersSerializer, ChangePasswordSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

User = get_user_model()
user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email address"),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="First name"),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
    }
)

# Vue pour l'enregistrement d'un nouvel utilisateur
class CreateAccountView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Permet à quiconque d'accéder à cette vue pour créer un compte

    @swagger_auto_schema(
        operation_description="Create a new user",
        tags=['Accounts'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Desired username"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
            },
            example={
                'username': 'newuser',
                'password': 'strongpassword',
                'email': 'newuser@example.com'
            }
        ),
        responses={
            201: openapi.Response(description="User created", schema=user_schema),
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Enregistrer l'utilisateur (create)
        self.perform_create(serializer)
        
        # Générer la réponse personnalisée
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "User account created successfully",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


# View for logging in (uses JWT)
class LoginView(TokenObtainPairView):
    permission_classes = []
    
    @swagger_auto_schema(
        operation_description="Authenticates a user and returns an access and refresh token.",
        tags=['Accounts'],
        responses={200: openapi.Response('Successful Login', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                'access': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ))},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# View for logging out (blacklisting the refresh token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logs out the user by blacklisting the refresh token.",
        tags=['Accounts'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="The refresh token to blacklist"),
            },
        ),
        responses={
            205: "Logout successful",
            400: "Invalid refresh token or error",
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for changing the password
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_description="Allows a user to change their password.",
        tags=['Accounts'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description="The current password"),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description="The new password"),
            },
        ),
        responses={
            200: "Password changed successfully",
            400: "Bad Request or invalid old password",
        }
    )
    def get_object(self, queryset=None):
        return self.request.user


# Custom token refresh view (if you need a custom behavior)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="Refresh JWT Token",
    tags=['Accounts'],  # Group this under 'Accounts' in Swagger
)
def refresh_token_view(request):
    refresh_token = request.data.get('refresh')
    if refresh_token:
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),
        })
    return Response({"detail": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
