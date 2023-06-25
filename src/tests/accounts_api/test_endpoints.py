class TestAccountsEndpoints:
    END_POINT = "/api/accounts/users/'"

    def test_retrieve_all_users(self, users, api_client):
        response = api_client.get(self.END_POINT)
        print(response.data)
        assert response.status_code == 200

    def test_api_work(self):
        assert 1 == 1
