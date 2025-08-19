from django.contrib import admin
from myapp.models import User,BOOK
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):


    list_display = ["id","email", "name","tc", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []
 
admin.site.register(User, UserAdmin)

class BookAdmin(admin.ModelAdmin):
    model=BOOK
    fields=['name','price','published_date','author']
admin.site.register(BOOK,BookAdmin)