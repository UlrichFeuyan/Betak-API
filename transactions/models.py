from django.db import models

from accounts.models import Users
from logements.models import Logement


class Transaction(models.Model):
    montant = models.FloatField()
    libelle = models.CharField(max_length=255)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_logement = models.ForeignKey(Logement, on_delete=models.CASCADE)
    id_type_transaction = models.ForeignKey('TypeTransaction', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Transaction {self.id_transaction} - {self.montant}"


class TypeTransaction(models.Model):
    nom_operateur = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_operateur
