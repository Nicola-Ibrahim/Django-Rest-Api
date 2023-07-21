from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model

from src.apps.accounts.api.serializers import serializers
from src.apps.accounts.models import models, profiles


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
    user_strategy = from_model(models.User)

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(teacher=from_model(models.Teacher))
    def test_serialize_teacher_instance(self, teacher, rf):
        """Test serializing User instance to json."""

        request = rf.get("/")
        serializer = serializers.UserDetailsSerializer(
            instance=teacher, context={"request": request}
        )

        expected_data = {
            "id": str(teacher.id),
            "email": teacher.email,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "is_staff": teacher.is_staff,
            "is_active": teacher.is_active,
            "is_verified": teacher.is_verified,
            "is_superuser": teacher.is_superuser,
            "groups": teacher.groups if teacher.groups.values("name") else None,
            "profile": {"num_courses": teacher.teacher_profile.num_courses},
        }

        assert serializer.data == expected_data

    def test_deserialize_json(self, rf):
        """Test deserializing json data into User model (python datatypes)."""

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

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(
        wrong_field=st.one_of(
            st.builds(dict, name=st.text(min_size=25)),
            st.builds(dict, tags=st.text()),
            st.builds(
                dict,
                tags=st.lists(
                    st.text(min_size=25, max_size=25), min_size=1, max_size=1
                ),
            ),
            st.builds(dict, version=st.text(min_size=17, max_size=17)),
            st.builds(dict, is_public=st.integers()),
            st.builds(dict, is_public=st.text()),
        ),
        user=from_model(models.User),
    )
    def test_fail_deserialize_json(self, wrong_field, user, db):
        """Test fail to deserializing json data into User model (python datatypes)."""

        # Get the Teacher model fields
        teacher_model_fields_names = [
            field.name for field in models.Teacher._meta.get_fields()
        ]

        invalid_serialized_data = {
            k: v for k, v in user.__dict__.items() if k in teacher_model_fields_names
        } | wrong_field
        print(invalid_serialized_data)
        print("-" * 40)
        serializer = serializers.TeacherUserCreateSerializer(
            data=invalid_serialized_data
        )

        assert not serializer.is_valid()
        assert serializer.errors != {}
