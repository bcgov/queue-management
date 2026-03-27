def test_healthz(client):
    response = client.get("/api/v1/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"message": "api is healthy"}


def test_readyz(client):
    response = client.get("/api/v1/readyz")

    assert response.status_code == 200
    assert response.get_json() == {"message": "api is ready"}


def test_info_includes_api_header(client):
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    assert response.get_json() == {"API": "notifications_api/"}
