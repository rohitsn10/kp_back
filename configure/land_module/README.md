# Land Bank APIs

This document provides details about the two APIs created for managing Land Bank data with pagination and search functionality.

---

## 1. Add SFA Data to Land Bank with Pagination

### Endpoint
```
POST /add_sfa_data_to_land_bank_with_pagination
GET /add_sfa_data_to_land_bank_with_pagination
```

### Description
- **POST**: Allows adding new SFA data to the Land Bank.
- **GET**: Fetches paginated Land Bank data with optional search functionality.

### Query Parameters (GET)
| Parameter   | Type   | Description                              |
|-------------|--------|------------------------------------------|
| `sfa_name`  | String | (Optional) Search by SFA name.           |
| `page`      | Int    | (Optional) Page number for pagination.   |
| `page_size` | Int    | (Optional) Number of records per page.   |

### Example Requests
1. **Paginated Request**:
   ```
   GET /add_sfa_data_to_land_bank_with_pagination?page=1&page_size=10
   ```
2. **Search by `sfa_name`**:
   ```
   GET /add_sfa_data_to_land_bank_with_pagination?sfa_name=test&page=1
   ```

### Example Response (GET)
```json
{
    "status": true,
    "message": "Land Bank List Successfully",
    "data": [
        {
            "id": 1,
            "sfa_name": "Test SFA",
            "land_name": "Example Land",
            "created_at": "2025-10-24T10:00:00Z",
            "updated_at": "2025-10-24T12:00:00Z"
        },
        ...
    ]
}
```

---

## 2. Create Land Bank Master with Pagination

### Endpoint
```
GET /create_land_bank_master_with_pagination
```

### Description
Fetches paginated Land Bank data with optional search functionality for `sfa_name` and `land_name`.

### Query Parameters
| Parameter   | Type   | Description                              |
|-------------|--------|------------------------------------------|
| `sfa_name`  | String | (Optional) Search by SFA name.           |
| `land_name` | String | (Optional) Search by Land name.          |
| `page`      | Int    | (Optional) Page number for pagination.   |
| `page_size` | Int    | (Optional) Number of records per page.   |

### Example Requests
1. **Paginated Request**:
   ```
   GET /create_land_bank_master_with_pagination?page=1&page_size=10
   ```
2. **Search by `sfa_name`**:
   ```
   GET /create_land_bank_master_with_pagination?sfa_name=test&page=1
   ```
3. **Search by `land_name`**:
   ```
   GET /create_land_bank_master_with_pagination?land_name=example&page=1
   ```
4. **Search by Both**:
   ```
   GET /create_land_bank_master_with_pagination?sfa_name=test&land_name=example&page=1
   ```

### Example Response
```json
{
    "status": true,
    "message": "Land Bank List Successfully",
    "data": [
        {
            "id": 1,
            "sfa_name": "Test SFA",
            "land_name": "Example Land",
            "is_land_bank_created": true,
            "created_at": "2025-10-24T10:00:00Z",
            "updated_at": "2025-10-24T12:00:00Z"
        },
        ...
    ]
}
```

---

## Notes for Frontend Developers
1. **Pagination**:
   - Both APIs support pagination. Use the `page` and `page_size` query parameters to control the number of records per page.
   - The default page size is 10.

2. **Search**:
   - Use the `sfa_name` and/or `land_name` query parameters to filter results based on these fields.

3. **Error Handling**:
   - If no data is found, the API will return:
     ```json
     {
         "status": false,
         "message": "No data found",
         "data": []
     }
     ```

4. **Authentication**:
   - Both APIs require the user to be authenticated. Ensure that the appropriate authentication headers are included in the request.

---

## Contact
For any issues or questions, please contact the backend team.