# Report Module API Documentation

## API Endpoints

### 1. Generate 66kV Statutory Approval Report
**Endpoint:**
`GET /satutory_approval_66kv_report/`

**Description:**
Generates a report for the 66kV statutory approval status.

**Response:**
- **200 OK**: Returns the report data.
- **400 Bad Request**: If there is an issue with the request.

---

### 2. Project Payment Status Report
**Endpoint:**
`GET /project_payment_status_report/`

**Description:**
Generates a report for the payment status of projects.

**Response:**
- **200 OK**: Returns the payment status report.
- **400 Bad Request**: If there is an issue with the request.

---

### 3. Project Budget vs Actual Cost Tracking Report
**Endpoint:**
`GET /project_budget_vs_actual_cost_tracking_report/`

**Description:**
Generates a report comparing the project budget with the actual cost tracking.

**Response:**
- **200 OK**: Returns the budget vs actual cost tracking report.
- **400 Bad Request**: If there is an issue with the request.

---

### 4. Land Report API
- **URL**: `/report_module/land_report/`
- **Method**: GET
- **Description**: Generates a land report and returns the file URL.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/land_report/
  ```

### 5. HSE MIS Report API
- **URL**: `/report_module/hse_mis_report/`
- **Method**: GET
- **Description**: Generates an HSE MIS report and returns the file URL.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/hse_mis_report/
  ```

### 6. SCM Material Tracking Report API
- **URL**: `/report_module/scm_material_tracking_report/`
- **Method**: GET
- **Description**: Generates an SCM Material Tracking report and returns the file URL.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/scm_material_tracking_report/
  ```

### 7. Check Quality Report API
- **URL**: `/report_module/check_quality_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/check_quality_report/
  ```


### 8. Project EAR Report API
- **URL**: `/report_module/project_ear_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_ear_report/
  ```


### 9. Project DPR Project Execution API
- **URL**: `/report_module/project_dpr_project_execution_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_dpr_project_execution_report/
  ```


### 10. Project Hoto Summary Report API
- **URL**: `/report_module/project_hoto_summary_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_hoto_summary_report/
  ```


### 11. Project Status Management Report API
- **URL**: `/report_module/project_status_management_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_status_management_report/
  ```


### 12. Project IAR Report API
- **URL**: `/report_module/project_iar_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_iar_report/
  ```


### 13. Project Delay Analysis Report API
- **URL**: `/report_module/project_delay_analysis_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/project_delay_analysis_report/
  ```


### 14. Design MDL Report API
- **URL**: `/report_module/design_mdl_report/`
- **Method**: GET
- **Description**: Checks and generates a quality report.
- **Permission**: `IsAuthenticated`
- **Curl Command**:
  ```bash
  curl -X GET \
       -H "Authorization: Bearer <your_token>" \
       http://127.0.0.1:8000/report_module/design_mdl_report/
  ```