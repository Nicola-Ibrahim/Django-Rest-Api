from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.forms.models import BaseInlineFormSet

from .models import models, profiles

# from django.utils.translation import ugettext_lazy as _


# Define an inline admin descriptor for the profile model


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "state",
                    "city",
                    "street",
                    "zipcode",
                    "identification",
                    "manager",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "type",
                )
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        disabled_fields = set()

        # Prevent non admin user from changing some fields
        is_admin = request.user.type == models.User.Type.ADMIN
        if not is_admin:
            disabled_fields |= {
                "email",
                "type",
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        return form

    def has_delete_permission(self, request, obj=None) -> bool:
        is_admin = request.user.type == models.User.Type.ADMIN  # type: ignore
        if not is_admin:
            return False

        return super().has_delete_permission(request, obj)


class AdminProfileInline(admin.StackedInline):
    # Use the custom inline formset
    model = profiles.AdminProfile
    can_delete = False
    verbose_name_plural = "profile"


@admin.register(models.Admin)
class AdminUserAdmin(UserAdmin):
    """Define admin model for custom User model."""

    inlines = (AdminProfileInline,)


class TeacherProfileInline(admin.StackedInline):
    # Use the custom inline formset
    model = profiles.TeacherProfile
    can_delete = False
    verbose_name_plural = "profile"


@admin.register(models.Teacher)
class TeacherUserAdmin(UserAdmin):
    """Define admin model for custom User model."""

    inlines = (TeacherProfileInline,)


class StudentProfileInline(admin.StackedInline):
    # Use the custom inline formset
    model = profiles.StudentProfile
    can_delete = False
    verbose_name_plural = "profile"


@admin.register(models.Student)
class StudentUserAdmin(UserAdmin):
    """Define admin model for custom User model."""

    inlines = (StudentProfileInline,)


admin.site.register(profiles.TeacherProfile)
