from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from main_app.custom_manager import AstronautManager
from main_app.mixins import NameMixin, UpdateAtMixin, LaunchDateMixin


class Astronaut(NameMixin, UpdateAtMixin):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex='^\d+$')]
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdateAtMixin, LaunchDateMixin):
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )


class Mission(NameMixin, UpdateAtMixin, LaunchDateMixin):
    class SatusChoices(models.TextChoices):
        PLANED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=SatusChoices.choices,
        default=SatusChoices.PLANED,
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions',
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanders',
    )

