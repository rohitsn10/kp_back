## API Endpoints

### 1. Upload Project Progress
**Endpoint:** `/project_module/upload_project_progress/`

**Method:** `POST`

**Description:** Uploads an Excel file containing project progress data.

**Headers:**
- `Authorization: Bearer <your_access_token>`
- `Content-Type: multipart/form-data`

**Body Parameters:**
- `file`: The Excel file to upload.
- `project_id`: The ID of the project.

**Response:**
- `200 OK`: Progress data uploaded successfully.
- `400 Bad Request`: Missing or invalid parameters.
- `403 Forbidden`: Authentication required.

**Example cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/project_module/upload_project_progress/ \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: multipart/form-data" \
-F "file=@/path/to/your/excel_file.xlsx" \
-F "project_id=<project_id>"
```

---

### 2. Get Project Progress
**Endpoint:** `/project_module/get_progress/`

**Method:** `GET`

**Description:** Retrieves the progress data for a specific project.

**Headers:**
- `Authorization: Bearer <your_access_token>`
- `Content-Type: application/json`

**Query Parameters:**
- `project_id`: The ID of the project.

**Response:**
- `200 OK`: Returns the progress data as a JSON array.
- `400 Bad Request`: Missing or invalid `project_id`.
- `403 Forbidden`: Authentication required.
- `404 Not Found`: Project not found.

**Example cURL Command:**
```bash
curl -X GET "http://127.0.0.1:8000/project_module/get_progress/?project_id=<project_id>" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json"
```