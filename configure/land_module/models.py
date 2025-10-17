from django.db import models
from django.conf import settings

class LandCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SFAAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_sfa_file = models.FileField(upload_to='land_sfa_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class SFAforTransmissionLineGSSAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sfa_for_transmission_line_gss_files = models.FileField(upload_to='sfa_for_transmission_line_gss_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class SfaSoilBearingCapacityAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sfa_soil_bearing_capacity_files = models.FileField(upload_to='sfa_soil_bearing_capacity_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
class LandLocationAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_location_file = models.FileField(upload_to='land_location', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandSurveyNumbeAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_survey_number_file = models.FileField(upload_to='land_survey_number', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandKeyPlanAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_key_plan_file = models.FileField(upload_to='land_key_plan', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandAttachApprovalReportAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_attach_approval_report_file = models.FileField(upload_to='land_attach_approval_report', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandApproachRoadAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_approach_road_file = models.FileField(upload_to='land_approach_road', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandCoOrdinatesAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_co_ordinates_file = models.FileField(upload_to='land_co_ordinates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandLeaseDeedAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_lease_deed_file = models.FileField(upload_to='land_lease_deed', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandTransmissionLineAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_transmission_line_file = models.FileField(upload_to='land_transmission_line', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandApprovedReportAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_report_file = models.FileField(upload_to='approved_report_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
from django.contrib.postgres.fields import ArrayField
class LandBankMaster(models.Model):
    SFA_LAND_TITLE_CHOICES = (
        ('Freehold', 'Freehold'),
        ('Govt', 'Govt'),
        ('Private', 'Private'),
    )
    SFA_LAND_CATEGORY_CHOICES = (
        ('Forest', 'Forest'),
        ('Agriculture', 'Agriculture'),
        ('AnyOther', 'AnyOther'),
    )
    
    SFA_LAND_PROFILE_CHOICES = (
        ('Hilly', 'Hilly'),
        ('Flat', 'Flat'),
        ('Undulated', 'Undulated'),
        ('Developed', 'Developed'),
        ('Undeveloped', 'Undeveloped'),
        ('Sandy', 'Sandy'),
        ('Silty', 'Silty'),
        ('BackFilled', 'BackFilled'),
    )
    
    SFA_LAND_ORIENTATION_CHOICES = (
        ('NorthToSouth', 'North To South'),
        ('EastToWest', 'East To West'),
    )
    
    SFA_POWER_EXPORT_HAPPENING_CHOICES = (
        ("Solar","Solar"),
        ("Wind","Wind"),
        ("Biogas","Biogas")
    )
    
    SOLAR_WIND_CHOICES = (
        ('Solar', 'Solar'),
        ('Wind', 'Wind'),
    )
    
    SFA_WEATHER_TEMP_CHOICES = (
        ('MinTemp','MinTemp'),
        ('MaxTemp','MaxTemp')
    )

    LAND_BANK_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    STATUS_OF_SITE_VISIT = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    LAND_TYPE_CHOICES = (
        ('BUY', 'buy'),
        ('LEASE', 'lease')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_category = models.ForeignKey(LandCategory, on_delete=models.CASCADE, null=True, blank=True)
    land_name = models.TextField(null=True, blank=True)
    block_number = models.CharField(max_length=200, null=True, blank=True)
    land_type=models.CharField(max_length=10, choices=LAND_TYPE_CHOICES, null=True, blank=True)
    sale_deed_date = models.DateTimeField(null=True, blank=True)
    sale_deed_number= models.CharField(max_length=200, null=True, blank=True)
    lease_deed_date = models.DateTimeField(null=True, blank=True) 
    lease_deed_number = models.CharField(max_length=200, null=True, blank=True)
    lease_deed_file = models.ManyToManyField(LandLeaseDeedAttachment, null=True, blank=True)

    keypoints = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    
    #=============== SFA ================
    sfa_name = models.CharField(max_length=255, null=True, blank=True)
    land_address = models.CharField(max_length=255, null=True, blank=True)
    client_consultant = models.CharField(max_length=255, null=True, blank=True)
    site_visit_date = models.DateTimeField(null=True, blank=True)
    palnt_capacity = models.CharField(max_length=255, null=True, blank=True)
    land_owner = models.CharField(max_length=255, null=True, blank=True)
    sfa_available_area_acres = models.CharField(max_length=255, null=True, blank=True)
    distance_from_main_road = models.CharField(max_length=500, null=True, blank=True)
    road_highway_details = models.CharField(max_length=500, null=True, blank=True)
    land_title = models.CharField(max_length=100, choices=SFA_LAND_TITLE_CHOICES, null=True, blank=True)
    sfa_land_category = models.CharField(max_length=100, choices=SFA_LAND_CATEGORY_CHOICES, null=True, blank=True)
    sfa_land_profile = models.CharField(max_length=100, choices=SFA_LAND_PROFILE_CHOICES, null=True, blank=True)
    sfa_land_orientation = models.CharField(max_length=100, choices=SFA_LAND_ORIENTATION_CHOICES, null=True, blank=True)
    sfa_land_soil_testing_availability = models.CharField(max_length=255, null=True, blank=True)
    sfa_soil_bearing_capacity_files = models.ManyToManyField(SfaSoilBearingCapacityAttachment)
    any_shadow_casting_buildings_or_hill = models.CharField(max_length=255, null=True, blank=True)
    any_water_ponds_or_nalas_within_the_proposed_location = models.CharField(max_length=500, null=True, blank=True)
    any_roads_or_bridge_within_the_proposed_location = models.CharField(max_length=500,null=True, blank=True)
    any_railway_lane_within_the_proposed_location = models.CharField(max_length=500,null=True, blank=True)
    is_the_proposed_site_is_of_natural_contour_or_filled_up_area = models.CharField(max_length=255, null=True, blank=True)
    land_co_ordinates = models.CharField(max_length=500, null=True, blank=True)
    substation_cordinates = models.CharField(max_length=500, null=True, blank=True)
    solar_isolation_data = models.CharField(max_length=500, null=True, blank=True)
    rain_fall_pattern = models.CharField(max_length=500, choices = SFA_WEATHER_TEMP_CHOICES, null=True, blank=True)
    communication_network_availability = models.CharField(max_length=500, null=True, blank=True)
    # Power Evacuation
    permission_required_for_power_generation = models.CharField(max_length=255, null=True, blank=True)
    transmission_network_availabilty_above_400_220_33kv = models.CharField(max_length=500, null=True, blank=True)
    distance_of_supply_point_from_proposed_site = models.CharField(max_length=500, null=True, blank=True)
    distance_of_nearest_substation_from_proposed_site = models.CharField(max_length=500, null=True, blank=True)
    transmission_line_load_carrying_or_evacuation_capacity = models.CharField(max_length=500, null=True, blank=True)
    right_of_way_requirement_up_to_the_delivery_point = models.CharField(max_length=500, null=True, blank=True)
    construction_power_availability_and_identify_source_distance = models.CharField(max_length=500, null=True, blank=True)
    grid_availability_data_outage_pattern = models.CharField(max_length=500, null=True, blank=True)
    substation_capacity_mva = models.CharField(max_length=500, null=True, blank=True)
    substation_load_side_voltage_level_kv = models.CharField(max_length=500, null=True, blank=True)
    kv_grid_voltage_variation = models.CharField(max_length=500, null=True, blank=True)
    hz_grid_voltage_variation = models.CharField(max_length=500, null=True, blank=True)
    check_space_availability_in_substation_to_conct_power_by_area = models.CharField(max_length=500, null=True, blank=True)
    transformer_rating_in_substation = models.CharField(max_length=500, null=True, blank=True)
    check_protection_system_details_of_substation = models.CharField(max_length=500, null=True, blank=True)
    any_future_plan_for_expansion_of_substation = models.CharField(max_length=500, null=True, blank=True)
    is_there_any_power_export_happening_at_substation = models.CharField(max_length=500,choices = SFA_POWER_EXPORT_HAPPENING_CHOICES, null=True, blank=True)
    any_specific_requirements_of_eb_for_double_pole_structure = models.CharField(max_length=500, null=True, blank=True)
    any_transmission_communication_line_passing_through_site = models.CharField(max_length=500, null=True, blank=True)
    neighboring_area_or_vicinity_details = models.CharField(max_length=500, null=True, blank=True)
    nearest_industry_category_and_distance = models.CharField(max_length=500, null=True, blank=True)
    nearest_village_or_district_name_and_distance = models.CharField(max_length=500, null=True, blank=True)
    nearest_highway_or_airport_name_and_distance = models.CharField(max_length=500, null=True, blank=True)
    availability_of_labor_and_cost_of_labor = models.CharField(max_length=500, null=True, blank=True)
    logistics = models.CharField(max_length=500, null=True, blank=True)
    is_there_an_approach_road_available_to_the_site = models.CharField(max_length=500, null=True, blank=True)
    can_truck_of_Multi_axel_with_40_foot_container_reach_site = models.CharField(max_length=500, null=True, blank=True)
    availability_of_vehicle_for_hiring_or_cost_per_km = models.CharField(max_length=500, null=True, blank=True)
    # HSSE
    list_the_risks_including_journey =  models.CharField(max_length=500, null=True, blank=True)
    # Others
    nearest_police_station_and_distance = models.CharField(max_length=500, null=True, blank=True)
    nearest_hospital_and_distance = models.CharField(max_length=500, null=True, blank=True)
    nearest_fire_station_and_distance = models.CharField(max_length=500, null=True, blank=True)
    nearest_seashore_and_distance = models.CharField(max_length=500, null=True, blank=True)
    availability_of_accommodation_to_site_approximate_cost = models.CharField(max_length=500, null=True, blank=True)
    provide_near_by_civil_electrical_contractors = models.CharField(max_length=500, null=True, blank=True)
    availability_of_construction_material_nearby = models.CharField(max_length=255, null=True, blank=True)
    any_weather_station_nearby = models.CharField(max_length=500, null=True, blank=True)
    # Water Availability 
    water_belt_profile_of_the_area = models.CharField(max_length=500, null=True, blank=True)
    water_availability = models.CharField(max_length=500, null=True, blank=True)
    construction_water_availability = models.CharField(max_length=500, null=True, blank=True)
    details_of_local_drainage_scheme = models.CharField(max_length=500, null=True, blank=True)
    availability_of_potable_water = models.CharField(max_length=500, null=True, blank=True)
    any_other_general_observation = models.CharField(max_length=500, null=True, blank=True)

    land_sfa_file = models.ManyToManyField(SFAAttachment)
    sfa_for_transmission_line_gss_files = models.ManyToManyField(SFAforTransmissionLineGSSAttachment)
    solar_or_winds = models.CharField(max_length=10, choices=SOLAR_WIND_CHOICES, null=True, blank=True)
    date_of_assessment = models.DateTimeField(null=True, blank=True)
    status_of_site_visit = models.CharField(max_length=255, choices=STATUS_OF_SITE_VISIT, null=True, blank=True,default='Pending')
    sfa_approved_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sfa_approved_user', null=True, blank=True, on_delete=models.SET_NULL)
    sfa_rejected_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sfa_rejected_user', null=True, blank=True, on_delete=models.SET_NULL)
    sfa_checked_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sfa_checked_user', null=True, blank=True, on_delete=models.SET_NULL)
    
    survey_number = models.CharField(max_length=500, null=True, blank=True)
    village_name = models.CharField(max_length=500, null=True, blank=True)
    district_name = models.CharField(max_length=500, null=True, blank=True)
    taluka_tahshil_name = models.CharField(max_length=500, null=True, blank=True)
    propose_gss_number = models.CharField(max_length=500, null=True, blank=True)
    land_status = models.CharField(max_length=500, null=True, blank=True)
    area_meters = models.CharField(max_length=500, null=True, blank=True)
    area_acres = models.CharField(max_length=500,null=True, blank=True)
    industrial_jantri = models.CharField(max_length=500, null=True,blank=True)
    jantri_value = models.CharField(max_length=500, null=True,blank=True)
    mort_gaged = models.CharField(max_length=500, null=True, blank=True)
    seller_name = models.CharField(max_length=500, blank=True, null=True)
    buyer_name = models.CharField(max_length=500, blank=True, null=True)
    actual_bucket = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    index_number = models.CharField(max_length=500, blank=True, null=True)
    tsr = models.CharField(max_length=100, blank=True, null=True)
    advocate_name = models.CharField(max_length=500, blank=True, null=True)

    total_land_area = models.CharField(max_length=500, null=True, blank=True)
    remaining_land_area = models.CharField(max_length=500, null=True, blank=True)
    land_location_file = models.ManyToManyField(LandLocationAttachment,null=True, blank=True)
    land_survey_number_file = models.ManyToManyField(LandSurveyNumbeAttachment, null=True, blank=True)
    land_key_plan_file = models.ManyToManyField(LandKeyPlanAttachment, null=True, blank=True)
    land_attach_approval_report_file = models.ManyToManyField(LandAttachApprovalReportAttachment, null=True, blank=True)
    land_approach_road_file = models.ManyToManyField(LandApproachRoadAttachment, null=True, blank=True)
    land_co_ordinates_file = models.ManyToManyField(LandCoOrdinatesAttachment, null=True, blank=True)
    land_lease_deed_files = models.ManyToManyField(LandLeaseDeedAttachment, null=True, blank=True)
    land_transmission_line_file = models.ManyToManyField(LandTransmissionLineAttachment, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    land_bank_status = models.CharField(max_length=255, choices=LAND_BANK_STATUS, null=True, blank=True, default='Pending')
    approved_report_file = models.ManyToManyField(LandApprovedReportAttachment)
    is_land_bank_created = models.BooleanField(default=False)
    is_land_bank_started = models.BooleanField(default=False)
    is_land_bank_added_attachment = models.BooleanField(default=False)

    land_bank_approved_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='land_bank_approved_user', null=True, blank=True, on_delete=models.SET_NULL)
    land_bank_rejected_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='land_bank_rejected_user', null=True, blank=True, on_delete=models.SET_NULL)
    land_bank_checked_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='land_bank_checked_user', null=True, blank=True, on_delete=models.SET_NULL)
    is_land_bank_approved_by_project_hod = models.BooleanField(default=False)

#geographic cordinates
    geo_coordinate_format = models.CharField(max_length=100, null=True, blank=True)
    geo_easting = models.CharField(max_length=100, null=True, blank=True)
    geo_northing = models.CharField(max_length=100, null=True, blank=True)
    geo_zone = models.CharField(max_length=100, null=True, blank=True)

#land cordinates
    land_coordinate_format = models.CharField(max_length=100, null=True, blank=True)
    land_easting = models.CharField(max_length=100, null=True, blank=True)
    land_northing = models.CharField(max_length=100, null=True, blank=True)
    land_zone = models.CharField(max_length=100, null=True, blank=True)

#substation coordinates
    substation_coordinate_format = models.CharField(max_length=100, null=True, blank=True)
    substation_easting = models.CharField(max_length=100, null=True, blank=True)
    substation_northing = models.CharField(max_length=100, null=True, blank=True)
    substation_zone = models.CharField(max_length=100, null=True, blank=True)    
    


class SaveApprovalDataOfStatusOfSiteVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE, null=True, blank=True)
    status_of_site_visit = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SaveRejectDataOfStatusOfSiteVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE, null=True, blank=True)
    status_of_site_visit = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LandSFAData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class LandBankApproveAction(models.Model):
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    land_bank_status = models.CharField(max_length=255, null=True, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

class LandBankRejectAction(models.Model):
    rejected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    land_bank_status = models.CharField(max_length=255, null=True, blank=True)
    rejected_at = models.DateTimeField(auto_now_add=True)

class DILRAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dilr_attachment_file = models.FileField(upload_to='dilr_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NA_65B_Permission_Attachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    na_65b_permission_attachment_file = models.FileField(upload_to='na_65b_permission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Revenue_7_12_Records_Attachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    revenue_7_12_records_attachment = models.FileField(upload_to='revenue_7_12_records_attachment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MunicipalCorporationPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    municipal_corporation_permission_file = models.FileField(upload_to='municipal_corporation_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TSRAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title_search_report_file = models.FileField(upload_to='title_search_report_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CoordinateVerificationAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coordinate_verification_file = models.FileField(upload_to='coordinate_verification', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EncumbranceNOCAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    encumbrance_noc_file = models.FileField(upload_to='encumbrance_noc', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DeveloperPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    developer_permission_file = models.FileField(upload_to='developer_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ListOfOtherApprovalsLandAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_of_other_approvals_land_file = models.FileField(upload_to='list_of_other_approvals_land', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromMinistryofDefenceAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noc_from_ministry_of_defence_file = models.FileField(upload_to='noc_from_ministry_of_defence', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromAirportAuthorityOfIndiaAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noc_from_airport_authority_of_india_file = models.FileField(upload_to='noc_from_airport_authority_of_india', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromForestAndAmpAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noc_from_forest_and_amp_attachment_file = models.FileField(upload_to='noc_from_forest_and_amp_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromGeologyAndMiningOfficeAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noc_from_geology_and_mining_office_attachment_file = models.FileField(upload_to='noc_from_geology_and_mining_office_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ApprovalsRequiredForTransmissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approvals_required_for_transmission_attachment_file = models.FileField(upload_to='approvals_required_for_transmission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CanalCrossingAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    canal_crossing_attachment_file = models.FileField(upload_to='canal_crossing_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LeaseDeedAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lease_deed_attachment_file = models.FileField(upload_to='lease_deed_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RailwayCrossingAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    railway_crossing_attachment_file = models.FileField(upload_to='railway_crossing_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyGasPipelineCrossingAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    any_gas_pipeline_crossing_attachment_file = models.FileField(upload_to='any_gas_pipeline_crossing_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoadCrossingPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    road_crossing_permission_attachment_file = models.FileField(upload_to='road_crossing_permission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyTransmissionLineCrossingPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    any_transmission_line_crossing_permission_attachment_file = models.FileField(upload_to='any_transmission_line_crossing_permission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyTransmissionLineShiftingPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    any_transmission_line_shifting_permission_attachment_file = models.FileField(upload_to='any_transmission_line_shifting_permission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GramPanchayatPermissionAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gram_panchayat_permission_attachment_file = models.FileField(upload_to='gram_panchayat_permission_attachment_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ListOfApprovalsRequiredForTransmissionLineAttachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_of_approvals_required_for_transmission_line_file = models.FileField(
        upload_to='list_of_approvals_required_for_transmission_line_file', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class LandBankAfterApprovedData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE,null=True, blank=True)
    dilr_attachment_file = models.ManyToManyField(DILRAttachment)
    na_65b_permission_attachment_file = models.ManyToManyField(NA_65B_Permission_Attachment)
    revenue_7_12_records_attachment = models.ManyToManyField(Revenue_7_12_Records_Attachment)
    noc_from_forest_and_amp_attachment_file = models.ManyToManyField(NOCfromForestAndAmpAttachment)
    noc_from_geology_and_mining_office_attachment_file = models.ManyToManyField(NOCfromGeologyAndMiningOfficeAttachment)
    approvals_required_for_transmission_attachment_file = models.ManyToManyField(ApprovalsRequiredForTransmissionAttachment)
    canal_crossing_attachment_file = models.ManyToManyField(CanalCrossingAttachment)
    lease_deed_attachment_file = models.ManyToManyField(LeaseDeedAttachment)
    railway_crossing_attachment_file = models.ManyToManyField(RailwayCrossingAttachment)
    any_gas_pipeline_crossing_attachment_file = models.ManyToManyField(AnyGasPipelineCrossingAttachment)
    road_crossing_permission_attachment_file = models.ManyToManyField(RoadCrossingPermissionAttachment)
    any_transmission_line_crossing_permission_attachment_file = models.ManyToManyField(AnyTransmissionLineCrossingPermissionAttachment)
    any_transmission_line_shifting_permission_attachment_file = models.ManyToManyField(AnyTransmissionLineShiftingPermissionAttachment)
    gram_panchayat_permission_attachment_file = models.ManyToManyField(GramPanchayatPermissionAttachment)
    municipal_corporation_permission_file = models.ManyToManyField(MunicipalCorporationPermissionAttachment)
    list_of_other_approvals_land_file = models.ManyToManyField(ListOfOtherApprovalsLandAttachment)
    title_search_report_file = models.ManyToManyField(TSRAttachment)
    coordinate_verification_file = models.ManyToManyField(CoordinateVerificationAttachment)
    encumbrance_noc_file = models.ManyToManyField(EncumbranceNOCAttachment)
    developer_permission_file = models.ManyToManyField(DeveloperPermissionAttachment)
    noc_from_ministry_of_defence_file = models.ManyToManyField(NOCfromMinistryofDefenceAttachment)
    list_of_approvals_required_for_transmission_line_file = models.ManyToManyField(ListOfApprovalsRequiredForTransmissionLineAttachment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_filled_22_forms = models.BooleanField(default=False)

class LandBankLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    land_bank_location_name = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_land_area = models.CharField(null=True, blank=True)
    near_by_area = models.CharField(max_length=500,null=True, blank=True)

class LandSurveyNumber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE,null=True, blank=True)
    location_name = models.ForeignKey(LandBankLocation, on_delete=models.CASCADE, related_name='land_survey_numbers', null=True, blank=True)
    land_survey_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)