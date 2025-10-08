# Quick Reference - Role & Permission Management APIs

## 🔗 Base URL
`/user_profile/`

---

## 📋 Quick Endpoint Reference

### 🎭 ROLES

| Action | Method | Endpoint | Body Example |
|--------|--------|----------|--------------|
| List roles | GET | `/roles/` | - |
| Create role | POST | `/roles/` | `{"name": "Manager", "department": 1, "permission_list": [{"module_id": 1, "can_access": true}]}` |
| Get role | GET | `/roles/{id}/` | - |
| Update role | PUT | `/roles/{id}/` | Same as create |
| Delete role | DELETE | `/roles/{id}/` | - |

**Filters:** `?department_id=1` `?search=manager`

---

### 📦 MODULES

| Action | Method | Endpoint | Body Example |
|--------|--------|----------|--------------|
| List modules | GET | `/modules/` | - |
| Create module | POST | `/modules/` | `{"name": "User Management"}` |
| Get module | GET | `/modules/{id}/` | - |
| Update module | PUT | `/modules/{id}/` | `{"name": "New Name"}` |
| Delete module | DELETE | `/modules/{id}/` | - |

---

### 🔐 PERMISSIONS

| Action | Method | Endpoint | Query Params |
|--------|--------|----------|--------------|
| List permissions | GET | `/role-permissions/` | `?role_id=1` or `?module_id=1` |
| Permission matrix | GET | `/role-permissions-by-module/` | `?role_id=1` (required) |

---

### 👤 USER ROLE ASSIGNMENTS

| Action | Method | Endpoint | Body Example |
|--------|--------|----------|--------------|
| List assignments | GET | `/user-roles/` | - |
| Assign role | POST | `/user-roles/` | `{"user": 5, "department": 1, "group": 2}` |
| Get assignment | GET | `/user-roles/{id}/` | - |
| Update assignment | PUT | `/user-roles/{id}/` | Same as assign |
| Remove assignment | DELETE | `/user-roles/{id}/` | - |

**Filters:** `?user_id=5` `?department_id=1`

---

### 🏢 DEPARTMENT ROLES

| Action | Method | Endpoint | Query Params |
|--------|--------|----------|--------------|
| Get dept roles | GET | `/department-roles/` | `?department_id=1` (required) |

---

## 🔑 Authentication

All requests require:
```
Authorization: Bearer <jwt_token>
```

---

## 📊 Common Response Format

### Success
```json
{
  "status": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### Error
```json
{
  "status": false,
  "message": "Error message",
  "errors": { ... }
}
```

---

## 🎯 Common Use Cases

### 1. Create Complete Role Setup
```bash
# Step 1: Create modules
POST /modules/ {"name": "Users"}
POST /modules/ {"name": "Projects"}

# Step 2: Create role with permissions
POST /roles/ {
  "name": "Manager",
  "department": 1,
  "permission_list": [
    {"module_id": 1, "can_access": true},
    {"module_id": 2, "can_access": true}
  ]
}

# Step 3: Assign to user
POST /user-roles/ {
  "user": 5,
  "department": 1,
  "group": 2
}
```

### 2. Check User Permissions
```bash
# Get user's role assignments
GET /user-roles/?user_id=5

# Get role details with permissions
GET /roles/{role_id}/

# Get permission matrix
GET /role-permissions-by-module/?role_id=1
```

### 3. Update Role Permissions
```bash
PUT /roles/1/ {
  "name": "Senior Manager",
  "department": 1,
  "permission_list": [
    {"module_id": 1, "can_access": true},
    {"module_id": 2, "can_access": true},
    {"module_id": 3, "can_access": true}
  ]
}
```

---

## 🚀 Quick Test Commands (curl)

### List Roles
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/user_profile/roles/
```

### Create Role
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Manager","department":1,"permission_list":[{"module_id":1,"can_access":true}]}' \
  http://localhost:8000/user_profile/roles/
```

### Get Permission Matrix
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/user_profile/role-permissions-by-module/?role_id=1"
```

### Assign Role to User
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user":5,"department":1,"group":2}' \
  http://localhost:8000/user_profile/user-roles/
```

---

## 📝 Notes

- ⚠️ **Creating roles:** Always create modules first
- ⚠️ **Updating permissions:** `permission_list` replaces all existing permissions
- ⚠️ **Group field:** In UserAssign, `group` represents the role ID
- ✅ **Best practice:** Use department_id filter when fetching roles
- ✅ **Performance:** Use role-permissions-by-module for complete permission view

---

## 📚 Full Documentation

See `ROLE_PERMISSION_API_DOCUMENTATION.md` for complete details with examples and best practices.
