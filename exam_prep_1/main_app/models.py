from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.mixins import LastUpdatedMixin, AwardMixin


class Base(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )


class Director(Base):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )


class Actor(Base, AwardMixin, LastUpdatedMixin):
    pass


class Movie(AwardMixin, LastUpdatedMixin):
    class GenresChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GenresChoices,
        default=GenresChoices.OTHER,
    )

    rating = models.DateField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(10.0)],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movie_director',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_movies',
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='actor_movies',
    )