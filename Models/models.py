import json

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from Licencjat.settings import STATICFILES_DIRS


class AlgorithmModel(models.Model):
    TYPE_CHOICES = (
        ("1", "LinearAdding"),
        ("2", "ExponentialAdding"),
        ("3", "SelectionAverage"),
        ("4", "AverageHumanOffset"),
        ("5", "AttributeWeightsOnTestSample"),
        ("6", "ExponentialAttributeWeightsOnTestSample")
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    photo = models.ForeignKey('PhotoModel', on_delete=models.CASCADE, null=True)
    selection = models.BooleanField(null=True)

class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=39, null=False)
    selection_count = models.IntegerField(null=False, default="0")
    has_finished = models.BooleanField(default=False)
    has_finished_results = models.BooleanField(default=False)

class SelectionModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    photo = models.ForeignKey('PhotoModel', on_delete=models.CASCADE)
    selection = models.BooleanField(null=True)


class PhotoModel(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=10, default="000001.jpg")
    attributes = models.CharField(max_length=200)
    landmarks = models.CharField(max_length=200)

    def set_landmarks(self, x):
        self.landmarks = json.dumps(x)

    def get_landmarks(self):
        return json.loads(self.landmarks)

    def set_attributes(self, x):
        self.attributes = json.dumps(x)

    def get_attributes(self):
        return json.loads(self.attributes)
