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
`GET /get_milestone`

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
  http://<your-domain>/get_milestone?project_id=1&start_date=2025-11-01&end_date=2025-11-30 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Update Milestone API

### URL
`PUT /update_milestone/<milestone_id>`

### Description
This API is used to update an existing milestone.

### Request Headers
- `Authorization`: Bearer <JWT_TOKEN>

### Request Body
```json
{
    "milestone_name": "Updated Milestone Name",
    "milestone_description": "Updated description of the milestone",
    "start_date": "2025-11-01T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z",
    "project_progress_list": [1, 2, 3]
}
```

### Response
#### Success Response
```json
{
    "status": true,
    "message": "Milestone updated successfully"
}
```

#### Error Response
```json
{
    "status": false,
    "message": "<Error message>",
    "error": "<Detailed error message>"
}
```

### CURL Command
```bash
curl -X PUT \
  http://<your-domain>/update_milestone/1 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "milestone_name": "Updated Milestone Name",
    "milestone_description": "Updated description of the milestone",
    "start_date": "2025-11-01T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z",
    "project_progress_list": [1, 2, 3]
  }'
```

## Delete Milestone API

### URL
`DELETE /delete_milestone/<milestone_id>`

### Description
This API is used to delete an existing milestone.

### Request Headers
- `Authorization`: Bearer <JWT_TOKEN>

### Response
#### Success Response
```json
{
    "status": true,
    "message": "Milestone deleted successfully."
}
```

#### Error Response
```json
{
    "status": false,
    "message": "<Error message>",
    "data": []
}
```

### CURL Command
```bash
curl -X DELETE \
  http://<your-domain>/delete_milestone/1 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Add Payment on Milestone API

### Endpoint
**POST** `/add_payment_on_milestone`

### Description
This API allows you to add a payment for a specific milestone. It validates the payment amount to ensure it does not exceed the total amount of the inflow payment and dynamically updates the pending amount. Additionally, users can upload files as attachments with the payment.

### Request Body
```json
{
    "inflow_payment": 1,
    "amount_paid": 5000.00,
    "payment_date": "2025-11-13T10:00:00Z",
    "notes": "First installment payment",
    "attachments": [
        "file1.pdf",
        "file2.jpg"
    ]
}
```

### Response
#### Success Response:
**Status Code:** 201 Created
```json
{
    "message": "Payment added successfully",
    "data": {
        "inflow_payment": 1,
        "amount_paid": "5000.00",
        "payment_date": "2025-11-13T10:00:00Z",
        "pending_amount": "3000.00",
        "notes": "First installment payment",
        "attachment_details": [
            {
                "id": 1,
                "file": "/media/payment_attachments/file1.pdf",
                "uploaded_at": "2025-11-13T10:00:00Z"
            },
            {
                "id": 2,
                "file": "/media/payment_attachments/file2.jpg",
                "uploaded_at": "2025-11-13T10:00:00Z"
            }
        ]
    }
}
```

#### Error Response:
**Status Code:** 400 Bad Request
```json
{
    "errors": {
        "non_field_errors": [
            "The total paid amount exceeds the total amount of the inflow payment."
        ]
    }
}
```

### Example cURL Command
```bash
curl -X POST \
  http://127.0.0.1:8000/add_payment_on_milestone/ \
  -H "Content-Type: multipart/form-data" \
  -F "inflow_payment=1" \
  -F "amount_paid=5000.00" \
  -F "payment_date=2025-11-13T10:00:00Z" \
  -F "notes=First installment payment" \
  -F "attachments=@/path/to/file1.pdf" \
  -F "attachments=@/path/to/file2.jpg"
```