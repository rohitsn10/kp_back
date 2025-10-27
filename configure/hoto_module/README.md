# HOTO Module APIs

This document provides details about the APIs available in the HOTO (Handing Over Taking Over) module.

---

## 1. Add Documents and Categories to Database

### Command
```
python3 manage.py add_documents
```

### Description
This command populates the database with predefined document categories and their associated document names. It is useful for setting up initial data for the HOTO module.

### Steps to Use
1. Open a terminal and navigate to the `configure` directory of the project.
2. Run the command:
   ```bash
   python3 manage.py add_documents
   ```
3. The command will add predefined categories and documents to the database.
4. Check the terminal output for success or error messages.

### Example Output
```
Documents and categories added successfully.
```

---

## 2. Fetch All Documents (Categories and Names)

### Endpoint
```
GET /fetch_all_documents
```

### Description
This API fetches all document categories and their associated document names.

### Response Format
The API returns a list of categories, each containing its ID, name, and a list of documents with their IDs and names.

### Example Request
```http
GET /fetch_all_documents
```

### Example Response
```json
{
    "status": true,
    "message": "Documents fetched successfully",
    "data": [
        {
            "id": 1,
            "category": "Test Report- AC",
            "documents": [
                {"id": 101, "name": "Switchyard Equipments"},
                {"id": 102, "name": "Micom Relays"},
                {"id": 103, "name": "Transformer IDT"},
                {"id": 104, "name": "CT"},
                {"id": 105, "name": "Relay"}
            ]
        },
        {
            "id": 2,
            "category": "Test Report- DC",
            "documents": [
                {"id": 201, "name": "Solar PV Module"},
                {"id": 202, "name": "MMS (Column post, Rafter, Purlin)"},
                {"id": 203, "name": "Transformer"},
                {"id": 204, "name": "Strings Inverter"}
            ]
        }
    ]
}
```

---

## 3. Upload Main Document

### Endpoint
```
POST /upload_main_document
```

### Description
This API allows uploading main documents for a specific project, linking them to a document name and category.

### Request Format
```json
{
    "project_id": 1,
    "document_name_id": 5,
    "category_id": 2,
    "status": "Pending",
    "remarks": "Initial upload"
}
```

### Response Format
```json
{
    "status": true,
    "message": "Documents uploaded/created successfully",
    "data": {
        "id": 1,
        "project": 1,
        "document_name": {
            "id": 5,
            "name": "Switchyard Equipments"
        },
        "category": {
            "id": 2,
            "name": "Test Report- AC"
        },
        "status": "Pending",
        "remarks": "Initial upload",
        "is_uploaded": true,
        "created_by": 3,
        "updated_by": 3,
        "document": [
            {
                "id": 15,
                "file": "hoto_documents/file1.pdf"
            },
            {
                "id": 16,
                "file": "hoto_documents/file2.pdf"
            }
        ]
    }
}
```

---

## 4. View Documents for a Project

### Endpoint
```
GET /view_document?project_id=<project_id>
```

### Description
Fetches all documents for a specific project, including uploaded and not-uploaded documents.

### Response Format
```json
{
    "status": true,
    "message": "Documents retrieved successfully",
    "data": [
        {
            "id": 1,
            "project": 1,
            "document_name": {
                "id": 5,
                "name": "Switchyard Equipments"
            },
            "category": {
                "id": 2,
                "name": "Test Report- AC"
            },
            "uploaded_documents": [
                {
                    "id": 15,
                    "file": "hoto_documents/file1.pdf",
                    "created_at": "2025-10-27T10:00:00Z",
                    "updated_at": "2025-10-27T12:00:00Z"
                }
            ],
            "not_uploaded_documents": [
                {
                    "id": 6,
                    "name": "Micom Relays"
                }
            ],
            "status": "Pending",
            "remarks": "Initial upload",
            "verify_comment": null,
            "created_by": 3,
            "created_by_name": "John Doe",
            "created_at": "2025-10-27T10:00:00Z",
            "updated_by": 3,
            "updated_by_name": "John Doe",
            "updated_at": "2025-10-27T12:00:00Z"
        }
    ]
}
```

---

## 5. Verify Document

### Endpoint
```
PUT /verify_document/<doc_id>/
```

### Description
Allows verifying or rejecting a document by updating its status and adding verification comments.

### Request Format
```json
{
    "status": "Verified",
    "verify_comment": "Document is complete and verified."
}
```

### Response Format
```json
{
    "status": true,
    "message": "Document verified successfully",
    "data": {
        "id": 1,
        "project": 1,
        "document_name": {
            "id": 5,
            "name": "Switchyard Equipments"
        },
        "category": {
            "id": 2,
            "name": "Test Report- AC"
        },
        "status": "Verified",
        "verify_comment": "Document is complete and verified.",
        "updated_by": 3
    }
}
```

---

## 6. Delete Document

### Endpoint
```
DELETE /delete_document
```

### Description
Deletes specific documents by their IDs.

### Request Format
```json
{
    "doc_id": [1, 2, 3]
}
```

### Response Format
```json
{
    "status": true,
    "message": "Deleted documents: [1, 2]. Documents not found: [3]"
}
```