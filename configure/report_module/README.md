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