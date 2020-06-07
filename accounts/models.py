from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Participant(models.Model):
    user = models.OneToOneField(to=User, related_name="participant", on_delete=models.CASCADE, null=True)
    contactNumber = models.BigIntegerField(null=True, verbose_name="Contact Number", validators=[
        MaxValueValidator(limit_value=9999999999, message="Phone number Not valid"),
        MinValueValidator(limit_value=1000000000, message="Phone number Not valid")
    ])
    accommodation = models.BooleanField(default=False)
    college = models.CharField(null=True, max_length=500)
    address = models.CharField(null=True, max_length=2000)
    yearOfStudy = models.IntegerField(null=True, default=1, verbose_name="Year of Study", validators=[
        MaxValueValidator(limit_value=5, message="Year Not valid"),
        MinValueValidator(limit_value=1, message="Year Not valid")
    ])
    firstTimer = models.BooleanField(default=True)
    gender = models.IntegerField(null=True, default=0, validators=[
        MaxValueValidator(limit_value=2, message="Gender Not valid"),
        MinValueValidator(limit_value=0, message="Gender Not valid")
    ])

    class Meta:
        permissions = (
            ('allowed_import', "Imports are allowed"),
        )

    def __str__(self):
        return ("Name: " + self.user.first_name + " | " if self.user.first_name else "") + "Username: " + self.user.username


class Team(models.Model):

    name = models.CharField(max_length=100)
    members = models.ManyToManyField(to=User, related_name="team")

    def __str__(self):

        return self.name + " - Events: " + ', '.join([i for i in self.registrations.values_list('registered_event__name', flat=True)])
