def test_retrieve_all_users(users, api_client):
    END_POINT = ""
    api_client.get(END_POINT + "/api//users/")
