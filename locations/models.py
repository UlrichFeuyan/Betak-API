from django.db import models

from accounts.models import Users
from logements.models import Logement


class Location(models.Model):
    is_exist = models.BooleanField(default=True)
    commentaire = models.CharField(max_length=255)
    id_user_locataire = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_user_proprietaire = models.ForeignKey(Users, related_name='locations_proprietaire', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Location {self.id_location}"


class ConditionBail(models.Model):
    montant_caution = models.FloatField()
    id_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    id_logement = models.ForeignKey(Logement, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Condition Bail {self.id_condition_bail}"


