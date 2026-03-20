from django.contrib import admin
from .models import Contact, CardText, Places, Comment


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


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('destinations', 'short_content', 'image_name')

    def short_content(self, obj):
        content = obj.content or ""
        return content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_preview', 'user', 'created_at')

    def comment_preview(self, obj):
        preview = obj.text or ""
        return preview[:20] + ("..." if len(obj.text) > 20 else "")
    comment_preview.short_description = "Preview"
