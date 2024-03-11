from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model representing a registered user in the system.

    Attributes:
        avatar (ImageField, optional): User's profile picture.
        date_birth (DateField, optional): User's date of birth.

    Methods:
        get_user_age(): Calculate the user's age based on the date of birth.

    """
    avatar = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )
    date_birth = models.DateField(
        blank=True,
        null=True
    )

    def get_user_age(self):
        """
        Calculate the user's age based on the date of birth.

        Returns:
            int: The age of the user.
        """
        if self.date_birth:
            today = date.today()
            age = today.year - self.date_birth.year - ((today.month, today.day) < (self.date_birth.month, self.date_birth.day))
            return age
        return None
