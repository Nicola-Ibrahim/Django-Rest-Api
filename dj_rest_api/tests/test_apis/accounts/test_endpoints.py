from rest_framework.reverse import reverse
from rest_framework import status


class TestAccountsEndpoints:
    END_POINT = "/api/accounts/"

    def test_list_users(self, users, api_client):
        # Ensure that the list endpoint returns a 200 status code
        response = api_client.get(path=self.END_POINT)
        assert response.status_code == status.HTTP_200_OK

        # Ensure that the correct number of users is returned
        assert len(response.data) == len(users)

    def test_retrieve_user(self, one_user, api_client):
        # Ensure that the retrieve endpoint returns a 200 status code
        url = reverse("user-detail", args=[one_user.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Ensure that the retrieved user data matches the expected data
        expected_data = {
            "email": "django.d@gmail.com",
            "first_name": "Django",
            "last_name": "D",
            "is_staff": False,
            "is_active": True,
            "is_verified": False,
            "is_superuser": False,
            "groups": None,
            "profile": {
                "admin": None,
                "section": "",
            },
        }
        assert response.data == expected_data

    def test_create_user(self, api_client):
        # Ensure that a new user can be created
        data = {
            "email": "new_user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure_password",
        }
        response = api_client.post(self.END_POINT, data)
        assert response.status_code == status.HTTP_201_CREATED

        # Ensure that the created user data matches the provided data
        created_user = User.objects.get(email=data["email"])
        assert created_user.first_name == data["first_name"]
        assert created_user.last_name == data["last_name"]

    def test_update_user(self, one_user, api_client):
        # Ensure that an existing user can be updated
        url = reverse("user-detail", args=[one_user.id])
        data = {"first_name": "Updated"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

        # Ensure that the updated user data matches the provided data
        updated_user = User.objects.get(id=one_user.id)
        assert updated_user.first_name == data["first_name"]

    def test_delete_user(self, one_user, api_client):
        # Ensure that an existing user can be deleted
        url = reverse("user-detail", args=[one_user.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Ensure that the user is no longer in the database
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=one_user.id)


class TestTeacherAccountsEndpoints:
    END_POINT = "/api/accounts/"

    def test_create_teacher_user(self, db, api_client):
        url = f"{self.END_POINT}teacher/create/"
        payload = {
            "email": "teacher1@gmail.com",
            "password": "teacher123",
            "first_name": "Django",
            "last_name": "D",
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

        expected_data = {
            "email": "teacher1@gmail.com",
            "first_name": "Django",
            "last_name": "D",
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
        response = api_client.post(path=url, data=payload, format="json")
        assert response.status_code == 201
        assert response.data["data"] == expected_data

    def test_update_teacher_user(self, one_teacher_user, api_client):
        update_by = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": "CA",
            "city": "LA",
            "street": "43",
            "zipcode": 444444,
            "identification": 232,
            "profile": {
                "num_courses": 10,
            },
        }

        expected_data = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": "CA",
            "city": "LA",
            "street": "43",
            "zipcode": 444444,
            "identification": 232,
            "profile": {
                "num_courses": 10,
            },
        }
        url = f"{self.END_POINT}{one_teacher_user.id}/"
        response = api_client.put(path=url, data=update_by, format="json")
        assert response.status_code == 200
        assert response.data["data"] == expected_data

    def test_partial_update_teacher_user(self, one_teacher_user, api_client):
        update_by = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "identification": 232,
            "profile": {
                "num_courses": 10,
            },
        }

        expected_data = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": None,
            "city": None,
            "street": None,
            "zipcode": None,
            "identification": 232,
            "profile": {
                "num_courses": 10,
            },
        }
        url = f"{self.END_POINT}{one_teacher_user.id}/"
        response = api_client.patch(path=url, data=update_by, format="json")
        assert response.status_code == 200
        assert response.data["data"] == expected_data


class TestStudentAccountsEndpoints:
    END_POINT = "/api/accounts/"

    def test_create_student_user(self, db, api_client):
        url = f"{self.END_POINT}student/create/"
        payload = {
            "email": "student1@gmail.com",
            "password": "student123",
            "first_name": "Django",
            "last_name": "D",
            "confirm_password": "student123",
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

        expected_data = {
            "email": "student1@gmail.com",
            "first_name": "Django",
            "last_name": "D",
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
        response = api_client.post(path=url, data=payload, format="json")
        assert response.status_code == 201
        assert response.data["data"] == expected_data

    def test_update_student_user(self, one_student_user, api_client):
        update_by = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": "CA",
            "city": "LA",
            "street": "43",
            "zipcode": 444444,
            "identification": 232,
            "profile": {
                "study_hours": 10,
            },
        }

        expected_data = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": "CA",
            "city": "LA",
            "street": "43",
            "zipcode": 444444,
            "identification": 232,
            "profile": {
                "study_hours": 10,
            },
        }
        url = f"{self.END_POINT}{one_student_user.id}/"
        response = api_client.put(path=url, data=update_by, format="json")
        assert response.status_code == 200
        assert response.data["data"] == expected_data

    def test_partial_update_student_user(self, one_student_user, api_client):
        update_by = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "identification": 232,
            "profile": {
                "study_hours": 10,
            },
        }

        expected_data = {
            "first_name": "Java",
            "last_name": "D",
            "phone_number": 34,
            "state": None,
            "city": None,
            "street": None,
            "zipcode": None,
            "identification": 232,
            "profile": {
                "study_hours": 10,
            },
        }
        url = f"{self.END_POINT}{one_student_user.id}/"
        response = api_client.patch(path=url, data=update_by, format="json")
        assert response.status_code == 200
        assert response.data["data"] == expected_data
