## Create Milestone API

### URL
`POST /create_milestone`

### Description
This API is used to create a new milestone for a project.

### Request Headers
- `Authorization`: Bearer <JWT_TOKEN>

### Request Body
```json
{
    "milestone_name": "Milestone 1",
    "project": 1,
    "project_tasks_list": [1, 2, 3],
    "start_date": "2025-11-01T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z",
    "milestone_description": "Description of the milestone",
    "is_depended": true
}
```

### Response
#### Success Response
```json
{
    "status": true,
    "message": "Milestone created successfully"
}
```

#### Error Response
```json
{
    "status": false,
    "message": "<Error message>"
}
```

### CURL Command
```bash
curl -X POST \
  http://<your-domain>/create_milestone \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "milestone_name": "Milestone 1",
    "project": 1,
    "project_progress_list": [1, 2, 3],
    "start_date": "2025-11-01T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z",
    "milestone_description": "Description of the milestone",
    "is_depended": true
  }'
```

## Get Milestones API

### URL
`GET /milestones`

### Description
This API is used to fetch milestones based on optional filters such as project ID, start date, and end date.

### Request Headers
- `Authorization`: Bearer <JWT_TOKEN>

### Query Parameters
- `project_id` (optional): ID of the project to filter milestones.
- `start_date` (optional): Filter milestones created on or after this date (format: YYYY-MM-DD).
- `end_date` (optional): Filter milestones created on or before this date (format: YYYY-MM-DD).

### Response
#### Success Response
```json
{
    "status": true,
    "message": "milestones fetched successfully.",
    "total": 2,
    "data": [
        {
            "id": 1,
            "project": 1,
            "start_date": "2025-11-01T00:00:00Z",
            "end_date": "2025-11-30T23:59:59Z",
            "project_task_list": [1, 2, 3],
            "milestone_name": "Milestone 1",
            "milestone_description": "Description of the milestone",
            "completed_at": null,
            "is_active": true,
            "is_depended": true,
            "milestone_status": "in_progress"
        },
        {
            "id": 2,
            "project": 1,
            "start_date": "2025-12-01T00:00:00Z",
            "end_date": "2025-12-31T23:59:59Z",
            "project_task_list": [4, 5],
            "milestone_name": "Milestone 2",
            "milestone_description": "Another milestone description",
            "completed_at": null,
            "is_active": true,
            "is_depended": false,
            "milestone_status": "pending"
        }
    ]
}
```

#### Error Response
```json
{
    "status": false,
    "message": "Something went wrong",
    "error": "<Error message>"
}
```

### CURL Command
```bash
curl -X GET \
  http://<your-domain>/milestones?project_id=1&start_date=2025-11-01&end_date=2025-11-30 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```