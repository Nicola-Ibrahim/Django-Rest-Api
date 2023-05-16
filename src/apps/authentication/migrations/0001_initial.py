# Generated by Django 4.1.6 on 2023-05-15 19:31

import apps.authentication.models.managers
import apps.authentication.models.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="email address",
                    ),
                ),
                ("phone_number", models.IntegerField(blank=True, null=True)),
                ("state", models.CharField(blank=True, max_length=50, null=True)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("street", models.CharField(blank=True, max_length=50, null=True)),
                ("zipcode", models.IntegerField(blank=True, null=True)),
                ("identification", models.IntegerField(blank=True, null=True)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Doctor", "doctor"),
                            ("Delivery worker", "delivery worker"),
                            ("Warehouse", "warehouse"),
                            ("Admin", "admin"),
                            ("Statistician", "statistician"),
                            ("Base accountant", "base accountant"),
                            ("Delivery worker accountant", "delivery worker accountant"),
                            ("Warehouse accountant", "warehouse accountant"),
                        ],
                        default="Admin",
                        max_length=50,
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", apps.authentication.models.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(max_length=50)),
                ("value", models.PositiveIntegerField()),
                ("details", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="WarehouseProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        max_length=200, validators=[apps.authentication.models.validators.NameRegexValidator()]
                    ),
                ),
                ("working_hours", models.FloatField()),
                ("profit_percentage", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("Warehouse", models.ManyToManyField(related_name="services", to="authentication.warehouseprofile")),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("warehouse", models.ManyToManyField(related_name="sections", to="authentication.warehouseprofile")),
            ],
        ),
        migrations.CreateModel(
            name="OTPNumber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(max_length=16, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "valid_until",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="The timestamp of the moment of expiry of the saved number.",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otp_number",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="subscription",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="authentication.subscription"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Admin")),
            ],
        ),
        migrations.CreateModel(
            name="BaseAccountant",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Base accountant")),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryWorker",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Delivery worker")),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryWorkerAccountant",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Delivery worker accountant")),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Doctor")),
            ],
        ),
        migrations.CreateModel(
            name="Statistician",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Statistician")),
            ],
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Warehouse")),
            ],
        ),
        migrations.CreateModel(
            name="WarehouseAccountant",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authentication.user",),
            managers=[
                ("objects", apps.authentication.models.managers.ProxyUserManger("Warehouse accountant")),
            ],
        ),
        migrations.AddField(
            model_name="warehouseprofile",
            name="warehouse",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="warehouse_profile",
                to="authentication.warehouse",
            ),
        ),
        migrations.CreateModel(
            name="WarehouseAccountantProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                (
                    "warehouse_accountant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="warehouse_accountant_profile",
                        to="authentication.warehouseaccountant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatisticianProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                (
                    "statistician",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statistician_profile",
                        to="authentication.statistician",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoctorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "first_name",
                    models.CharField(
                        max_length=200, validators=[apps.authentication.models.validators.NameRegexValidator()]
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=200, validators=[apps.authentication.models.validators.NameRegexValidator()]
                    ),
                ),
                (
                    "doctor",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_profile",
                        to="authentication.doctor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryWorkerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "first_name",
                    models.CharField(
                        max_length=200, validators=[apps.authentication.models.validators.NameRegexValidator()]
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=200, validators=[apps.authentication.models.validators.NameRegexValidator()]
                    ),
                ),
                ("distance", models.FloatField(max_length=200)),
                ("duration", models.FloatField()),
                ("profit_percentage", models.FloatField()),
                ("is_idle", models.BooleanField(default=False)),
                (
                    "delivery_worker",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_worker_profile",
                        to="authentication.deliveryworker",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryWorkerAccountantProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                (
                    "delivery_worker_accountant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_worker_accountant_profile",
                        to="authentication.deliveryworkeraccountant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BaseAccountantProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                (
                    "base_accountant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base_accountant_profile",
                        to="authentication.baseaccountant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdminProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin_profile",
                        to="authentication.admin",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="manager",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="authentication.admin"
            ),
        ),
    ]