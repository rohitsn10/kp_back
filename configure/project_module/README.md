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

---

### 3. Update Project Progress
**Endpoint:** `/project_module/update_progress/<project_id>/`

**Method:** `PUT`

**Description:** Updates the details of a specific progress entry for a project.

**Headers:**
- `Authorization: Bearer <your_access_token>`
- `Content-Type: application/json`

**Body Parameters:**
- `progress_id` (required): The ID of the progress entry to update.
- Other fields to update (e.g., `particulars`, `status`, `days_to_complete`, etc.).

**Response:**
- `200 OK`: Progress entry updated successfully.
- `400 Bad Request`: Missing or invalid parameters.
- `403 Forbidden`: Authentication required.
- `404 Not Found`: Progress entry not found.

**Example cURL Command:**
```bash
curl -X PUT "http://127.0.0.1:8000/project_module/update_progress/<project_id>/" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "progress_id": 123,
    "particulars": "Updated Task",
    "status": "In Progress",
    "days_to_complete": 5
}'
```

---

### 4. Assign Roles to Project
**Endpoint:** `/project_module/assign_project_roles/<project_id>`

**Method:** `PUT`

**Description:** Assigns roles to users for a specific project. Allows assigning multiple roles to a user within the same project.

**Headers:**
- `Authorization: Bearer <your_access_token>`
- `Content-Type: application/json`

**Body Parameters:**
- `assigned_users` (required): A list of dictionaries containing the role and user IDs to assign. Each dictionary should have the following keys:
  - `role` (string, required): The role to assign (e.g., "Project Manager").
  - `user_ids` (list of integers, required): The IDs of the users to assign the role to.

**Example Request Body:**
```json
{
    "assigned_users": [
        {"role": "Project Manager", "user_ids": [1, 2, 3]},
        {"role": "Project Assistant", "user_ids": [4, 5]}
    ]
}
```

**Response:**
- `200 OK`: Roles assigned successfully.
- `400 Bad Request`: Missing or invalid parameters.
- `403 Forbidden`: Authentication required.
- `404 Not Found`: Project or user not found.

**Example cURL Command:**
```bash
curl -X PUT "http://127.0.0.1:8000/project_module/assign_project_roles/123" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "assigned_users": [
        {"role": "Project Manager", "user_ids": [1, 2, 3]},
        {"role": "Project Assistant", "user_ids": [4, 5]}
    ]
}'
```

### 5. Get Project task History

**Endpoint:** /project_module/get_project_task_history/<project_task_id>/

**Method:** GET

**Description:** Retrieves the history of changes for a specific project task.

**Headers:**

- Authorization: Bearer <your_access_token>
- Content-Type: application/json

**Path Parameters:**

- progress_id: The ID of the project progress entry.

**Response:**

- 200 OK: Returns the history of changes as a JSON array.
- 403 Forbidden: Authentication required.
- 404 Not Found: Progress entry not found.

**Example Response:**
```json
{
    "status": true,
    "data": [
        {
            "field_name": "status",
            "old_value": "not_started",
            "new_value": "in_progress",
            "changed_by": "user1",
            "changed_at": "2025-11-08T12:00:00Z"
        },
        {
            "field_name": "remarks",
            "old_value": "Initial remarks",
            "new_value": "Updated remarks",
            "changed_by": "user2",
            "changed_at": "2025-11-08T12:01:00Z"
        }
    ]
}
```

**Example cURL Command:**
```bash
curl -X GET "http://127.0.0.1:8000/project_module/get_project_task_history/<project_task_id>/" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json"
```

### 6. Delete Activity Sheet

```bash 
curl --location --request DELETE 'http://127.0.0.1:8000/project_module/delete_activity_sheet/6' \
--header 'Authorization: ••••••'
```


### 7. Export Activity Sheet

```bash
curl --location 'http://127.0.0.1:8000/project_module/export_project_progress_sheet/6' \
--header 'Authorization: Bearer Token'
```
### Response
```json
{
    
    "status": true,
    "message": "Project progress report generated successfully",
    "file_url": "http://127.0.0.1:8000/media/project/activity_sheet/project_progress_export_6_20251214_032516.xlsx",
    "total_records": 212
}
```

