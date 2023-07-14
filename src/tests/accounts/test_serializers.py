import pytest

from src.apps.accounts.api.serializers import serializers
from src.apps.accounts.models import models


class TestUserSerializer:
    def test_serialize_model_instance(self, one_user, rf):
        """Test properly serialize a Model instance"""
        request = rf.get("/")
        serializer = serializers.UserListSerializer(
            instance=one_user, context={"request": request}, many=False
        )
        assert serializer.data

    def test_serialize_model_instances(self, users, rf):
        """Test properly serialize a Model instance"""
        request = rf.get("/")
        serializer = serializers.UserListSerializer(
            instance=users, context={"request": request}, many=True
        )
        assert serializer.data


class TestAdminUserSerializer:
    def test_serialized_data(self, rf):
        """Test inserting json data via serializer
        from json to django model.
        """
        payload = {
            "email": "admin1@gmail.com",
            "password": "admin323",
            "confirm_password": "admin323",
            "phone_number": 4234234,
            "state": "",
            "city": "",
            "street": "",
            "zipcode": None,
            "identification": None,
            "profile": {"section": "sdf"},
        }

        request = rf.get("/")
        serializer = serializers.AdminUserCreateSerializer(
            data=payload, context={"request": request}
        )

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestStudentUserSerializer:
    def test_serialized_data(self, rf):
        """Test inserting json data via serializer
        from json to django model.
        """
        payload = {
            "email": "student@gmail.com",
            "password": "student23",
            "confirm_password": "student23",
            "phone_number": 4234234,
            "state": "",
            "city": "",
            "street": "",
            "zipcode": None,
            "identification": None,
            "profile": {
                "study_hours": 5,
            },
        }

        request = rf.get("/")
        serializer = serializers.StudentUserCreateSerializer(
            data=payload, context={"request": request}
        )

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestTeacherUserSerializer:
    def test_serialized_data(self, rf):
        """Test inserting json data via serializer
        from json to django model.
        """
        payload = {
            "email": "teacher1@gmail.com",
            "password": "teacher123",
            "confirm_password": "teacher123",
            "phone_number": 4234234,
            "state": "",
            "city": "",
            "street": "",
            "zipcode": None,
            "identification": None,
            "profile": {
                "num_courses": 5,
            },
        }

        request = rf.get("/")
        serializer = serializers.TeacherUserCreateSerializer(
            data=payload, context={"request": request}
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

    ml_model_name_max_chars = 134

    @pytest.mark.parametrize(
        "wrong_field",
        (
            {"name": "a" * (ml_model_name_max_chars + 1)},
            {"tags": "tag outside of array"},
            {"tags": ["--------wrong length tag--------"]},
            {"version": "wronglengthversion"},
            {"is_public": 1},
            {"is_public": "Nope"},
        ),
    )
    def test_deserialize_fails(self, one_teacher_user, wrong_field: dict):
        # Get the Teacher model fields
        teacher_model_fields_names = [
            field.name for field in models.Teacher._meta.get_fields()
        ]

        invalid_serialized_data = {
            k: v
            for k, v in one_teacher_user.__dict__.items()
            if k in teacher_model_fields_names
        } | wrong_field

        serializer = serializers.TeacherUserCreateSerializer(
            data=invalid_serialized_data
        )

        assert not serializer.is_valid()
        assert serializer.errors != {}
