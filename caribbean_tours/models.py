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

    class Meta:
        verbose_name = 'CardText'
        verbose_name_plural = 'CardTexts'


class Places(models.Model):
    card = models.ForeignKey(CardText,
                             on_delete=models.CASCADE, null=True, blank=True)
    destinations = models.CharField(max_length=50)
    content = models.TextField()
    image_name = models.CharField(
        max_length=100,
        help_text="Enter file name (eg Cancun).",
        default="default.jpg",
        blank=True
    )

    def __str__(self):
        return self.destinations or f"Card for {self.image_name}"

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


class Comment(models.Model):
    places = models.ForeignKey(
        Places,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"


class CommentReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'like'),
        (DISLIKE, 'dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='reactions')
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'comment')
