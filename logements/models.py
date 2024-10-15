from django.db import models

from utils import img_path

class TypeLogement(models.Model):
    libelle = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle


class Position(models.Model):
    libelle = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle


class Logement(models.Model):
    edge_left = models.FloatField()
    edge_right = models.FloatField()
    dimension = models.FloatField()
    id_type_logement = models.ForeignKey(TypeLogement, on_delete=models.CASCADE)
    id_position = models.ForeignKey(Position, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Logement {self.id_logement}"


class Piece(models.Model):
    photo = models.BinaryField()
    montant_du_piece = models.FloatField()
    dimension = models.FloatField()
    id_logement = models.ForeignKey(Logement, on_delete=models.CASCADE)
    id_type_piece = models.ForeignKey('TypePiece', on_delete=models.CASCADE)
    id_condition = models.ForeignKey('Condition', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Piece {self.id_piece}"


class TypePiece(models.Model):
    libelle = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle


class Condition(models.Model):
    libelle = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle


class Option(models.Model):
    is_present = models.BooleanField(default=False)
    balcon = models.BooleanField(default=False)
    is_meuble = models.BooleanField(default=False)
    is_parking = models.BooleanField(default=False)
    surface_balcon = models.FloatField(null=True, blank=True)
    ascenseur = models.BooleanField(default=False)
    terrasse = models.BooleanField(default=False)
    jardin = models.BooleanField(default=False)
    piscine = models.BooleanField(default=False)
    route_pavee = models.BooleanField(default=False)
    distance_route = models.FloatField(null=True, blank=True)
    groupes_elec = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Option {self.id_option}"
