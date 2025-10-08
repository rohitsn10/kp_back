# Role & Permission Management API Documentation

This document provides comprehensive API documentation for the Role and Permission Management system.

## Base URL
All endpoints are prefixed with: `/user_profile/`

---

## 📋 Table of Contents
1. [Department Management](#department-management)
2. [Role Management](#role-management)
3. [Module Management](#module-management)
4. [Permission Management](#permission-management)
5. [User Role Assignment](#user-role-assignment)

---

## 🏢 Department Management

### Get All Departments
```http
GET /user_profile/get_department
```

**Query Parameters:**
- `search` (optional): Search by department name
- `page` (optional): Page number for pagination
- `page_size` (optional): Items per page

**Response:**
```json
{
  "status": true,
  "message": "Departments fetched successfully",
  "data": [
    {
      "id": 1,
      "department_name": "Engineering",
      "created_at": "2025-10-08T10:30:00Z"
    }
  ]
}
```

### Create Department
```http
POST /user_profile/create_get_department
```

**Request Body:**
```json
{
  "department_name": "Engineering"
}
```

**Response:**
```json
{
  "status": true,
  "message": "Department created successfully",
  "data": {
    "id": 1,
    "department_name": "Engineering",
    "created_at": "2025-10-08T10:30:00Z"
  }
}
```

### Update Department
```http
PUT /user_profile/update_delete_department/{department_id}
```

**Request Body:**
```json
{
  "department_name": "Engineering Department"
}
```

### Delete Department
```http
DELETE /user_profile/update_delete_department/{department_id}
```

---

## 🎭 Role Management

### Get All Roles
```http
GET /user_profile/roles/
```

**Query Parameters:**
- `department_id` (optional): Filter by department
- `search` (optional): Search by role name or department name
- `ordering` (optional): Sort by fields (name, created_at, -created_at)

**Response:**
```json
{
  "status": true,
  "message": "Roles fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "Project Manager",
      "department": 1,
      "department_name": "Engineering",
      "permissions": [
        {
          "id": 1,
          "role": 1,
          "role_name": "Project Manager",
          "module": 1,
          "module_name": "User Management",
          "can_access": true,
          "created_at": "2025-10-08T10:30:00Z"
        }
      ],
      "created_at": "2025-10-08T10:30:00Z"
    }
  ]
}
```

### Create Role with Permissions
```http
POST /user_profile/roles/
```

**Request Body:**
```json
{
  "name": "Project Manager",
  "department": 1,
  "permission_list": [
    {
      "module_id": 1,
      "can_access": true
    },
    {
      "module_id": 2,
      "can_access": false
    }
  ]
}
```

**Response:**
```json
{
  "status": true,
  "message": "Role created successfully",
  "data": {
    "id": 1,
    "name": "Project Manager",
    "department": 1,
    "department_name": "Engineering",
    "permissions": [
      {
        "id": 1,
        "role": 1,
        "role_name": "Project Manager",
        "module": 1,
        "module_name": "User Management",
        "can_access": true,
        "created_at": "2025-10-08T10:30:00Z"
      }
    ],
    "created_at": "2025-10-08T10:30:00Z"
  }
}
```

### Get Specific Role
```http
GET /user_profile/roles/{role_id}/
```

**Response:**
```json
{
  "status": true,
  "message": "Role details fetched successfully",
  "data": {
    "id": 1,
    "name": "Project Manager",
    "department": 1,
    "department_name": "Engineering",
    "permissions": [...]
  }
}
```

### Update Role with Permissions
```http
PUT /user_profile/roles/{role_id}/
```

**Request Body:**
```json
{
  "name": "Senior Project Manager",
  "department": 1,
  "permission_list": [
    {
      "module_id": 1,
      "can_access": true
    },
    {
      "module_id": 3,
      "can_access": true
    }
  ]
}
```

**Note:** The `permission_list` will replace all existing permissions for this role.

### Delete Role
```http
DELETE /user_profile/roles/{role_id}/
```

**Response:**
```json
{
  "status": true,
  "message": "Role 'Project Manager' deleted successfully"
}
```

### Get Roles by Department
```http
GET /user_profile/department-roles/?department_id=1
```

**Response:**
```json
{
  "status": true,
  "message": "Department roles fetched successfully",
  "data": {
    "department_id": 1,
    "department_name": "Engineering",
    "roles": [
      {
        "id": 1,
        "name": "Project Manager",
        "department": 1,
        "department_name": "Engineering",
        "permissions": [...]
      }
    ]
  }
}
```

---

## 📦 Module Management

### Get All Modules
```http
GET /user_profile/modules/
```

**Query Parameters:**
- `search` (optional): Search by module name
- `ordering` (optional): Sort by fields (name, created_at)

**Response:**
```json
{
  "status": true,
  "message": "Modules fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "User Management",
      "created_at": "2025-10-08T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Project Management",
      "created_at": "2025-10-08T10:30:00Z"
    }
  ]
}
```

### Create Module
```http
POST /user_profile/modules/
```

**Request Body:**
```json
{
  "name": "User Management"
}
```

**Response:**
```json
{
  "status": true,
  "message": "Module created successfully",
  "data": {
    "id": 1,
    "name": "User Management",
    "created_at": "2025-10-08T10:30:00Z"
  }
}
```

### Get Specific Module
```http
GET /user_profile/modules/{module_id}/
```

### Update Module
```http
PUT /user_profile/modules/{module_id}/
```

### Delete Module
```http
DELETE /user_profile/modules/{module_id}/
```

**Response:**
```json
{
  "status": true,
  "message": "Module 'User Management' deleted successfully"
}
```

---

## 🔐 Permission Management

### Get All Role Permissions
```http
GET /user_profile/role-permissions/
```

**Query Parameters:**
- `role_id` (optional): Filter by role
- `module_id` (optional): Filter by module

**Response:**
```json
{
  "status": true,
  "message": "Permissions fetched successfully",
  "data": [
    {
      "id": 1,
      "role": 1,
      "role_name": "Project Manager",
      "module": 1,
      "module_name": "User Management",
      "can_access": true,
      "created_at": "2025-10-08T10:30:00Z"
    }
  ]
}
```

### Get Permissions by Module for a Role
```http
GET /user_profile/role-permissions-by-module/?role_id=1
```

**Response:**
```json
{
  "status": true,
  "message": "Role permissions fetched successfully",
  "data": {
    "role_id": 1,
    "role_name": "Project Manager",
    "department_id": 1,
    "department_name": "Engineering",
    "permissions": [
      {
        "module_id": 1,
        "module_name": "User Management",
        "can_access": true
      },
      {
        "module_id": 2,
        "module_name": "Project Management",
        "can_access": false
      }
    ]
  }
}
```

---

## 👤 User Role Assignment

### Get User Role Assignments
```http
GET /user_profile/user-roles/
```

**Query Parameters:**
- `user_id` (optional): Filter by user
- `department_id` (optional): Filter by department

**Response:**
```json
{
  "status": true,
  "message": "User role assignments fetched successfully",
  "data": [
    {
      "id": 1,
      "user": 5,
      "user_name": "John Doe",
      "user_email": "john@example.com",
      "department": 1,
      "department_name": "Engineering",
      "group": 2,
      "role_name": "Project Manager",
      "created_at": "2025-10-08T10:30:00Z",
      "updated_at": "2025-10-08T10:30:00Z"
    }
  ]
}
```

### Assign Role to User
```http
POST /user_profile/user-roles/
```

**Request Body:**
```json
{
  "user": 5,
  "department": 1,
  "group": 2
}
```

**Response:**
```json
{
  "status": true,
  "message": "Role assigned to user successfully",
  "data": {
    "id": 1,
    "user": 5,
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "department": 1,
    "department_name": "Engineering",
    "group": 2,
    "role_name": "Project Manager",
    "created_at": "2025-10-08T10:30:00Z",
    "updated_at": "2025-10-08T10:30:00Z"
  }
}
```

### Update User Role Assignment
```http
PUT /user_profile/user-roles/{assignment_id}/
```

**Request Body:**
```json
{
  "user": 5,
  "department": 1,
  "group": 3
}
```

### Remove User Role Assignment
```http
DELETE /user_profile/user-roles/{assignment_id}/
```

**Response:**
```json
{
  "status": true,
  "message": "Role assignment removed successfully"
}
```

---

## 📝 Complete Workflow Examples

### Example 1: Creating a Complete Role with Permissions

**Step 1:** Create modules (if not exist)
```http
POST /user_profile/modules/
{
  "name": "User Management"
}

POST /user_profile/modules/
{
  "name": "Project Management"
}
```

**Step 2:** Create a role with permissions
```http
POST /user_profile/roles/
{
  "name": "Project Manager",
  "department": 1,
  "permission_list": [
    {"module_id": 1, "can_access": true},
    {"module_id": 2, "can_access": true}
  ]
}
```

**Step 3:** Assign role to user
```http
POST /user_profile/user-roles/
{
  "user": 5,
  "department": 1,
  "group": 2
}
```

### Example 2: Updating Role Permissions

**Update permissions for an existing role:**
```http
PUT /user_profile/roles/1/
{
  "name": "Senior Project Manager",
  "department": 1,
  "permission_list": [
    {"module_id": 1, "can_access": true},
    {"module_id": 2, "can_access": true},
    {"module_id": 3, "can_access": true}
  ]
}
```

### Example 3: Checking User Permissions

**Get all permissions for a specific role:**
```http
GET /user_profile/role-permissions-by-module/?role_id=1
```

**Get user's role assignments:**
```http
GET /user_profile/user-roles/?user_id=5
```

---

## 🔒 Authentication

All endpoints require authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

---

## ⚠️ Error Responses

### Validation Error (400)
```json
{
  "status": false,
  "message": "Validation error",
  "errors": {
    "department": ["This field is required."]
  }
}
```

### Not Found (404)
```json
{
  "status": false,
  "message": "Role not found"
}
```

### Unauthorized (401)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 📊 Data Models

### Role
- `id`: Integer (auto)
- `name`: String (max 255)
- `department`: Foreign Key to Department
- `created_at`: DateTime (auto)

### Module
- `id`: Integer (auto)
- `name`: String (max 255)
- `created_at`: DateTime (auto)

### RolePermission
- `id`: Integer (auto)
- `role`: Foreign Key to Role
- `module`: Foreign Key to Module
- `can_access`: Boolean (default: false)
- `created_at`: DateTime (auto)

### UserAssign
- `id`: Integer (auto)
- `user`: Foreign Key to CustomUser
- `department`: Foreign Key to Department
- `group`: Foreign Key to Group (represents role)
- `project`: Foreign Key to Project (nullable)
- `created_at`: DateTime (auto)
- `updated_at`: DateTime (auto)

---

## 🎯 Best Practices

1. **Always create modules first** before creating roles with permissions
2. **Use department_id filter** when fetching roles to get department-specific roles
3. **Use role_id parameter** in role-permissions-by-module endpoint to get complete permission matrix
4. **When updating roles**, include all permissions in permission_list as it replaces existing permissions
5. **Check user assignments** using user_id query parameter before assigning new roles

---

## 📞 Support

For any issues or questions, please contact the development team.
