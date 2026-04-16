from django.contrib import admin
from .models import Profile # Import your model
from unfold.admin import ModelAdmin
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):

    list_display = ("user", "first", "surname", "phone", "activation")
    search_fields = ("user__username", "phone")
    list_filter = ("activation",)
    
    # Using fieldsets to group inputs nicely
    fieldsets = (
        (None, {
            "fields": ("user", "image"),
        }),
        ("Personal Information", {
            "fields": (("first", "surname"), "phone"),
        }),
        ("Account Status", {
            "fields": ("activation",),
        }),
    )

