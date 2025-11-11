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