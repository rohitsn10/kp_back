# Report Module API Documentation

## API Endpoints

### 1. Land Report API
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

### 2. HSE MIS Report API
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

### 3. SCM Material Tracking Report API
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

### 4. Check Quality Report API
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


### 5. Project EAR Report API
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


### 6. Project DPR Project Execution API
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

### 7. Project Hoto Summary Report API
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


### 8. Project Status Management Report API
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


### 9. Project IAR Report API
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

### 10. Project Delay Analysis Report API
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

