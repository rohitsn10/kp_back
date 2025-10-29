## Upload Documents API

This module provides endpoints to upload and manage documents related to HOTO (Handing Over, Taking Over) processes.

### Endpoints

#### 1. Upload Documents (Create)
- **URL:** `/api/hoto_module/upload_document`
- **Method:** `POST`
- **Authentication:** Required (Token/JWT)
- **Request Body (multipart/form-data):**
	- `project_id` (int, required): Project identifier.
	- `document_id` (int, required): Document type identifier.
	- `category_id` (int, required): Document category identifier
    - `file` (file[], required)
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.
	- `data` (object): Uploaded document details.

- **URL:** `/api/hoto_module/upload_document`
- **Method:** `PUT` or `PATCH`
- **Authentication:** Required
- **Request Body (multipart/form-data):**
	- `project_id` (int, required)
	- `document_id` (int, required)
	- `file` (file[], required)
- **Response:**
	- `status` (bool)
	- `message` (string)
	- `data` (object): Updated document details

### Notes
- Both endpoints require authentication.
- Files are linked to the `HotoDocument` instance.
- On error, a descriptive message is returned.
