def test_index_ok(client):
    response = client.get('/banana')  # Doesn't exist
    assert response.status_code == 200
