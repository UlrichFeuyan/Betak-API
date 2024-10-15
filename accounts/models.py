from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import img_path

class Role(models.Model):
    id_role = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    is_exist = models.BooleanField(default=True)
    nom_role = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_role


class Users(AbstractUser):
    date_naissance = models.DateTimeField()
    genre = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    secret = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255)
    photo = models.ImageField(upload_to=img_path, blank=True, null=True)
    signature = models.BooleanField(default=False)
    certifie = models.BooleanField(default=False)
    id_role = models.ForeignKey(Role, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Chat(models.Model):
    message = models.TextField()
    id_user_env = models.ForeignKey(Users, related_name='chats_envoyes', on_delete=models.CASCADE)
    id_user_recep = models.ForeignKey(Users, related_name='chats_recus', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat from {self.id_user_env} to {self.id_user_recep}"

