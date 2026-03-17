from django.contrib import admin
from .models import Contact, CardText


# Register your models here.
@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


# --------------
# Card Text
# ---------------
@admin.register(CardText)
class CardText(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'image_name')

    def short_content(self, obj):
        content = obj.content or ""
        return content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"
