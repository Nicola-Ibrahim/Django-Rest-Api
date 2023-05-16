from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models.models import (
    Admin,
    BaseAccountant,
    DeliveryWorker,
    DeliveryWorkerAccountant,
    Doctor,
    Subscription,
    User,
    Warehouse,
    WarehouseAccountant,
)
from .models.profiles import (
    AdminProfile,
    BaseAccountantProfile,
    DeliveryWorkerAccountantProfile,
    DeliveryWorkerProfile,
    DoctorProfile,
    StatisticianProfile,
    WarehouseAccountantProfile,
    WarehouseProfile,
)

# from django.utils.translation import ugettext_lazy as _


@admin.register(
    User,
    Warehouse,
    DeliveryWorker,
    Doctor,
    Admin,
    BaseAccountant,
    WarehouseAccountant,
    DeliveryWorkerAccountant,
)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
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
    list_display = ("email", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        disabled_fields = set()

        # Prevent non admin user from changing some fields
        is_admin = request.user.type == User.Type.ADMIN
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
        is_admin = request.user.type == User.Type.ADMIN  # type: ignore
        if not is_admin:
            return False

        return super().has_delete_permission(request, obj)


# class SectionsInlineAdmin(admin.TabularInline):
#     model = Section
#     # fields = ['name', 'warehouse']

# class ServicesInLineAdmin(admin.TabularInline):
#     model = Service


@admin.register(WarehouseProfile)
class WarehouseProfileAdmin(admin.ModelAdmin):
    """Define admin model for Warehouse User model."""

    list_display = [
        "name",
    ]
    readonly_fields = [
        "name",
    ]
    raw_id_fields = [
        "warehouse",
    ]

    # inlines = [SectionsInlineAdmin, ServicesInLineAdmin]


admin.site.register(
    [
        DoctorProfile,
        DeliveryWorkerProfile,
        BaseAccountantProfile,
        DeliveryWorkerAccountantProfile,
        WarehouseAccountantProfile,
        AdminProfile,
        StatisticianProfile,
        Subscription,
    ]
)
