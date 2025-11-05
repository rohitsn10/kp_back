## API Endpoints

### Get Users with Pagination
**Endpoint:** `/user_profile/get_users_with_pagination/`

**Method:** `GET`

**Description:** Retrieves a paginated list of users.

**Query Parameters:**
- `page` (optional): The page number to retrieve.
- `page_size` (optional): The number of items per page (default is 10).

**Curl Command:**
```bash
curl -X GET "http://127.0.0.1:8000/user_profile/get_users_with_pagination/?page=2&page_size=5" \
-H "Authorization: Bearer <your-auth-token>"
```

**Response Example:**
```json
{
    "count": 50,
    "next": "http://127.0.0.1:8000/user_profile/get_users_with_pagination/?page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "user1@example.com",
            "full_name": "User One",
            "phone": "1234567890",
            "address": "Address 1"
        }
    ]
}
```

### Get Users by Group
**Endpoint:** `/user_profile/get_user_by_group/`

**Method:** `GET`

**Description:** Retrieves a paginated list of users belonging to a specific group.

**Query Parameters:**
- `group_id` (required): The ID of the group to filter users by.
- `page` (optional): The page number to retrieve.
- `page_size` (optional): The number of items per page (default is 10).

**Curl Command:**
```bash
curl -X GET "http://127.0.0.1:8000/user_profile/get_user_by_names/?name=hasmukh&page=2&page_size=5" \
-H "Authorization: Bearer <your-auth-token>"
```

**Response Example:**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/user_profile/get_user_by_names/?name=hasmukh&page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "id": 6,
            "email": "user6@example.com",
            "full_name": "User Six",
            "phone": "1234567896",
            "address": "Address 6"
        }
    ]
}
```