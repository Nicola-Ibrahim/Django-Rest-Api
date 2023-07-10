import json


class TestAccountsEndpoints:
    END_POINT = "/api/accounts/"

    def test_list_users(self, users, api_client):
        response = api_client.get(path=self.END_POINT)
        assert response.status_code == 200
        assert len(users) == 3

    def test_create_teacher_user(self, db, api_client):
        url = f"{self.END_POINT}teacher/create/"
        user_data = {
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
        response = api_client.post(path=url, data=user_data, format="json")
        assert response.status_code == 201
        assert response.data["data"] == expected_data

    def test_retrieve_user(self, one_user, api_client):
        url = f"{self.END_POINT}{one_user.id}/"
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
        response = api_client.get(url)
        response.data["data"].pop("id")
        assert response.status_code == 200
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
        print(one_teacher_user)
        url = f"{self.END_POINT}{one_teacher_user.id}/"
        response = api_client.put(path=url, data=update_by, format="json")
        assert response.status_code == 200
        # assert response.data["data"] == expected_data

    # def test_delete(self, one_user, api_client):
    #     url = f"{self.END_POINT}/{one_user.id}"
    #     response = api_client.delete(url)
    #     assert response.status_code == 204

    # def test_full_name(self, db, user1):
    #     assert user1.get_full_name() == "Django D"

    # def test_set_password(self, db, user1):
    #     user1.set_password("Django au")
    #     assert user1.check_password("Django au") is True
