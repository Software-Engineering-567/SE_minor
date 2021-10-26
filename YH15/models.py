from typing import Union, NewType

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

Numeric = NewType('Numeric', Union[float, int])


class Bar(models.Model):
    MAX_BAR_CAPACITY: int = 1000
    MAX_BAR_RATING: float = 5.0

    bar_name = models.CharField(max_length=200)

    bar_rating = models.FloatField(
        default=0.0,
    )

    bar_capacity = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(1000), MinValueValidator(0)]
    )

    bar_occupancy = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(bar_capacity), MinValueValidator(0)]
    )

    def __eq__(self, other) -> bool:
        if isinstance(other, Bar):
            return self.bar_name == other.bar_name and self.bar_rating == other.bar_rating and self.bar_capacity == other.bar_capacity and self.bar_occupancy == other.bar_occupancy
        return False

    def __hash__(self) -> int:
        return hash(self.bar_name) + hash(self.bar_rating)

    def clean_fields(self, exclude=None) -> None:
        if self.bar_rating < 0 or self.bar_rating > self.MAX_BAR_RATING:
            raise ValidationError(f'Invalid bar rating value {self.bar_rating}')

        if self.bar_capacity < 0 or self.bar_capacity > self.MAX_BAR_CAPACITY:
            raise ValidationError(f"Invalid bar capacity value {self.bar_capacity}")

        if self.bar_occupancy < 0 or self.bar_occupancy > self.bar_capacity:
            raise ValidationError(f"Invalid bar occupancy value {self.bar_occupancy}")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Bar, self).save(*args, **kwargs)

    def check_enough_occupancy(self, n: int) -> bool:
        return self.bar_occupancy + n <= self.bar_capacity

    def add_customers(self, n: int) -> None:
        if not self.check_enough_occupancy(n):
            raise ValueError(f"Cannot add {n} more customers to the bar!")
        self.bar_occupancy += n

    def customers_leave(self, n: int) -> None:
        if self.bar_occupancy - n < 0:
            raise ValueError(f"Less {n} customers in the bar!")
        self.bar_occupancy -= n

    @property
    def occupant_rate(self):
        return self.bar_occupancy / self.bar_capacity
