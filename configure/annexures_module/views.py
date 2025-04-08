from django.shortcuts import render
from user_profile.models import *
from annexures_module.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from annexures_module.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class PermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermitToWorkSerializer
    queryset = PermitToWork.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            location_id = request.data.get('location_id')
            site_name = request.data.get('site_name')
            department = request.data.get('department')
            permit_number = request.data.get('permit_number')
            external_agency_name = request.data.get('external_agency_name')
            type_of_permit = request.data.get('type_of_permit')
            other_permit_description = request.data.get('other_permit_description')
            permit_issued_for = request.data.get('permit_issued_for', [])
            day = request.data.get('day')
            night = request.data.get('night')
            job_activity = request.data.get('job_activity')
            location_area = request.data.get('location_area')
            tools_equipment = request.data.get('tools_equipment')
            hazard_consideration = request.data.get('hazard_consideration', [])
            other_hazard_consideration = request.data.get('other_hazard_consideration')
            job_preparation = request.data.get('job_preparation', [])
            risk_assessment_number = request.data.get('risk_assessment_number')
            other_job_preparation = request.data.get('other_job_preparation')
            fire_protection = request.data.get('fire_protection', [])
            other_fire_protection = request.data.get('other_fire_protection')
            
            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})
    
            permit_issued_for_str = ",".join(permit_issued_for) if permit_issued_for else ""
            hazard_consideration_str = ",".join(hazard_consideration) if hazard_consideration else ""
            fire_protection_str = ",".join(fire_protection) if fire_protection else ""
            job_preparation_str = ",".join(job_preparation) if job_preparation else ""

            if type_of_permit == "cold work":
                expiry_date = timezone.now() + timezone.timedelta(days=25)
            else:
                expiry_date = timezone.now() + timezone.timedelta(hours=24)
                # expiry_date = timezone.now() + timezone.timedelta(minutes=1) #temporary

            permit_to_work = PermitToWork.objects.create(
                user=user,
                location=location_instance,
                site_name=site_name,
                department=department,
                permit_number=permit_number,
                name_of_external_agency=external_agency_name,
                type_of_permit=type_of_permit,
                other_permit_description = other_permit_description,
                day = day,
                night=night,
                job_activity_details=job_activity,
                location_area=location_area,
                tools_equipment=tools_equipment,
                hazard_consideration=hazard_consideration_str,
                other_hazard_consideration = other_hazard_consideration,
                fire_protection=fire_protection_str,
                permit_issue_for=permit_issued_for_str,
                job_preparation=job_preparation_str,
                risk_assessment_number = risk_assessment_number,
                other_job_preparation = other_job_preparation,
                other_fire_protection = other_fire_protection,
                expiry_date=expiry_date
            )

            serializer = PermitToWorkSerializer(permit_to_work)
            return Response({"status": True, "message": "Permit to work created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetPermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermitToWorkSerializer
    queryset = PermitToWork.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
class LocationIdWisePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermitToWorkSerializer
    queryset = PermitToWork.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location_id=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class UpdatePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermitToWorkSerializer
    queryset = PermitToWork.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)
            site_name = request.data.get('site_name')
            department = request.data.get('department')
            permit_number = request.data.get('permit_number')
            external_agency_name = request.data.get('external_agency_name')
            type_of_permit = request.data.get('type_of_permit')
            other_permit_description = request.data.get('other_permit_description')
            day = request.data.get('day')
            night = request.data.get('night')
            job_activity = request.data.get('job_activity')
            location_area = request.data.get('location_area')
            tools_equipment = request.data.get('tools_equipment')
            other_hazard_consideration = request.data.get('other_hazard_consideration')
            hazard_consideration = request.data.get('hazard_consideration', [])
            job_preparation = request.data.get('job_preparation', [])
            permit_issued_for = request.data.get('permit_issued_for', [])
            fire_protection = request.data.get('fire_protection', [])
            risk_assessment_number = request.data.get('risk_assessment_number')
            other_job_preparation = request.data.get('other_job_preparation')
            other_fire_protection = request.data.get('other_fire_protection')

            if permit_issued_for:
                permit_issued_for_str = ",".join(permit_issued_for) if permit_issued_for else ""
                permit_to_work.permit_issue_for = permit_issued_for_str
            if hazard_consideration:
                hazard_consideration_str = ",".join(hazard_consideration) if hazard_consideration else ""
                permit_to_work.hazard_consideration = hazard_consideration_str
            if job_preparation:
                job_preparation_str = ",".join(job_preparation) if job_preparation else ""
                permit_to_work.job_preparation = job_preparation_str
            if fire_protection:
                fire_protection_str = ",".join(fire_protection) if fire_protection else ""
                permit_to_work.fire_protection = fire_protection_str

            if site_name:
                permit_to_work.site_name = site_name
            if department:
                permit_to_work.department = department
            if permit_number:
                permit_to_work.permit_number = permit_number
            if external_agency_name:
                permit_to_work.name_of_external_agency = external_agency_name
            if type_of_permit:
                permit_to_work.type_of_permit = type_of_permit
            if other_permit_description:
                permit_to_work.other_permit_description = other_permit_description
            if day:
                permit_to_work.day = day
            if night:
                permit_to_work.night = night
            if job_activity:
                permit_to_work.job_activity_details = job_activity
            if location_area:
                permit_to_work.location_area = location_area
            if tools_equipment:
                permit_to_work.tools_equipment = tools_equipment
            if other_hazard_consideration:
                permit_to_work.other_hazard_consideration = other_hazard_consideration
            if other_job_preparation:
                permit_to_work.other_job_preparation = other_job_preparation
            if risk_assessment_number:
                permit_to_work.risk_assessment_number = risk_assessment_number
            permit_to_work.save()
            serializer = PermitToWorkSerializer(permit_to_work)
            return Response({"status": True, "message": "Permit to work updated successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


    def destroy(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)
            permit_to_work.delete()
            return Response({"status": True, "message": "Permit to work deleted successfully", "data": []})
        except PermitToWork.DoesNotExist:
            return Response({"status": False, "message": "Permit to work not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})  
        
    
class ApprovePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApprovePermitSerializer
    queryset = ApprovePermit.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)

            issuer = request.data.get('issuer')
            approver = request.data.get('approver')
            receiver = request.data.get('receiver')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')

            issuer_instance = CustomUser.objects.get(id=issuer)
            approver_instance = CustomUser.objects.get(id=approver)
            receiver_instance = CustomUser.objects.get(id=receiver)

            approve_permit = ApprovePermit.objects.create(
                permit=permit_to_work,
                issuer=issuer_instance,
                approver=approver_instance,
                receiver=receiver_instance,
                start_time=start_time,
                end_time=end_time
            )
            serializer = ApprovePermitSerializer(approve_permit)
            return Response({"status": True, "message": "Permit to work approved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ClosureOfPermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ClosureOfPermit.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)
            closer_of_permit = request.data.get('closer_of_permit')
            remarks = request.data.get('remarks')

            closer = ClosureOfPermit.objects.create(
                user=user,
                permit=permit_to_work,
                closer_of_permit=closer_of_permit,
                remarks=remarks
            )
            serializer = ClosureOfPermitSerializer(closer)
            return Response({"status": True, "message": "Closure of permit to work created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class IncidentNearmissInvestigationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentNearMissSerializer
    queryset = IncidentNearMiss.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            site_name = request.data.get('site_name')
            location_id = request.data.get('location')
            date_of_occurrence = request.data.get('date_of_occurrence')
            date_of_report = request.data.get('date_of_report')
            category = request.data.get('category')
            title_incident_nearmiss = request.data.get('title_incident_nearmiss')
            description = request.data.get('description')
            investigation_findings = request.data.get('investigation_findings')
            physical_factor = request.data.get('physical_factor')
            human_factor = request.data.get('human_factor')
            system_factor = request.data.get('system_factor')
            recommendation_for_preventive_action = request.data.get('recommendation_for_preventive_action', {})
            committee_members = request.data.get('committee_members', {})
            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})
            incident_nearmiss = IncidentNearMiss.objects.create(
                user=user,
                site_name=site_name,
                date_of_occurrence=date_of_occurrence,
                date_of_report=date_of_report,
                category=category,
                title_incident_nearmiss=title_incident_nearmiss,
                description=description,
                investigation_findings=investigation_findings,
                physical_factor=physical_factor,
                human_factor=human_factor,
                system_factor=system_factor,
                status='under review',
                recommendation_for_preventive_action=recommendation_for_preventive_action,
                committee_members=committee_members
            )
            serializer = IncidentNearMissSerializer(incident_nearmiss)
            return Response({"status": True, "message": "Incident nearmiss created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class GetIncidentNearmissInvestigationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentNearMissSerializer
    queryset = IncidentNearMiss.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response({"status": True, "message": "Incident nearmisses fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class IDWiseGetIncidentNearmissInvestigationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentNearMissSerializer
    queryset = IncidentNearMiss.objects.all()
    lookup_field = 'incident_nearmiss_id'

    def list(self, request, *args, **kwargs):
        incident_id = kwargs.get('incident_nearmiss_id')
        try:
            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_id)
            serializer = self.serializer_class(incident_nearmiss)
            return Response({"status": True, "message": "Incident nearmiss fetched successfully", "data": serializer.data})
        except IncidentNearMiss.DoesNotExist:
            return Response({"status": False, "message": "Incident nearmiss not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
    

class UpdateIncidentNearmissInvestigationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentNearMissSerializer
    queryset = IncidentNearMiss.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            incident_id = kwargs.get('id')
            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_id)
            site_name = request.data.get('site_name')
            location = request.data.get('location')
            date_of_occurrence = request.data.get('date_of_occurrence')
            date_of_report = request.data.get('date_of_report')
            category = request.data.get('category')
            title_incident_nearmiss = request.data.get('title_incident_nearmiss')
            description = request.data.get('description')
            investigation_findings = request.data.get('investigation_findings')
            physical_factor = request.data.get('physical_factor')
            human_factor = request.data.get('human_factor')
            system_factor = request.data.get('system_factor')
            recommendation_for_preventive_action = request.data.get('recommendation_for_preventive_action', {})
            committee_members = request.data.get('committee_members', {})

            if site_name:
                incident_nearmiss.site_name = site_name
            if location:
                incident_nearmiss.location = location
            if date_of_occurrence:
                incident_nearmiss.date_of_occurrence = date_of_occurrence
            if date_of_report:
                incident_nearmiss.date_of_report = date_of_report
            if category:
                incident_nearmiss.category = category
            if title_incident_nearmiss:
                incident_nearmiss.title_incident_nearmiss = title_incident_nearmiss
            if description:
                incident_nearmiss.description = description
            if investigation_findings:
                incident_nearmiss.investigation_findings = investigation_findings
            if physical_factor:
                incident_nearmiss.physical_factor = physical_factor
            if human_factor:
                incident_nearmiss.human_factor = human_factor
            if system_factor:
                incident_nearmiss.system_factor = system_factor
            if recommendation_for_preventive_action:
                incident_nearmiss.recommendation_for_preventive_action = recommendation_for_preventive_action
            if committee_members:
                incident_nearmiss.committee_members = committee_members

            incident_nearmiss.save()
            serializer = IncidentNearMissSerializer(incident_nearmiss)
            return Response({"status": True, "message": "Incident nearmiss updated successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self,request, *args, **kwargs):
        try:
            incident_id = kwargs.get('id')
            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_id)
            incident_nearmiss.delete()
            return Response({"status": True, "message": "Incident nearmiss deleted successfully", "data": []})
        except IncidentNearMiss.DoesNotExist:
            return Response({"status": False, "message": "Incident nearmiss not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    
class ReviewByIncidentNearmissViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewIncidentNearMissSerializer
    queryset = ReviewIncidentNearMiss.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            incident_id = kwargs.get('id')
            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_id)
            remarks = request.data.get('remarks')

            existing_review = ReviewIncidentNearMiss.objects.filter(incident_nearmiss=incident_nearmiss, reviewer=user).exists()
            if existing_review:
                return Response({"status": False, "message": "You have already reviewed this incident."})

            ReviewIncidentNearMiss.objects.create(
                incident_nearmiss=incident_nearmiss,
                reviewer=user,
                remarks=remarks
            )
            total = CustomUser.objects.filter(review_incident_nearmiss__incident_nearmiss=incident_nearmiss).count()
            reviewed = ReviewIncidentNearMiss.objects.filter(incident_nearmiss=incident_nearmiss).count()

            if reviewed == total:
                incident_nearmiss.status = 'under approval'
            else:
                incident_nearmiss.status = 'reviewed'
            
            incident_nearmiss.save()
            serializer = IncidentNearMissSerializer(incident_nearmiss)
            return Response({"status": True, "message": "Review submitted successfully", "data": serializer.data})
        except IncidentNearMiss.DoesNotExist:
            return Response({"status": False, "message": "Incident nearmiss not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class ApproveByIncidentNearmissViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApproveIncidentNearMissSerializer
    queryset = ApproveIncidentNearMiss.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            incident_id = kwargs.get('id')
            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_id)
            remarks = request.data.get('remarks')

            existing_approval = ApproveIncidentNearMiss.objects.filter(incident_nearmiss=incident_nearmiss, approver=user).exists()
            if existing_approval:
                return Response({"status": False, "message": "You have already approved this incident."})
            
            approve = ApproveIncidentNearMiss.objects.create(
                incident_nearmiss=incident_nearmiss,
                approver=user,
                remarks=remarks
            )

            incident_nearmiss.status = 'approved'
            incident_nearmiss.save()

            serializer = IncidentNearMissSerializer(incident_nearmiss)
            return Response({"status": True, "message": "Review submitted successfully", "data": serializer.data})
        except IncidentNearMiss.DoesNotExist:
            return Response({"status": False, "message": "Incident nearmiss not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ReportOfIncidentNearmissViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportOfIncidentNearmissSerializer


    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            incident_nearmiss_id = kwargs.get('incident_nearmiss_id')
            immediate_action_taken = request.data.get('immediate_action_taken')
            apparent_cause = request.data.get('apparent_cause')
            preventive_action = request.data.get('preventive_action')

            incident_nearmiss = IncidentNearMiss.objects.get(id=incident_nearmiss_id)

            report = ReportOfIncidentNearmiss.objects.create(
                user=user,
                incident_nearmiss=incident_nearmiss,
                immediate_action_taken=immediate_action_taken,
                apparent_cause=apparent_cause,
                preventive_action=preventive_action,
            )
            serializer = ReportOfIncidentNearmissSerializer(report)
            return Response({"status": True, "message": "Report created successfully", "data": serializer.data})
        except IncidentNearMiss.DoesNotExist:
            return Response({"status": False, "message": "Incident nearmiss not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class SafetyViolationReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SafetyViolationReportAgainstUnsafeACTSerializer
    queryset = SafetyViolationReportAgainstUnsafeACT.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            site_name = request.data.get('site_name')
            issued_to = request.data.get('issued_to')
            issued_to_violator_name = request.data.get('issued_to_violator_name')
            issued_to_designation = request.data.get('issued_to_designation')
            issued_to_department = request.data.get('issued_to_department')
            issued_by = request.data.get('issued_by')
            issued_by_name = request.data.get('issued_by_name')
            issued_by_designation = request.data.get('issued_by_designation')
            issued_by_department = request.data.get('issued_by_department')
            contractors_name = request.data.get('contractors_name')
            description_safety_violation = request.data.get('description_safety_violation')
            action_taken = request.data.get('action_taken')

            safety_violation_report = SafetyViolationReportAgainstUnsafeACT.objects.create(
                user=user,
                site_name=site_name,
                issued_to=issued_to,
                issued_to_violator_name=issued_to_violator_name,
                issued_to_designation=issued_to_designation,
                issued_to_department=issued_to_department,
                issued_by=issued_by,
                issued_by_name=issued_by_name,
                issued_by_designation=issued_by_designation,
                issued_by_department=issued_by_department,
                contractors_name=contractors_name,
                description_safety_violation=description_safety_violation,
                action_taken=action_taken,
            )
            serializer = SafetyViolationReportAgainstUnsafeACTSerializer(safety_violation_report)   
            return Response({"status": True, "message": "Safety violation report created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    
class GetSafetyViolationReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SafetyViolationReportAgainstUnsafeACTSerializer
    queryset = SafetyViolationReportAgainstUnsafeACT.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            safety_violation_report = SafetyViolationReportAgainstUnsafeACT.objects.all()
            serializer = SafetyViolationReportAgainstUnsafeACTSerializer(safety_violation_report, many=True)
            return Response({"status": True, "message": "Safety violation report fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class BoomLiftInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoomLiftInspectionSerializer
    queryset = BoomLiftInspection.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            site_name = request.data.get('site_name')
            location = request.data.get('location')
            equipment_name = request.data.get('equipment_name')
            make_model = request.data.get('make_model')
            identification_number = request.data.get('identification_number')
            inspection_date = request.data.get('inspection_date')
            all_valid_document_observations = request.data.get('all_valid_document_observations')
            all_valid_document_action_by = request.data.get('all_valid_document_action_by')
            all_valid_document_remarks = request.data.get('all_valid_document_remarks')
            operator_fitness_certificate_observations = request.data.get('operator_fitness_certificate_observations')
            operator_fitness_certificate_action_by = request.data.get('operator_fitness_certificate_action_by')
            operator_fitness_certificate_remarks = request.data.get('operator_fitness_certificate_remarks')
            main_horn_reverse_horn_observations = request.data.get('main_horn_reverse_horn_observations')
            main_horn_reverse_horn_action_by = request.data.get('main_horn_reverse_horn_action_by')
            main_horn_reverse_horn_remarks = request.data.get('main_horn_reverse_horn_remarks')
            emergency_lowering_observations = request.data.get('emergency_lowering_observations')
            emergency_lowering_action_by = request.data.get('emergency_lowering_action_by')
            emergency_lowering_remarks = request.data.get('emergency_lowering_remarks')
            tyre_pressure_condition_observations = request.data.get('tyre_pressure_condition_observations')
            tyre_pressure_condition_action_by = request.data.get('tyre_pressure_condition_action_by')
            tyre_pressure_condition_remarks = request.data.get('tyre_pressure_condition_remarks')
            any_leakage_observations = request.data.get('any_leakage_observations')
            any_leakage_action_by = request.data.get('any_leakage_action_by')
            any_leakage_remarks = request.data.get('any_leakage_remarks')
            smooth_function_observations = request.data.get('smooth_function_observations')
            smooth_function_action_by = request.data.get('smooth_function_action_by')
            smooth_function_remarks = request.data.get('smooth_function_remarks')
            brake_stop_hold_observations = request.data.get('brake_stop_hold_observations')
            brake_stop_hold_action_by = request.data.get('brake_stop_hold_action_by')
            brake_stop_hold_remarks = request.data.get('brake_stop_hold_remarks')
            condition_of_all_observations = request.data.get('condition_of_all_observations')
            condition_of_all_action_by = request.data.get('condition_of_all_action_by')
            condition_of_all_remarks = request.data.get('condition_of_all_remarks')
            guard_rails_without_damage_observations = request.data.get('guard_rails_without_damage_observations')
            guard_rails_without_damage_action_by = request.data.get('guard_rails_without_damage_action_by')
            guard_rails_without_damage_remarks = request.data.get('guard_rails_without_damage_remarks')
            toe_guard_observations = request.data.get('toe_guard_observations')
            toe_guard_action_by = request.data.get('toe_guard_action_by')
            toe_guard_remarks = request.data.get('toe_guard_remarks')
            platform_condition_observations = request.data.get('platform_condition_observations')
            platform_condition_action_by = request.data.get('platform_condition_action_by')
            platform_condition_remarks = request.data.get('platform_condition_remarks')
            door_lock_platform_observations = request.data.get('door_lock_platform_observations')
            door_lock_platform_action_by = request.data.get('door_lock_platform_action_by')
            door_lock_platform_remarks = request.data.get('door_lock_platform_remarks')
            swl_observations = request.data.get('swl_observations')
            swl_action_by = request.data.get('swl_action_by')
            swl_remarks = request.data.get('swl_remarks')
            over_load_indicator_cut_off_devices_observations = request.data.get('over_load_indicator_cut_off_devices_observations')
            over_load_indicator_cut_off_devices_action_by = request.data.get('over_load_indicator_cut_off_devices_action_by')
            over_load_indicator_cut_off_devices_remarks = request.data.get('over_load_indicator_cut_off_devices_remarks')
            battery_condition_observations = request.data.get('battery_condition_observations')
            battery_condition_action_by = request.data.get('battery_condition_action_by')
            battery_condition_remarks = request.data.get('battery_condition_remarks')
            operator_list_observations = request.data.get('operator_list_observations')
            operator_list_action_by = request.data.get('operator_list_action_by')
            operator_list_remarks = request.data.get('operator_list_remarks')
            ppe_observations = request.data.get('ppe_observations')
            ppe_action_by = request.data.get('ppe_action_by')
            ppe_remarks = request.data.get('ppe_remarks')

            boom_lift_inspection = BoomLiftInspection.objects.create(
                user=user,
                site_name=site_name,
                location=location,
                equipment_name=equipment_name,
                make_model=make_model,
                identification_number=identification_number,
                inspection_date=inspection_date,
                all_valid_document_observations=all_valid_document_observations,
                all_valid_document_action_by=all_valid_document_action_by,
                all_valid_document_remarks=all_valid_document_remarks,
                operator_fitness_certificate_observations=operator_fitness_certificate_observations,
                operator_fitness_certificate_action_by=operator_fitness_certificate_action_by,
                operator_fitness_certificate_remarks=operator_fitness_certificate_remarks,
                main_horn_reverse_horn_observations=main_horn_reverse_horn_observations,
                main_horn_reverse_horn_action_by=main_horn_reverse_horn_action_by,
                main_horn_reverse_horn_remarks=main_horn_reverse_horn_remarks,
                emergency_lowering_observations=emergency_lowering_observations,
                emergency_lowering_action_by=emergency_lowering_action_by,
                emergency_lowering_remarks=emergency_lowering_remarks,
                tyre_pressure_condition_observations=tyre_pressure_condition_observations,
                tyre_pressure_condition_action_by=tyre_pressure_condition_action_by,
                tyre_pressure_condition_remarks=tyre_pressure_condition_remarks,
                any_leakage_observations=any_leakage_observations,
                any_leakage_action_by=any_leakage_action_by,
                any_leakage_remarks=any_leakage_remarks,
                smooth_function_observations=smooth_function_observations,
                smooth_function_action_by=smooth_function_action_by,
                smooth_function_remarks=smooth_function_remarks,
                brake_stop_hold_observations=brake_stop_hold_observations,
                brake_stop_hold_action_by=brake_stop_hold_action_by,
                brake_stop_hold_remarks=brake_stop_hold_remarks,
                condition_of_all_observations=condition_of_all_observations,
                condition_of_all_action_by=condition_of_all_action_by,
                condition_of_all_remarks=condition_of_all_remarks,
                guard_rails_without_damage_observations=guard_rails_without_damage_observations,
                guard_rails_without_damage_action_by=guard_rails_without_damage_action_by,
                guard_rails_without_damage_remarks=guard_rails_without_damage_remarks,
                toe_guard_observations=toe_guard_observations,
                toe_guard_action_by=toe_guard_action_by,
                toe_guard_remarks=toe_guard_remarks,
                platform_condition_observations=platform_condition_observations,
                platform_condition_action_by=platform_condition_action_by,
                platform_condition_remarks=platform_condition_remarks,
                door_lock_platform_observations=door_lock_platform_observations,
                door_lock_platform_action_by=door_lock_platform_action_by,
                door_lock_platform_remarks=door_lock_platform_remarks,
                swl_observations=swl_observations,
                swl_action_by=swl_action_by,
                swl_remarks=swl_remarks,
                over_load_indicator_cut_off_devices_observations=over_load_indicator_cut_off_devices_observations,
                over_load_indicator_cut_off_devices_action_by=over_load_indicator_cut_off_devices_action_by,
                over_load_indicator_cut_off_devices_remarks=over_load_indicator_cut_off_devices_remarks,
                battery_condition_observations=battery_condition_observations,
                battery_condition_action_by=battery_condition_action_by,
                battery_condition_remarks=battery_condition_remarks,
                operator_list_observations=operator_list_observations,
                operator_list_action_by=operator_list_action_by,
                operator_list_remarks=operator_list_remarks,
                ppe_observations=ppe_observations,
                ppe_action_by=ppe_action_by,
                ppe_remarks=ppe_remarks
            )
            serializer = BoomLiftInspectionSerializer(boom_lift_inspection)
            return Response({"status": True, "message": "Boom lift inspection created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class GetBoomLiftInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoomLiftInspectionSerializer

    def list(self, request, *args, **kwargs):
        try:
            boom_lift = BoomLiftInspection.objects.all().order_by('-id')
            serializer = BoomLiftInspectionSerializer(boom_lift, many=True)
            return Response({"status": True, "message": "Boom lift inspection fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class CraneHydraInspectionChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CraneHydraInspectionsSerializer
    queryset = CraneHydraInspections.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            equipment_name = request.data.get('equipment_name')
            make_model = request.data.get('make_model')
            identification_number = request.data.get('identification_number')
            inspection_date = request.data.get('inspection_date')
            site_name = request.data.get('site_name')
            location = request.data.get('location')
            all_valid_document_observations = request.data.get('all_valid_document_observations')
            all_valid_document_action_by = request.data.get('all_valid_document_action_by')
            all_valid_document_remarks = request.data.get('all_valid_document_remarks')
            driver_fitness_certificate_observations = request.data.get('driver_fitness_certificate_observations')
            driver_fitness_certificate_action_by = request.data.get('driver_fitness_certificate_action_by')
            driver_fitness_certificate_remarks = request.data.get('driver_fitness_certificate_remarks')
            main_horn_reverse_horn_observations = request.data.get('main_horn_reverse_horn_observations')
            main_horn_reverse_horn_action_by = request.data.get('main_horn_reverse_horn_action_by')
            main_horn_reverse_horn_remarks = request.data.get('main_horn_reverse_horn_remarks')
            cutch_brake_observations = request.data.get('cutch_brake_observations')
            cutch_brake_action_by = request.data.get('cutch_brake_action_by')
            cutch_brake_remarks = request.data.get('cutch_brake_remarks')
            tyre_pressure_condition_observations = request.data.get('tyre_pressure_condition_observations')
            tyre_pressure_condition_action_by = request.data.get('tyre_pressure_condition_action_by')
            tyre_pressure_condition_remarks = request.data.get('tyre_pressure_condition_remarks')
            head_light_indicator_observations = request.data.get('head_light_indicator_observations')
            head_light_indicator_action_by = request.data.get('head_light_indicator_action_by')
            head_light_indicator_remarks = request.data.get('head_light_indicator_remarks')
            seat_belt_observations = request.data.get('seat_belt_observations')
            seat_belt_action_by = request.data.get('seat_belt_action_by')
            seat_belt_remarks = request.data.get('seat_belt_remarks')
            wiper_blade_observations = request.data.get('wiper_blade_observations')
            wiper_blade_action_by = request.data.get('wiper_blade_action_by')
            wiper_blade_remarks = request.data.get('wiper_blade_remarks')
            side_mirror_observations = request.data.get('side_mirror_observations')
            side_mirror_action_by = request.data.get('side_mirror_action_by')
            side_mirror_remarks = request.data.get('side_mirror_remarks')
            wind_screen_observations = request.data.get('wind_screen_observations')
            wind_screen_action_by = request.data.get('wind_screen_action_by')
            wind_screen_remarks = request.data.get('wind_screen_remarks')
            door_lock_observations = request.data.get('door_lock_observations')
            door_lock_action_by = request.data.get('door_lock_action_by')
            door_lock_remarks = request.data.get('door_lock_remarks')
            battery_condition_observations = request.data.get('battery_condition_observations')
            battery_condition_action_by = request.data.get('battery_condition_action_by')
            battery_condition_remarks = request.data.get('battery_condition_remarks')
            hand_brake_observations = request.data.get('hand_brake_observations')
            hand_brake_action_by = request.data.get('hand_brake_action_by')
            hand_brake_remarks = request.data.get('hand_brake_remarks')
            swl_on_boom_lift_observations = request.data.get('swl_on_boom_lift_observations')
            swl_on_boom_lift_action_by = request.data.get('swl_on_boom_lift_action_by')
            swl_on_boom_lift_remarks = request.data.get('swl_on_boom_lift_remarks')
            any_leakage_observations = request.data.get('any_leakage_observations')
            any_leakage_action_by = request.data.get('any_leakage_action_by')
            any_leakage_remarks = request.data.get('any_leakage_remarks')
            speedometere_observations = request.data.get('speedometere_observations')
            speedometere_action_by = request.data.get('speedometere_action_by')
            speedometere_remarks = request.data.get('speedometere_remarks')
            guard_parts_observations = request.data.get('guard_parts_observations')
            guard_parts_action_by = request.data.get('guard_parts_action_by')
            guard_parts_remarks = request.data.get('guard_parts_remarks')
            ppe_observations = request.data.get('ppe_observations')
            ppe_action_by = request.data.get('ppe_action_by')
            ppe_remarks = request.data.get('ppe_remarks')

            crane_hydra_inspection = CraneHydraInspections.objects.create(
                user=user,
                equipment_name=equipment_name,
                make_model=make_model,
                identification_number=identification_number,
                inspection_date=inspection_date,
                site_name=site_name,
                location=location,
                all_valid_document_observations=all_valid_document_observations,
                all_valid_document_action_by=all_valid_document_action_by,
                all_valid_document_remarks=all_valid_document_remarks,
                driver_fitness_certificate_observations=driver_fitness_certificate_observations,
                driver_fitness_certificate_action_by=driver_fitness_certificate_action_by,
                driver_fitness_certificate_remarks=driver_fitness_certificate_remarks,
                main_horn_reverse_horn_observations=main_horn_reverse_horn_observations,
                main_horn_reverse_horn_action_by=main_horn_reverse_horn_action_by,
                main_horn_reverse_horn_remarks=main_horn_reverse_horn_remarks,
                cutch_brake_observations=cutch_brake_observations,
                cutch_brake_action_by=cutch_brake_action_by,
                cutch_brake_remarks=cutch_brake_remarks,
                tyre_pressure_condition_observations=tyre_pressure_condition_observations,
                tyre_pressure_condition_action_by=tyre_pressure_condition_action_by,
                tyre_pressure_condition_remarks=tyre_pressure_condition_remarks,
                head_light_indicator_observations=head_light_indicator_observations,
                head_light_indicator_action_by=head_light_indicator_action_by,
                head_light_indicator_remarks=head_light_indicator_remarks,
                seat_belt_observations=seat_belt_observations,
                seat_belt_action_by=seat_belt_action_by,
                seat_belt_remarks=seat_belt_remarks,
                wiper_blade_observations=wiper_blade_observations,
                wiper_blade_action_by=wiper_blade_action_by,
                wiper_blade_remarks=wiper_blade_remarks,
                side_mirror_observations=side_mirror_observations,
                side_mirror_action_by=side_mirror_action_by,
                side_mirror_remarks=side_mirror_remarks,
                wind_screen_observations=wind_screen_observations,
                wind_screen_action_by=wind_screen_action_by,
                wind_screen_remarks=wind_screen_remarks,
                door_lock_observations=door_lock_observations,
                door_lock_action_by=door_lock_action_by,
                door_lock_remarks=door_lock_remarks,
                battery_condition_observations=battery_condition_observations,
                battery_condition_action_by=battery_condition_action_by,
                battery_condition_remarks=battery_condition_remarks,
                hand_brake_observations=hand_brake_observations,
                hand_brake_action_by=hand_brake_action_by,
                hand_brake_remarks=hand_brake_remarks,
                swl_on_boom_lift_observations=swl_on_boom_lift_observations,
                swl_on_boom_lift_action_by=swl_on_boom_lift_action_by,
                swl_on_boom_lift_remarks=swl_on_boom_lift_remarks,
                any_leakage_observations=any_leakage_observations,
                any_leakage_action_by=any_leakage_action_by,
                any_leakage_remarks=any_leakage_remarks,
                speedometere_observations=speedometere_observations,
                speedometere_action_by=speedometere_action_by,
                speedometere_remarks=speedometere_remarks,
                guard_parts_observations=guard_parts_observations,
                guard_parts_action_by=guard_parts_action_by,
                guard_parts_remarks=guard_parts_remarks,
                ppe_observations=ppe_observations,
                ppe_action_by=ppe_action_by,
                ppe_remarks=ppe_remarks
            )

            serializer = CraneHydraInspectionsSerializer(crane_hydra_inspection)
            return Response({"status": True, "message": "Crane hydra inspection created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})


class GetCraneHydraInspectionChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CraneHydraInspectionsSerializer
    queryset = CraneHydraInspections.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = CraneHydraInspections.objects.all()
            serializer = CraneHydraInspectionsSerializer(queryset, many=True)
            return Response({"status": True, "message": "Crane hydra inspection checklist retrieved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class TrailerInspectionChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TrailerInspectionChecklistSerializer
    queryset = TrailerInspectionChecklist.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            equipment_name = request.data.get('equipment_name')
            make_model = request.data.get('make_model')
            identification_number = request.data.get('identification_number')
            inspection_date = request.data.get('inspection_date')
            site_name = request.data.get('site_name')
            location = request.data.get('location')
            all_valid_document_observations = request.data.get('all_valid_document_observations')
            all_valid_document_action_by = request.data.get('all_valid_document_action_by')
            all_valid_document_remarks = request.data.get('all_valid_document_remarks')
            driver_fitness_certificate_observations = request.data.get('driver_fitness_certificate_observations')
            driver_fitness_certificate_action_by = request.data.get('driver_fitness_certificate_action_by')
            driver_fitness_certificate_remarks = request.data.get('driver_fitness_certificate_remarks')
            main_horn_reverse_horn_observations = request.data.get('main_horn_reverse_horn_observations')
            main_horn_reverse_horn_action_by = request.data.get('main_horn_reverse_horn_action_by')
            main_horn_reverse_horn_remarks = request.data.get('main_horn_reverse_horn_remarks')
            cutch_brake_observations = request.data.get('cutch_brake_observations')
            cutch_brake_action_by = request.data.get('cutch_brake_action_by')
            cutch_brake_remarks = request.data.get('cutch_brake_remarks')
            tyre_pressure_condition_observations = request.data.get('tyre_pressure_condition_observations')
            tyre_pressure_condition_action_by = request.data.get('tyre_pressure_condition_action_by')
            tyre_pressure_condition_remarks = request.data.get('tyre_pressure_condition_remarks')
            head_light_indicator_observations = request.data.get('head_light_indicator_observations')
            head_light_indicator_action_by = request.data.get('head_light_indicator_action_by')
            head_light_indicator_remarks = request.data.get('head_light_indicator_remarks')
            seat_belt_observations = request.data.get('seat_belt_observations')
            seat_belt_action_by = request.data.get('seat_belt_action_by')
            seat_belt_remarks = request.data.get('seat_belt_remarks')
            wiper_blade_observations = request.data.get('wiper_blade_observations')
            wiper_blade_action_by = request.data.get('wiper_blade_action_by')
            wiper_blade_remarks = request.data.get('wiper_blade_remarks')
            side_mirror_observations = request.data.get('side_mirror_observations')
            side_mirror_action_by = request.data.get('side_mirror_action_by')
            side_mirror_remarks = request.data.get('side_mirror_remarks')
            wind_screen_observations = request.data.get('wind_screen_observations')
            wind_screen_action_by = request.data.get('wind_screen_action_by')
            wind_screen_remarks = request.data.get('wind_screen_remarks')
            door_lock_action_by = request.data.get('door_lock_action_by')
            door_lock_remarks = request.data.get('door_lock_remarks')
            door_lock_observations = request.data.get('door_lock_observations')
            battery_condition_observations = request.data.get('battery_condition_observations')
            battery_condition_action_by = request.data.get('battery_condition_action_by')
            battery_condition_remarks = request.data.get('battery_condition_remarks')
            hand_brake_observations = request.data.get('hand_brake_observations')
            hand_brake_action_by = request.data.get('hand_brake_action_by')
            hand_brake_remarks = request.data.get('hand_brake_remarks')
            any_leakage_observations = request.data.get('any_leakage_observations')
            any_leakage_action_by = request.data.get('any_leakage_action_by')
            any_leakage_remarks = request.data.get('any_leakage_remarks')
            speedometere_observations = request.data.get('speedometere_observations')
            speedometere_action_by = request.data.get('speedometere_action_by')
            speedometere_remarks = request.data.get('speedometere_remarks')
            guard_parts_observations = request.data.get('guard_parts_observations')
            guard_parts_action_by = request.data.get('guard_parts_action_by')
            guard_parts_remarks = request.data.get('guard_parts_remarks')
            ppe_observations = request.data.get('ppe_observations')
            ppe_action_by = request.data.get('ppe_action_by')
            ppe_remarks = request.data.get('ppe_remarks')

            trailer_inspection = TrailerInspectionChecklist.objects.create(
                user=user,
                equipment_name=equipment_name,
                make_model=make_model,
                identification_number=identification_number,
                inspection_date=inspection_date,
                site_name=site_name,
                location=location,
                all_valid_document_observations=all_valid_document_observations,
                all_valid_document_action_by=all_valid_document_action_by,
                all_valid_document_remarks=all_valid_document_remarks,
                driver_fitness_certificate_observations=driver_fitness_certificate_observations,
                driver_fitness_certificate_action_by=driver_fitness_certificate_action_by,
                driver_fitness_certificate_remarks=driver_fitness_certificate_remarks,
                main_horn_reverse_horn_observations=main_horn_reverse_horn_observations,
                main_horn_reverse_horn_action_by=main_horn_reverse_horn_action_by,
                main_horn_reverse_horn_remarks=main_horn_reverse_horn_remarks,
                cutch_brake_observations=cutch_brake_observations,
                cutch_brake_action_by=cutch_brake_action_by,
                cutch_brake_remarks=cutch_brake_remarks,
                tyre_pressure_condition_observations=tyre_pressure_condition_observations,
                tyre_pressure_condition_action_by=tyre_pressure_condition_action_by,
                tyre_pressure_condition_remarks=tyre_pressure_condition_remarks,
                head_light_indicator_observations=head_light_indicator_observations,
                head_light_indicator_action_by=head_light_indicator_action_by,
                head_light_indicator_remarks=head_light_indicator_remarks,
                seat_belt_observations=seat_belt_observations,
                seat_belt_action_by=seat_belt_action_by,
                seat_belt_remarks=seat_belt_remarks,
                wiper_blade_observations=wiper_blade_observations,
                wiper_blade_action_by=wiper_blade_action_by,
                wiper_blade_remarks=wiper_blade_remarks,
                side_mirror_observations=side_mirror_observations,
                side_mirror_action_by=side_mirror_action_by,
                side_mirror_remarks=side_mirror_remarks,
                wind_screen_observations=wind_screen_observations,
                wind_screen_action_by=wind_screen_action_by,
                wind_screen_remarks=wind_screen_remarks,
                door_lock_action_by=door_lock_action_by,
                door_lock_remarks=door_lock_remarks,
                door_lock_observations=door_lock_observations,
                battery_condition_observations=battery_condition_observations,
                battery_condition_action_by=battery_condition_action_by,
                battery_condition_remarks=battery_condition_remarks,
                hand_brake_observations=hand_brake_observations,
                hand_brake_action_by=hand_brake_action_by,
                hand_brake_remarks=hand_brake_remarks,
                any_leakage_observations=any_leakage_observations,
                any_leakage_action_by=any_leakage_action_by,
                any_leakage_remarks=any_leakage_remarks,
                speedometere_observations=speedometere_observations,
                speedometere_action_by=speedometere_action_by,
                speedometere_remarks=speedometere_remarks,
                guard_parts_observations=guard_parts_observations,
                guard_parts_action_by=guard_parts_action_by,
                guard_parts_remarks=guard_parts_remarks,
                ppe_observations=ppe_observations,
                ppe_action_by=ppe_action_by,
                ppe_remarks=ppe_remarks
            )
            serializer = TrailerInspectionChecklistSerializer(trailer_inspection)
            return Response({"status": True, "message": "Trailer inspection created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetTrailerInspectionChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TrailerInspectionChecklistSerializer

    def list(self, request, *args, **kwargs):
        try:
            trailer_inspection = TrailerInspectionChecklist.objects.all().order_by('-id')
            serializer = TrailerInspectionChecklistSerializer(trailer_inspection, many=True)
            return Response({"status": True, "message": "Trailer inspection fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class MockDrillReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MockDrillReportSerializer
    queryset = MockDrillReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            site_plant_name = request.data.get('site_plant_name')
            location = request.data.get('location')
            emergncy_scenario_mock_drill = request.data.get('emergncy_scenario_mock_drill')
            type_of_mock_drill = request.data.get('type_of_mock_drill')
            mock_drill_date = request.data.get('mock_drill_date')
            mock_drill_time = request.data.get('mock_drill_time')
            completed_time = request.data.get('completed_time')
            overall_time = request.data.get('overall_time')
            team_leader_incident_controller = request.data.get('team_leader_incident_controller')
            performance = request.data.get('performance')
            traffic_or_evacuation = request.data.get('traffic_or_evacuation')
            ambulance_first_aid_ppe_rescue = request.data.get('ambulance_first_aid_ppe_rescue')
            team_member1 = request.data.get('team_member1')
            team_member2 = request.data.get('team_member2')
            table_top_records = request.data.get('table_top_records', {})
            description_of_control = request.data.get('description_of_control')
            head_count_at_assembly_point = request.data.get('head_count_at_assembly_point', {})
            rating_of_emergency_team_members = request.data.get('rating_of_emergency_team_members', {})
            overall_rating = request.data.get('overall_rating')
            observation = request.data.get('observation')
            recommendations = request.data.get('recommendations', {})

            mock_drill_report = MockDrillReport.objects.create(
                user=user,
                site_plant_name=site_plant_name,
                location=location,
                emergncy_scenario_mock_drill=emergncy_scenario_mock_drill,
                type_of_mock_drill=type_of_mock_drill,
                mock_drill_date=mock_drill_date,
                mock_drill_time=mock_drill_time,
                completed_time=completed_time,
                overall_time=overall_time,
                team_leader_incident_controller=team_leader_incident_controller,
                performance=performance,
                traffic_or_evacuation=traffic_or_evacuation,
                ambulance_first_aid_ppe_rescue=ambulance_first_aid_ppe_rescue,
                team_member1=team_member1,
                team_member2=team_member2,
                table_top_records=table_top_records,
                description_of_control=description_of_control,
                head_count_at_assembly_point=head_count_at_assembly_point,
                rating_of_emergency_team_members=rating_of_emergency_team_members,
                overall_rating=overall_rating,
                observation=observation,
                recommendations=recommendations
            )
            serializer = MockDrillReportSerializer(mock_drill_report)
            return Response({"status": True, "message": "Mock drill report created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetMockDrillReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MockDrillReportSerializer

    def list(self, request, *args, **kwargs):
        try:
            mock_drill_report = MockDrillReport.objects.all().order_by('-id')
            serializer = MockDrillReportSerializer(mock_drill_report, many=True)
            return Response({"status": True, "message": "Mock drill report fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
