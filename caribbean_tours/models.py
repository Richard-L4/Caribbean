from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=30)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} | {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class CardText(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image_name = models.CharField(
        max_length=100,
        help_text="Enter file name (eg Alicante.jpg)",
        default="default.jpg",
        blank=True
    )

    saved_by = models.ManyToManyField(User,
                                      related_name="saved_cards", blank=True)

    def __str__(self):
        return self.title or f"Card for {self.image_name}"
