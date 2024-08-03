from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.custom_managers import CustomManagerTennisPlayer


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)],
    )

    birth_date = models.DateField()

    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
    )

    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)],
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = CustomManagerTennisPlayer()


class Tournament(models.Model):
    class SurfaceTypeChoices(models.TextChoices):
        NOT_SELECTED = "Not Selected", "Not Selected"
        CLAY = "Clay", "Clay"
        GRASS = "Grass", "Grass"
        HARD_COURT = "Hard Court", "Hard Court"

    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
        unique=True,
    )

    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
    )

    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    start_date = models.DateField()

    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceTypeChoices.choices,
        default=SurfaceTypeChoices.NOT_SELECTED,
    )


class Match(models.Model):
    score = models.CharField(
        max_length=100,
    )

    summary = models.TextField(
        validators=[MinLengthValidator(5)],
    )

    date_played = models.DateTimeField()

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='tournament_matches'
    )

    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='player_matches',
    )

    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_match',
    )

    class Meta:
        verbose_name_plural = "Matches"
