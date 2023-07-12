from src.apps.accounts.api.serializers import serializers


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
