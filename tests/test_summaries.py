def test_generate_and_get_summary(client):
    # Create case
    case_res = client.post("/api/v1/cases", json={"title": "Summary Test Case"})
    case_id = case_res.json()["id"]

    # Generate summary
    gen_res = client.post(f"/api/v1/cases/{case_id}/summary")
    assert gen_res.status_code == 201
    data = gen_res.json()
    assert data["case_id"] == case_id
    assert "content" in data
    assert data["model_version"] == "baseline-v1"

    # Fetch summary
    get_res = client.get(f"/api/v1/cases/{case_id}/summary")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == data["id"]