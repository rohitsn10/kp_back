## Upload Documents API

This module provides endpoints to upload and manage documents related to HOTO (Handing Over, Taking Over) processes.

### Endpoints

#### 1. Upload Documents (Create)
- **URL:** `/api/hoto_module/upload_document/<int:project_id>`
- **Method:** `POST`
- **Authentication:** Required (Token/JWT)
- **Request Body (multipart/form-data):**
	- `document_id` (int, required): Document type identifier.
	- `status` (string, optional): Status of the document.
	- `remarks` (string, optional): Remarks for the document.
	- `file` (file[], optional): Files to upload.
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.
	- `data` (object): Updated document details.

#### 2. Upload or Update Document
- **URL:** `/api/hoto_module/upload_document/<int:project_id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Body (multipart/form-data):**
	- `document_id` (int, required): Document type identifier.
	- `status` (string, optional): Status of the document.
	- `remarks` (string, optional): Remarks for the document.
	- `file` (file[], optional): Files to upload.
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.
	- `data` (object): Updated document details.

### Notes
- Both endpoints require authentication.
- Files are linked to the `HotoDocument` instance.
- On error, a descriptive message is returned.

### Additional Endpoints

#### 3. Fetch All Documents Names
- **URL:** `/api/hoto_module/fetch_all_documents_names/<project_id>`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.
	- `data` (list): List of documents grouped by category.

#### 4. Delete Particular Document
- **URL:** `/api/hoto_module/delete_document/<project_id>`
- **Method:** `DELETE`
- **Authentication:** Required
- **Request Body (JSON):**
	- `document_id` (list[int], required): List of document IDs to delete.
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.

#### 5. Verify Document
- **URL:** `/api/hoto_module/verify_document/<project_id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Body (JSON):**
	- `document_id` (int, required): Document ID to verify.
	- `status` (string, required): Verification status.
	- `verify_comment` (string, optional): Verification comment.
- **Response:**
	- `status` (bool): Success status.
	- `message` (string): Status message.

## Punch Points API Details

### 1. Raise Punch Points
**Endpoint:**
```
POST /raise_punch_points/<int:project_id>
```
**Description:**
Raise a new punch point for a specific project.
**Request Body:**
- `punch_title` (string): Title of the punch point.
- `punch_description` (string): Description of the punch point.
- `punch_file` (file[]): List of files to attach.

**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (object): Details of the created punch point.

### 2. Completed Punch Points
**Endpoint:**
```
POST /accepted_rejected_punch_points/<int:project_id>
```
**Description:**
Mark a punch point as completed for a specific project.
**Request Body:**
- `punch_id` (integer): ID of the punch point to mark as completed.
- `is_accepted` (boolean) : True if accepted otherwise False
- `punch_description` (string): Description of the completed punch point.
- `tentative_timeline` (datetime): Tentative timeline for completion.
- `comments` (string): Comments from the Project Team.
- `punch_file` (file[]): List of files to attach.

**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (object): Details of the completed punch point.

### 3. Mark Punch Points Completed

**Endpoint:**
```
PUT /mark_punch_points_completed/<int:project_id>
```
**Description:**
Mark a punch point as completed for a specific project.
**Request Body:**
- `completed_punch_id` (integer): ID of the completed punch point.
- `remarks` (string): Remarks for the completed punch point.
- `punch_file` (file[]): List of files to attach.

**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (object): Details of the updated punch point.

### 4. Verify Completed Punch Points
**Endpoint:**
```
PUT /verify_completed_punch_points/<int:project_id>
```
**Description:**
Verify a completed punch point for a specific project.
**Request Body:**
- `completed_punch_id` (integer): ID of the completed punch point to verify.
- `verify_description` (string): Description of the verification.
- `status` (string): Status of the verification.

**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (object): Details of the verified punch point.

### 5. Get All Project-Wise Punch Points
**Endpoint:**
```
GET /get_all_project_wise_punch_raise_completed_verify/<int:project_id>
```
**Description:**
Retrieve all punch points (raised, completed, and verified) for a specific project.
**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (object): Contains:
  - `punch_points` (list): List of raised punch points.
  - `completed_punch_points` (list): List of completed punch points.
  - `verified_punch_points` (list): List of verified punch points.

### 6. Generate HOTO Certificate
**Endpoint:**
```
PUT /hoto_certificate
```
**Description:**
Generate a HOTO certificate PDF for a project.
**Request Body:**
- `project_id` (integer): ID of the project.
- `plant_name` (string): Name of the plant.
- `plant_cod` (date): COD of the plant.
- `issued_date` (date): Date of certificate issuance.
- `project_team_name` (string): Name of the project team.
- `onm_team_name` (string): Name of the O&M team.
- `epc_team_name` (string): Name of the EPC team.
- `list_attached` (list): List of attached documents.
- `design_section` (object): Design section details.
- `scm_section` (object): SCM section details.
- `project_section` (object): Project section details.
- `user_names` (object): User names involved.

**Response:**
- `status` (boolean): Indicates success or failure.
- `message` (string): Response message.
- `data` (string): URL of the generated PDF.

