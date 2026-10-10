# REST API Specification

This document defines the HTTP endpoints, payload contracts and status codes for the Case Management Assistant API.

---

## Endpoint Summary

| Method | Endpoint | Description | Scope |
| --- | --- | --- | --- |
| `POST` | `/api/v1/cases` | Create a new case container | MVP |
| `GET` | `/api/v1/cases` | List all cases | MVP |
| `GET` | `/api/v1/cases/{case_id}` | Retrieve details of a specific case | MVP |
| `POST` | `/api/v1/cases/{case_id}/documents` | Upload a document file to a case | MVP |
| `GET` | `/api/v1/cases/{case_id}/documents` | List documents attached to a case | MVP |
| `POST` | `/api/v1/cases/{case_id}/summary` | Trigger or generate a case summary | MVP |
| `GET` | `/api/v1/cases/{case_id}/summary` | Retrieve existing case summary | MVP |
| `GET` | `/api/v1/cases/{case_id}/timeline` | Retrieve chronological case events | Version 2 |

---

## Endpoint Details

### 1. Create Case
* **`POST /api/v1/cases`**
* **Request Body:**
  ```json
  {
    "title": "Apex Engineering Pension Scheme Investigation",
    "description": "Non-payment of contributions."
  }

* **Response (201 Created):**
```json
{
  "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "reference_number": "CAS-2026-0001",
  "title": "Apex Engineering Pension Scheme Investigation",
  "description": "Non-payment of contributions.",
  "status": "NEW",
  "created_at": "2026-10-10T20:30:00Z",
  "updated_at": "2026-10-10T20:30:00Z"
}
```

### 2. Upload Document
* **POST /api/v1/cases/{case_id}/documents**
* **Content-Type: multipart/form-data**
* **Form Field: file (Binary file data, .txt or .pdf)**

* **Response (201 Created):**
```json
{
  "id": "e3b0c442-98fc-11ee-b9d1-0242ac120002",
  "case_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "filename": "01_complaint_letter.txt",
  "file_size": 842,
  "mime_type": "text/plain",
  "uploaded_at": "2026-10-10T20:32:00Z"
}
```

### 3. Generate Case Summary
* **POST /api/v1/cases/{case_id}/summary**

* **Response (200 OK):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
  "case_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "content": "Case involves unpaid employee pension contributions for Apex Engineering Ltd from October 2024 to January 2025",
  "model_version": "baseline-v1",
  "created_at": "2026-10-10T20:35:00Z"
}
```

