from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models.user import User, UserProfile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'rol', 'is_active', 'is_staff', 'team')
    list_filter = ('rol', 'is_active', 'is_staff', 'team')
    search_fields = ('email', 'name')
    ordering = ('email',)
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name', 'team', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'rol', 'team', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image_preview')
    search_fields = ('user__email', 'user__name')
    list_per_page = 25
    readonly_fields = ('profile_image_preview',)

    def profile_image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image_url.url)
        return "(Sin imagen)"
    profile_image_preview.short_description = "Imagen de perfil"

admin.site.register(User, CustomUserAdmin)