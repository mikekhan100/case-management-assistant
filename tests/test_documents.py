from pathlib import Path


def test_upload_document_success(client):
    # First create a target case
    case_res = client.post("/api/v1/cases", json={"title": "Doc Upload Test Case"})
    case_id = case_res.json()["id"]

    # Upload file from our synthetic case-001 dataset
    sample_file_path = Path("data/test-cases/case-001/01_complaint_letter.txt")
    
    with open(sample_file_path, "rb") as file_bytes:
        files = {"file": ("01_complaint_letter.txt", file_bytes, "text/plain")}
        response = client.post(f"/api/v1/cases/{case_id}/documents", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["case_id"] == case_id
    assert data["filename"] == "01_complaint_letter.txt"
    assert data["file_size"] > 0


def test_upload_document_case_not_found(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    files = {"file": ("test.txt", b"sample content", "text/plain")}
    response = client.post(f"/api/v1/cases/{non_existent_id}/documents", files=files)
    assert response.status_code == 404