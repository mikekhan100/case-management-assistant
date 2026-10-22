def test_create_case_success(client):
    payload = {
        "title": "Apex Engineering Scheme Review",
        "description": "Non-payment of contributions",
    }
    response = client.post("/api/v1/cases", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == "NEW"
    assert "id" in data
    assert "reference_number" in data


def test_create_case_invalid_title(client):
    payload = {"title": ""}  # Empty title violates min_length=1 schema constraint
    response = client.post("/api/v1/cases", json=payload)
    assert response.status_code == 422


def test_list_cases(client):
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_case_not_found(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/cases/{non_existent_id}")
    assert response.status_code == 404