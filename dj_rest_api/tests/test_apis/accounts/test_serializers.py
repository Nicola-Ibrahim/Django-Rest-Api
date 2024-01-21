from api.accounts.serializers import UserCreateSerializer, UserListSerializer
from apps.accounts.models import Teacher, User
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(user=from_model(User))
def test_serialize_user_instance(user, rf):
    """Test properly serialize a User instance"""
    request = rf.get("/")
    serializer = UserListSerializer(instance=user, context={"request": request}, many=False)
    assert serializer.data


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(users=from_model(User).flatmap(lambda x: st.lists(st.just(x), min_size=1)))
def test_serialize_user_instances(users, rf):
    """Test properly serialize a list of User instances"""
    request = rf.get("/")
    serializer = UserListSerializer(instance=users, context={"request": request}, many=True)
    assert serializer.data


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(teacher=from_model(Teacher))
def test_serialize_teacher_instance(teacher, rf):
    """Test serializing Teacher instance to json."""
    request = rf.get("/")
    serializer = serializers.UserDetailsSerializer(instance=teacher, context={"request": request})

    expected_data = {
        "id": str(teacher.id),
        "email": teacher.email,
        "first_name": teacher.first_name,
        "last_name": teacher.last_name,
        "is_staff": teacher.is_staff,
        "is_active": teacher.is_active,
        "is_verified": teacher.is_verified,
        "is_superuser": teacher.is_superuser,
        "groups": teacher.groups.values("name") if teacher.groups.exists() else None,
        "profile": {"num_courses": teacher.teacher_profile.num_courses},
    }

    assert serializer.data == expected_data


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    payload=st.fixed_dictionaries(
        {
            "email": st.text(),
            "password": st.text(),
            "confirm_password": st.text(),
            "phone_number": st.integers(),
            "state": st.text(),
            "city": st.text(),
            "street": st.text(),
            "zipcode": st.none() | st.integers(),
            "identification": st.none() | st.text(),
            "profile": st.fixed_dictionaries({"num_courses": st.integers()}),
        }
    )
)
def test_deserialize_json(payload, rf):
    """Test deserializing json data into Teacher model."""
    request = rf.get("/")
    serializer = serializers.TeacherUserCreateSerializer(data=payload, context={"request": request})

    assert serializer.is_valid()
    assert serializer.errors == {}


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    wrong_field=st.one_of(
        st.builds(dict, name=st.text(min_size=25)),
        st.builds(dict, tags=st.text()),
        st.builds(
            dict,
            tags=st.lists(st.text(min_size=25, max_size=25), min_size=1, max_size=1),
        ),
        st.builds(dict, version=st.text(min_size=17, max_size=17)),
        st.builds(dict, is_public=st.integers()),
        st.builds(dict, is_public=st.text()),
    ),
    teacher=from_model(Teacher),
)
def test_fail_deserialize_json(wrong_field, teacher, db):
    """Test fail to deserializing json data into Teacher model."""
    # Get the Teacher model fields
    teacher_model_fields_names = [field.name for field in Teacher._meta.get_fields()]

    invalid_serialized_data = {
        k: v for k, v in teacher.__dict__.items() if k in teacher_model_fields_names
    } | wrong_field
    serializer = serializers.TeacherUserCreateSerializer(data=invalid_serialized_data)

    assert not serializer.is_valid()
    assert serializer.errors != {}
