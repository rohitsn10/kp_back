from django.shortcuts import render
from user_profile.models import *
from annexures_module.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from annexures_module.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.files.storage import default_storage
import json
from django.core.files.base import ContentFile  

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
            permit_date = request.data.get('permit_date')
            external_agency_name = request.data.get('external_agency_name')
            type_of_permit = request.data.get('type_of_permit')
            other_permit_description = request.data.get('other_permit_description')
            permit_valid_from = request.data.get('permit_valid_from')
            permit_valid_to = request.data.get('permit_valid_to')
            permit_risk_type = request.data.get('permit_risk_type')
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
            issuer_name = request.data.get('issuer_name')
            issuer_sign = request.data.get('issuer_sign')
            
            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})
                
            if isinstance(hazard_consideration, str):
                try:
                    hazard_consideration = json.loads(hazard_consideration)
                except json.JSONDecodeError:
                    hazard_consideration = []

            if isinstance(job_preparation, str):
                try:
                    job_preparation = json.loads(job_preparation)
                except json.JSONDecodeError:
                    job_preparation = []

            if isinstance(fire_protection, str):
                try:
                    fire_protection = json.loads(fire_protection)
                except json.JSONDecodeError:
                    fire_protection = []
    
            permit_issued_for_str = ",".join(permit_issued_for) if permit_issued_for else ""
            hazard_consideration_str = ",".join(hazard_consideration) if hazard_consideration else ""
            fire_protection_str = ",".join(fire_protection) if fire_protection else ""
            job_preparation_str = ",".join(job_preparation) if job_preparation else ""

            # if type_of_permit == "cold work":
            #     expiry_date = timezone.now() + timezone.timedelta(days=25)
            # else:
            #     expiry_date = timezone.now() + timezone.timedelta(hours=24)
                # expiry_date = timezone.now() + timezone.timedelta(minutes=1) #temporary

            permit_to_work = PermitToWork.objects.create(
                user=user,
                location=location_instance,
                site_name=site_name,
                department=department,
                permit_number=permit_number,
                permit_date=permit_date,
                name_of_external_agency=external_agency_name,
                type_of_permit=type_of_permit,
                other_permit_description = other_permit_description,
                permit_valid_from=permit_valid_from,
                permit_valid_to=permit_valid_to,
                permit_risk_type=permit_risk_type,
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
                # expiry_date=expiry_date,
                issuer_name=issuer_name,
                issuer_sign=issuer_sign
            )
            permit_to_work.issuer_done = True
            permit_to_work.save()
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
        
    
class IssueApprovePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueApprovePermitSerializer
    queryset = IssueApprovePermit.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)

            # issuer = request.data.get('issuer')
            issuer_name = request.data.get('issuer_name')
            issuer_sign = request.data.get('issuer_sign')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')

            # issuer_instance = CustomUser.objects.get(id=issuer)
            # approver_instance = CustomUser.objects.get(id=approver)
            # receiver_instance = CustomUser.objects.get(id=receiver)

            approve_permit = IssueApprovePermit.objects.create(
                permit=permit_to_work,
                issuer_name=issuer_name,
                issuer_sign=issuer_sign,
                start_time=start_time,
                end_time=end_time
            )
            permit_to_work.issuer_done = True
            permit_to_work.approver_done = False
            permit_to_work.save()
            serializer = IssueApprovePermitSerializer(approve_permit)
            return Response({"status": True, "message": "Permit to work approved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class IssueGetPermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueApprovePermitSerializer
    queryset = IssueApprovePermit.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            # permit_to_work = PermitToWork.objects.get(id=permit_id)
            queryset = self.filter_queryset(self.get_queryset())
            if permit_id:
                queryset = queryset.filter(permit=permit_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ApproverApprovePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApproverApprovePermitSerializer
    queryset = ApproverApprovePermit.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)

            approver_name = request.data.get('approver_name')
            approver_sign = request.data.get('approver_sign')
            approver_status = request.data.get('approver_status')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')

            approve_permit = ApproverApprovePermit.objects.create(
                permit=permit_to_work,
                approver_name=approver_name,
                approver_sign=approver_sign,
                approver_status=approver_status,
                start_time=start_time,
                end_time=end_time
            )
            if approver_status == "approved":
                permit_to_work.approver_done = True
                permit_to_work.receiver_done = False
            # permit_to_work.approver_done = False
            # permit_to_work.receiver_done = False
                permit_to_work.save()
            serializer = ApproverApprovePermitSerializer(approve_permit)
            return Response({"status": True, "message": "Permit to work approved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ApproverGetPermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApproverApprovePermitSerializer
    queryset = ApproverApprovePermit.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            queryset = self.filter_queryset(self.get_queryset())
            if permit_id:
                queryset = queryset.filter(permit=permit_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class RecevierApprovePermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceiverApprovePermitSerializer
    queryset = ReceiverApprovePermit.objects.all()
    lookup_field = 'permit_id'

    def update(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            permit_to_work = PermitToWork.objects.get(id=permit_id)

            receiver_name = request.data.get('receiver_name')
            receiver_sign = request.data.get('receiver_sign')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')

            approve_permit = ReceiverApprovePermit.objects.create(
                permit=permit_to_work,
                receiver_name=receiver_name,
                receiver_sign=receiver_sign,
                start_time=start_time,
                end_time=end_time
            )
            permit_to_work.receiver_done = True
            permit_to_work.issuer_done = False
            permit_to_work.save()
            serializer = ReceiverApprovePermitSerializer(approve_permit)
            return Response({"status": True, "message": "Permit to work approved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ReceiverGetPermitToWorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceiverApprovePermitSerializer
    queryset = ReceiverApprovePermit.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            permit_id = kwargs.get('permit_id')
            queryset = self.filter_queryset(self.get_queryset())
            if permit_id:
                queryset = queryset.filter(permit=permit_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            remarks = request.data.get('closure_remarks')
            inspector_name = request.data.get('inspector_name')
            closure_sign = request.FILES.get('closure_sign')
            closure_time = request.data.get('closure_time')

            closer = ClosureOfPermit.objects.create(
                user=user,
                permit=permit_to_work,
                inspector_name=inspector_name,
                closure_sign=closure_sign,
                closure_remarks=remarks,
                closure_time=closure_time
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
            committee_members = []
            index = 0
            while True:
                name = request.data.get(f'committee_member_name_{index}')
                rank = request.data.get(f'committee_member_rank_{index}')
                signature = request.FILES.get(f'committee_member_signature_{index}')

                if not name and not signature:
                    break

                signature_path = None
                if signature:
                    file_name = default_storage.save(f"incident_nearmiss/committee_members/{signature.name}", signature)
                    signature_path = default_storage.url(file_name)

                member = {
                    "name": name,
                    "rank": rank,
                    "signature": signature_path
                }
                committee_members.append(member)
                index += 1
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
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
    queryset = ReportOfIncidentNearmiss.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            location = request.data.get('location')
            site_name = request.data.get('site_name')
            date_of_occurrence = request.data.get('date_of_occurrence')
            date_of_report = request.data.get('date_of_report')
            reported_by = request.data.get('reported_by')
            designation = request.data.get('designation')
            employee_code = request.data.get('employee_code')
            vendor_name = request.data.get('vendor_name')
            category = request.data.get('category')
            description = request.data.get('description')
            member_1 = request.data.get('member_1')
            member_2 = request.data.get('member_2')
            member_3 = request.data.get('member_3')
            member_1_sign = request.FILES.get('member_1_sign')
            member_2_sign = request.FILES.get('member_2_sign')
            member_3_sign = request.FILES.get('member_3_sign')
            site_incharge_name = request.data.get('site_incharge_name')
            site_incharge_designation = request.data.get('site_incharge_designation')
            site_incharge_sign  = request.FILES.get('site_incharge_sign')
            immediate_action_taken = request.data.get('immediate_action_taken')
            apparent_cause = request.data.get('apparent_cause')
            preventive_action = request.data.get('preventive_action')

            location_instance = None
            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})


            report = ReportOfIncidentNearmiss.objects.create(
                user=user,
                location=location_instance,
                site_name=site_name,
                date_of_occurrence=date_of_occurrence,
                date_of_report=date_of_report,
                reported_by=reported_by,
                designation=designation,
                employee_code=employee_code,
                vendor_name=vendor_name,
                category=category,
                description=description,
                member_1=member_1,
                member_2=member_2,
                member_3=member_3,
                member_1_sign=member_1_sign,
                member_2_sign=member_2_sign,
                member_3_sign=member_3_sign,
                site_incharge_name=site_incharge_name,
                site_incharge_designation=site_incharge_designation,
                site_incharge_sign=site_incharge_sign,
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
        
class GetReportOfIncidentNearmissViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportOfIncidentNearmissSerializer
    queryset = ReportOfIncidentNearmiss.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            location = request.data.get('location')
            issued_to = request.data.get('issued_to')
            issued_to_violator_name = request.data.get('issued_to_violator_name')
            issued_to_designation = request.data.get('issued_to_designation')
            issued_to_department = request.data.get('issued_to_department')
            issued_to_sign = request.FILES.get('issued_to_sign')
            issued_by = request.data.get('issued_by')
            issued_by_name = request.data.get('issued_by_name')
            issued_by_designation = request.data.get('issued_by_designation')
            issued_by_department = request.data.get('issued_by_department')
            issued_by_sign = request.FILES.get('issued_by_sign')
            contractors_name = request.data.get('contractors_name')
            description_safety_violation = request.data.get('description_safety_violation')
            action_taken = request.data.get('action_taken')
            hseo_name = request.data.get('hseo_name')
            hseo_sign = request.FILES.get('hseo_sign')
            site_incharge_name = request.data.get('site_incharge_name')
            site_incharge_sign = request.FILES.get('site_incharge_sign')
            manager_name = request.data.get('manager_name')
            manager_sign = request.FILES.get('manager_sign')

            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            safety_violation_report = SafetyViolationReportAgainstUnsafeACT.objects.create(
                user=user,
                site_name=site_name,
                location=location_instance,
                issued_to=issued_to,
                issued_to_violator_name=issued_to_violator_name,
                issued_to_designation=issued_to_designation,
                issued_to_department=issued_to_department,
                issued_to_sign=issued_to_sign,
                issued_by=issued_by,
                issued_by_name=issued_by_name,
                issued_by_designation=issued_by_designation,
                issued_by_department=issued_by_department,
                issued_by_sign=issued_by_sign,
                contractors_name=contractors_name,
                description_safety_violation=description_safety_violation,
                action_taken=action_taken,
                hseo_name=hseo_name,
                hseo_sign=hseo_sign,
                site_incharge_name=site_incharge_name,
                site_incharge_sign=site_incharge_sign,
                manager_name=manager_name,
                manager_sign=manager_sign
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
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            inspected_name = request.data.get('inspected_name')
            inspected_sign = request.FILES.get('inspected_sign', [])

            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            boom_lift_inspection = BoomLiftInspection.objects.create(
                user=user,
                site_name=site_name,
                location=location_instance,
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
                ppe_remarks=ppe_remarks,
                inspected_name=inspected_name,
                inspected_sign=inspected_sign
            )
            serializer = BoomLiftInspectionSerializer(boom_lift_inspection)
            return Response({"status": True, "message": "Boom lift inspection created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class GetBoomLiftInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoomLiftInspectionSerializer
    queryset = BoomLiftInspection.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            inspected_name = request.data.get('inspected_name')
            inspected_sign = request.FILES.get('inspected_sign', [])

            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            crane_hydra_inspection = CraneHydraInspections.objects.create(
                user=user,
                equipment_name=equipment_name,
                make_model=make_model,
                identification_number=identification_number,
                inspection_date=inspection_date,
                site_name=site_name,
                location=location_instance,
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
                ppe_remarks=ppe_remarks,
                inspected_name=inspected_name,
                inspected_sign=inspected_sign
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
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            inspected_name = request.data.get('inspected_name')
            inspected_sign = request.FILES.get('inspected_sign', [])

            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            trailer_inspection = TrailerInspectionChecklist.objects.create(
                user=user,
                equipment_name=equipment_name,
                make_model=make_model,
                identification_number=identification_number,
                inspection_date=inspection_date,
                site_name=site_name,
                location=location_instance,
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
                ppe_remarks=ppe_remarks,
                inspected_name=inspected_name,
                inspected_sign=inspected_sign
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
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
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
            location_id = request.data.get('location')
            emergncy_scenario_mock_drill = request.data.get('emergncy_scenario_mock_drill')
            type_of_mock_drill = request.data.get('type_of_mock_drill')
            mock_drill_date = request.data.get('mock_drill_date')
            mock_drill_time = request.data.get('mock_drill_time')
            completed_time = request.data.get('completed_time')
            overall_time = request.data.get('overall_time')
            table_top_records = request.data.get('table_top_records', {})
            description_of_control = request.data.get('description_of_control')
            rating_data_raw = request.data.get('rating_of_emergency_team_members', '[]')
            rating_of_emergency_team_members = json.loads(rating_data_raw)
            overall_rating = request.data.get('overall_rating')
            observation = request.data.get('observation')
            recommendations_data_raw = request.data.get('recommendations', '{}')
            recommendations = json.loads(recommendations_data_raw)
            
            head_count_at_assembly_point = {
                "people_present_as_per_record": {
                    "no_of_kpi_employee": request.data.get('no_of_kpi_employee'),
                    "no_of_contractor_employee": request.data.get('no_of_contractor_employee'),
                    "no_of_visitor_angies": request.data.get('no_of_visitor_angies'),
                    "head_count_remarks": request.data.get('head_count_remarks')
                },
                "actual_participants_participate_in_drill": {
                    "no_of_kpi_employee": request.data.get('no_of_kpi_employee'),
                    "no_of_contractor_employee": request.data.get('no_of_contractor_employee'),
                    "no_of_visitor_angies": request.data.get('no_of_visitor_angies'),
                    "actual_remarks": request.data.get('actual_remarks')
                },
                "no_of_people_not_participated_in_drill": {
                    "no_of_kpi_employee": request.data.get('not_participated_kpi'),
                    "no_of_contractor_employee": request.data.get('not_participated_contractor'),
                    "no_of_visitor_angies": request.data.get('not_participated_visitor'),
                    "not_participated_remarks": request.data.get('not_participated_remarks')
                }
            }


            # Handle location
            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            # ✅ Process drill_details with optional image upload
            fields = [
                "team_leader_incident_controller",
                "performance",
                "traffic_or_evacuation",
                "ambulance_first_aid_ppe_rescue"
            ]
            drill_details = {}
            for field in fields:
                value = request.data.get(field)
                image = request.FILES.get(f"{field}_image")
                image_path = None

                if image:
                    file_name = default_storage.save(f"mock_drills/{image.name}", image)
                    image_path = default_storage.url(file_name)

                drill_details[field] = {
                    "value": value,
                    "image": image_path
                }

            team_members = []
            index = 0
            while True:
                name = request.data.get(f'team_member_name_{index}')
                image = request.FILES.get(f'team_member_image_{index}')

                if not name and not image:
                    break

                image_path = None
                if image:
                    file_name = default_storage.save(f"mock_drills/team_members/{image.name}", image)
                    image_path = default_storage.url(file_name)

                member = {
                    "name": name,
                    "image": image_path
                }
                team_members.append(member)
                index += 1

            # ✅ Create the report
            report = MockDrillReport.objects.create(
                user=user,
                site_plant_name=site_plant_name,
                location=location_instance,
                emergncy_scenario_mock_drill=emergncy_scenario_mock_drill,
                type_of_mock_drill=type_of_mock_drill,
                mock_drill_date=mock_drill_date,
                mock_drill_time=mock_drill_time,
                completed_time=completed_time,
                overall_time=overall_time,
                
                drill_details=drill_details,
                team_members=team_members,
                
                table_top_records=table_top_records,
                description_of_control=description_of_control,
                head_count_at_assembly_point=head_count_at_assembly_point,
                rating_of_emergency_team_members=rating_of_emergency_team_members,
                overall_rating=overall_rating,
                observation=observation,
                recommendations=recommendations
            )

            serializer = MockDrillReportSerializer(report, context={'request': request})
            return Response({"status": True, "message": "Mock drill report created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

        

class GetMockDrillReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MockDrillReportSerializer

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class SafetyTrainingAttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingAttendanceSerializer
    queryset = SafetyTrainingAttendance.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            location_id = data.get('location')
            location_instance = None

            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid location ID",
                        "data": []
                    })

            attendance = SafetyTrainingAttendance.objects.create(
                site_name=data.get('site_name'),
                training_topic=data.get('training_topic'),
                remarks=data.get('remarks'),
                location=location_instance,
                date=data.get('date'),
                faculty_name=data.get('trainer_name'),
                faculty_signature=data.get('trainer_signature'),
                file_upload=data.get('file_upload')
            )

            serializer = TrainingAttendanceSerializer(attendance)
            return Response({
                "status": True,
                "message": "Training attendance created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })


class GetTrainingAttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingAttendanceSerializer
    queryset = SafetyTrainingAttendance.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class MinutesSafetyTrainingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MinutesSafetyTrainingSerializer
    queryset = MinutesSafetyTraining.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            location_id = request.data.get('location')
            site_name = request.data.get('site_name')
            time = request.data.get('time')
            mom_recorded_by = request.data.get('mom_recorded_by')
            mom_issue_date = request.data.get('mom_issue_date')
            chairman_name = request.data.get('chairman_name')
            hse_performance_data = request.data.get('hse_performance_data', [])
            hse_performance_data_json = json.loads(hse_performance_data)
            incident_investigation = request.data.get('incident_investigation', [])
            incident_investigation_json = json.loads(incident_investigation)
            safety_training = request.data.get('safety_training', [])
            safety_training_json = json.loads(safety_training)
            internal_audit = request.data.get('internal_audit', [])
            internal_audit_json = json.loads(internal_audit)
            mock_drill = request.data.get('mock_drill', [])
            mock_drill_json = json.loads(mock_drill)
            procedure_checklist_update = request.data.get('procedure_checklist_update', [])
            procedure_checklist_update_json = json.loads(procedure_checklist_update)
            review_last_meeting = request.data.get('review_last_meeting', [])
            review_last_meeting_json = json.loads(review_last_meeting)
            new_points_discussed = request.data.get('new_points_discussed', [])
            new_points_discussed_json = json.loads(new_points_discussed)
            minutes_prepared_by = request.data.get('minutes_prepared_by')
            signature_prepared_by = request.data.get('signature_prepared_by', [])
            signature_chairman = request.data.get('signature_chairman', [])

            location_ins = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid location ID",
                        "data": []
                    })
            
            safety_training_create = MinutesSafetyTraining.objects.create(
                user=user,
                location=location_instance,
                site_name=site_name,
                time=time,
                mom_recorded_by=mom_recorded_by,
                mom_issue_date=mom_issue_date,
                chairman_name=chairman_name,
                hse_performance_data=hse_performance_data_json,
                incident_investigation=incident_investigation_json,
                safety_training=safety_training_json,
                internal_audit=internal_audit_json,
                mock_drill=mock_drill_json,
                procedure_checklist_update=procedure_checklist_update_json,
                review_last_meeting=review_last_meeting_json,
                new_points_discussed=new_points_discussed_json,
                minutes_prepared_by=minutes_prepared_by,
                signature_prepared_by=signature_prepared_by,
                signature_chairman=signature_chairman
            )

            serializer = MinutesSafetyTrainingSerializer(safety_training_create)
            return Response({
                "status": True,
                "message": "Minutes of safety training created successfully",
                "data": serializer.data
            })
        
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })
        
class GetMinutesSafetyTrainingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MinutesSafetyTrainingSerializer
    queryset = MinutesSafetyTraining.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class InternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InternalAuditReportSerializer
    queryset = InternalAuditReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            location_id = data.get('location')
            location_instance = None

            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid location ID",
                        "data": []
                    })
            
            report = InternalAuditReport.objects.create(
                site_name=data.get('site_name'),
                location=location_instance,
                date=data.get('date'),
                observer_details=data.get('observer_details'),
                observer_name=data.get('observer_name'),
                observer_sign=data.get('observer_sign'),
                auditee_name=data.get('auditee_name'),
                auditee_sign=data.get('auditee_sign'),
                agreed_completion_date=data.get('agreed_completion_date'),
            )

            serializer = InternalAuditReportSerializer(report)
            return Response({
                "status": True,
                "message": "Internal audit report created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })


class GetInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InternalAuditReportSerializer
    queryset = InternalAuditReport.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "internal audit list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class CorrectionInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CorrectionInternalAuditReportSerializer
    queryset = CorrectionInternalAuditReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            audit_report = data.get('audit_report')
            audit_report_ins = None

            if audit_report:
                try:
                    audit_report_ins = InternalAuditReport.objects.get(id=audit_report)
                except InternalAuditReport.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid InternalAuditReport ID",
                        "data": []
                    })
            
            report = CorrectionInternalAuditReport.objects.create(
                root_cause=data.get('root_cause'),
                audit_report=audit_report_ins,
                corrective_action=data.get('corrective_action'),
                correction_auditee_name=data.get('correction_auditee_name'),
                correction_auditee_sign=data.get('correction_auditee_sign'),
                correction_auditee_date=data.get('correction_auditee_date')
            )
            audit_report_ins.is_correction_done = True
            audit_report_ins.save()

            serializer = CorrectionInternalAuditReportSerializer(report)
            return Response({
                "status": True,
                "message": "Correction internal audit report created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })
        
    
class GetCorrectionInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CorrectionInternalAuditReportSerializer
    queryset = CorrectionInternalAuditReport.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            audit_report = self.kwargs.get('audit_report')
            queryset = self.filter_queryset(self.get_queryset())
            if audit_report:
                queryset = queryset.filter(audit_report=audit_report)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "correction list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class VerificationInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VerificationInternalAuditReportSerializer
    queryset = VerificationInternalAuditReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            audit_report = data.get('audit_report')
            audit_report_ins = None

            if audit_report:
                try:
                    audit_report_ins = InternalAuditReport.objects.get(id=audit_report)
                except InternalAuditReport.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid InternalAuditReport ID",
                        "data": []
                    })
            
            report = VerificationInternalAuditReport.objects.create(
                audit_report=audit_report_ins,
                verification_auditor_name=data.get('verification_auditor_name'),
                verification_auditor_sign=data.get('verification_auditor_sign'),
                verification_auditor_date=data.get('verification_auditor_date')
            )
            audit_report_ins.is_verification_done = True
            audit_report_ins.save()

            serializer = VerificationInternalAuditReportSerializer(report)
            return Response({
                "status": True,
                "message": "verification internal audit report created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })


class GetVerificationInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VerificationInternalAuditReportSerializer
    queryset = VerificationInternalAuditReport.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            audit_report = self.kwargs.get('audit_report')
            queryset = self.filter_queryset(self.get_queryset())
            if audit_report:
                queryset = queryset.filter(audit_report=audit_report)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Verification list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ClosureInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClosureInternalAuditReportSerializer
    queryset = ClosureInternalAuditReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            audit_report = data.get('audit_report')
            audit_report_ins = None

            if audit_report:
                try:
                    audit_report_ins = InternalAuditReport.objects.get(id=audit_report)
                except InternalAuditReport.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid InternalAuditReport ID",
                        "data": []
                    })
            
            report = ClosureInternalAuditReport.objects.create(
                audit_report=audit_report_ins,
                report_closure=data.get('report_closure'),
                siteincharge_name=data.get('siteincharge_name'),
                siteincharge_sign=data.get('siteincharge_sign'),
                siteincharge_date=data.get('siteincharge_date')
            )
            audit_report_ins.is_closure_done = True
            audit_report_ins.save()

            serializer = ClosureInternalAuditReportSerializer(report)
            return Response({
                "status": True,
                "message": "closure internal audit report created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })


class GetClosureInternalAuditReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClosureInternalAuditReportSerializer
    queryset = ClosureInternalAuditReport.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            audit_report = self.kwargs.get('audit_report')
            queryset = self.filter_queryset(self.get_queryset())
            if audit_report:
                queryset = queryset.filter(audit_report=audit_report)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Closure list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


from rest_framework.parsers import MultiPartParser, FormParser
class CreateInductionTrainingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InductionTrainingSerializer
    queryset = InductionTraining.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Induction training created successfully",
                    "data": serializer.data
                })
            return Response({
                "status": False,
                "message": serializer.errors,
                "data": []
            })
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})

            
         
class ToollboxTalkAttendenceCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ToollboxTalkAttendenceSerializer
    queryset = ToollboxTalkAttendence.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            site_name= request.data.get('site_name')
            location_id=request.data.get('location')
            date=request.data.get('date')
            time=request.data.get('time')
            tbt_against_permit_no=request.data.get('tbt_against_permit_no')
            permit_date=request.data.get('permit_date')
            tbt_conducted_by_name=request.data.get('tbt_conducted_by_name')
            tbt_conducted_by_signature=request.FILES.get('tbt_conducted_by_signature')
            name_of_contractor=request.data.get('name_of_contractor')
            job_activity_in_detail=request.data.get('job_activity_in_detail')
            use_of_ppes_topic_discussed=request.data.get('use_of_ppes_topic_discussed')
            use_of_tools_topic_discussed=request.data.get('use_of_tools_topic_discussed')
            hazard_at_work_place_topic_discussed=request.data.get('hazard_at_work_place_topic_discussed')
            use_of_action_in_an_emergency_topic_discussed=request.data.get('use_of_action_in_an_emergency_topic_discussed')
            use_of_health_status_topic_discussed=request.data.get('use_of_health_status_topic_discussed')
            use_of_others_topic_discussed=request.data.get('use_of_others_topic_discussed')
            participant_upload_attachments=request.FILES.get('participant_upload_attachments')
            remarks=request.data.get('remarks')

            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            attendance = ToollboxTalkAttendence.objects.create(
                site_name=site_name,
                location=location_instance,
                date=date,
                time=time,
                tbt_against_permit_no=tbt_against_permit_no,
                permit_date=permit_date,
                tbt_conducted_by_name=tbt_conducted_by_name,
                tbt_conducted_by_signature=tbt_conducted_by_signature,
                name_of_contractor=name_of_contractor,
                job_activity_in_detail=job_activity_in_detail,
                use_of_ppes_topic_discussed=use_of_ppes_topic_discussed,
                use_of_tools_topic_discussed=use_of_tools_topic_discussed,
                hazard_at_work_place_topic_discussed=hazard_at_work_place_topic_discussed,
                use_of_action_in_an_emergency_topic_discussed=use_of_action_in_an_emergency_topic_discussed,
                use_of_health_status_topic_discussed=use_of_health_status_topic_discussed,
                use_of_others_topic_discussed=use_of_others_topic_discussed,
                participant_upload_attachments=participant_upload_attachments,
                remarks=remarks
            )

            serializer = ToollboxTalkAttendenceSerializer(attendance, context={'request': request})
            return Response({
                "status": True,
                "message": "Toolbox talk attendance created successfully",
                "data": serializer.data
            })


        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })



class GetInductionTrainingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InductionTrainingSerializer
    queryset = InductionTraining.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})    


class FireExtinguisherInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FireExtinguisherInspectionJSONFormatSerializer
    queryset = FireExtinguisherInspectionJSONFormat.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            site_name = request.data.get('site_name')
            location_id = request.data.get('location')
            date_of_inspection = request.data.get('date_of_inspection')
            checked_by_name = request.data.get('checked_by_name')
            signature = request.FILES.get('signature')
            fire_extinguisher_details = request.data.get('fire_extinguisher_details', [])

            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            fire_extinguisher_details = json.loads(fire_extinguisher_details)
            fire_extinguisher_inspection = FireExtinguisherInspectionJSONFormat.objects.create(
                site_name=site_name,
                location=location_instance,
                date_of_inspection=date_of_inspection,
                checked_by_name=checked_by_name,
                signature=signature,
                fire_extinguisher_details=fire_extinguisher_details
            )

            serializer = FireExtinguisherInspectionJSONFormatSerializer(fire_extinguisher_inspection, context={'request': request})
            return Response({
                "status": True,
                "message": "Fire extinguisher inspection created successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})
        
class GetFireExtinguisherInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FireExtinguisherInspectionJSONFormatSerializer
    queryset = FireExtinguisherInspectionJSONFormat.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})   
  
class ToollboxTalkAttendenceGetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ToollboxTalkAttendenceSerializer
    queryset = ToollboxTalkAttendence.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            attendance = ToollboxTalkAttendence.objects.all().order_by('-id')
            serializer = ToollboxTalkAttendenceSerializer(attendance, context={'request': request}, many=True)
            data = serializer.data
            return Response({"status": True,"message": "Toolbox talk attendance fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})
        
        
class LocationIdwiseGetToollboxTalkAttendenceGetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ToollboxTalkAttendenceSerializer
    queryset = ToollboxTalkAttendence.objects.all()
    
    def list(self,request,*args,**kwargs):
        try:
            location_id = kwargs.get('location_id')
            if not location_id:
                return Response({"status": False, "message": "Location Id is required", "data": []})
            attendance = ToollboxTalkAttendence.objects.filter(location_id=location_id).order_by('-id')
            serializer = ToollboxTalkAttendenceSerializer(attendance, context={'request': request}, many=True)
            data = serializer.data
            return Response({"status": True,"message": "Toolbox talk attendance fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})
            
            
            
class FirstAidRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            site_name=request.data.get('site_name')
            location_id=request.data.get('location')
            date=request.data.get('date')
            first_aid_name = request.data.get('first_aid_name')
            designation = request.data.get('designation')
            employee_of = request.data.get('employee_of')
            description = request.data.get('description')

            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})
                
            first_aid_record = FirstAidRecord.objects.create(
                site_name=site_name,
                location=location_instance,
                date=date,
                first_aid_name=first_aid_name,
                designation=designation,
                employee_of=employee_of,
                description=description
            )
            serializer = FirstAidRecordSerializer(first_aid_record, context={'request': request})
            data = serializer.data
            return Response({
                "status": True,
                "message": "First Aid Record created successfully",
                "data": data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []

            })            
        
    def list(self, request, *args, **kwargs):
        try:
            inspections = self.get_queryset()
            serializer = self.get_serializer(inspections, many=True)
            return Response({
                "status": True,
                "message": "Fire extinguisher inspections fetched successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })    

           
            
            
class GetListFirstrecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            first_aid_record = FirstAidRecord.objects.all().order_by('-id')
            serializer = FirstAidRecordSerializer(first_aid_record, context={'request': request}, many=True)
            data = serializer.data
            return Response({"status": True,"message": "First Aid Record fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})
        
        
class LocationIdwiseGetListFirstrecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    
    def list(self,request,*args,**kwargs):
        try:
            location_id = kwargs.get('location_id')
            if not location_id:
                return Response({"status": False, "message": "Location Id is required", "data": []})
            first_aid_record = FirstAidRecord.objects.filter(location_id=location_id).order_by('-id')
            serializer = FirstAidRecordSerializer(first_aid_record, context={'request': request}, many=True)
            data = serializer.data
            return Response({"status": True,"message": "First Aid Record fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data": []})
        

class HarnessInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HarnessInspectionSerializer
    queryset = HarnessInspection.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "status": True,
                "message": "Harness inspection report created successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })

class GetHarnessInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HarnessInspectionSerializer
    queryset = HarnessInspection.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})   


class ExcavationPermitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExcavationPermitSerializer
    queryset = ExcavationPermit.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            def to_bool(value):
                return str(value).lower() in ['true', '1', 'yes']
            site_name = request.data.get('site_name')
            location_id = request.data.get('location')
            permit_number = request.data.get('permit_number')
            date = request.data.get('date')
            description_of_work = request.data.get('description_of_work')
            location_area_work = request.data.get('location_area_work')
            length = request.data.get('length')
            breadth = request.data.get('breadth')
            start_work_date = request.data.get('start_work_date')
            depth = request.data.get('depth')
            start_work_time = request.data.get('start_work_time')
            duration_work_day = request.data.get('duration_work_day')
            duration_work_hors = request.data.get('duration_work_hors')
            purpose_of_excavation = request.data.get('purpose_of_excavation')
            electrical_cable_description = request.data.get('electrical_cable_description')
            electrical_cable_name = request.data.get('electrical_cable_name')
            electrical_cable_date = request.data.get('electrical_cable_date')
            sign_upload = request.FILES.get('sign_upload', [])
            water_gas_description = request.data.get('water_gas_description')
            water_gas_name = request.data.get('water_gas_name')
            water_gas_date = request.data.get('water_gas_date')
            water_sign_upload = request.FILES.get('water_sign_upload', [])
            telephone_description = request.data.get('telephone_description')
            telephone_name = request.data.get('telephone_name')
            telephone_date = request.data.get('telephone_date')
            telephone_sign_upload = request.FILES.get('telephone_sign_upload', [])
            road_barricading = to_bool(request.data.get('road_barricading'))
            warning_sign = to_bool(request.data.get('warning_sign'))
            barricading_excavated_area = to_bool(request.data.get('barricading_excavated_area'))
            shoring_carried = to_bool(request.data.get('shoring_carried'))
            any_other_precaution = request.data.get('any_other_precaution')
            name_acceptor = request.data.get('name_acceptor')
            acceptor_sign_upload = request.FILES.get('acceptor_sign_upload', [])
            remarks = request.data.get('remarks')
            check_by_name = request.data.get('check_by_name')
            check_by_sign = request.FILES.get('check_by_sign', [])

            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})

            excavation_permit = ExcavationPermit.objects.create(
                site_name=site_name,
                location=location_instance,
                permit_number=permit_number,
                date=date,
                description_of_work=description_of_work,
                location_area_work=location_area_work,
                length=length,
                breadth=breadth,
                start_work_date=start_work_date,
                depth=depth,
                start_work_time=start_work_time,
                duration_work_day=duration_work_day,
                duration_work_hors=duration_work_hors,
                purpose_of_excavation=purpose_of_excavation,
                electrical_cable_description=electrical_cable_description,
                electrical_cable_name=electrical_cable_name,
                electrical_cable_date=electrical_cable_date,
                sign_upload=sign_upload,
                water_gas_description=water_gas_description,
                water_gas_name=water_gas_name,
                water_gas_date=water_gas_date,
                water_sign_upload=water_sign_upload,
                telephone_description=telephone_description,
                telephone_name=telephone_name,
                telephone_date=telephone_date,
                telephone_sign_upload=telephone_sign_upload,
                road_barricading=road_barricading,
                warning_sign=warning_sign,
                barricading_excavated_area=barricading_excavated_area,
                shoring_carried=shoring_carried,
                any_other_precaution=any_other_precaution,
                name_acceptor=name_acceptor,
                acceptor_sign_upload=acceptor_sign_upload,
                remarks=remarks,
                check_by_name=check_by_name,
                check_by_sign=check_by_sign
            )

            serializer = ExcavationPermitSerializer(excavation_permit, context={'request': request})
            return Response({
                "status": True,
                "message": "Excavation permit created successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })
        

class GetExcavationPermitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExcavationPermitSerializer
    queryset = ExcavationPermit.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})   
        
class LadderInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LadderInspectionSerializer
    queryset = LadderInspection.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "status": True,
                "message": "Ladder inspection report created successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })

class GetLadderInspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LadderInspectionSerializer
    queryset = LadderInspection.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})       
        

class SuggestionSchemeReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SuggestionSchemeReportSerializer
    queryset = SuggestionSchemeReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            location = request.data.get('location')

            if location:
                try:
                    location_instance = LandBankLocation.objects.get(id=location)
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location ID", "data": []})
            report = SuggestionSchemeReport.objects.create(
                site=data.get('site'),
                location=location_instance,
                date=data.get('date'),
                name=data.get('name'),
                designation=data.get('designation'),
                suggestion_description=data.get('suggestion_description'),
                benefits_upon_implementation=data.get('benefits_upon_implementation'),
                evaluated_by=data.get('evaluated_by'),
                evaluator_name=data.get('evaluator_name'),
                evaluator_designation=data.get('evaluator_designation'),
                evaluation_remarks=data.get('evaluation_remarks'),
                evaluator_signature=data.get('evaluator_signature'),
            )

            serializer = SuggestionSchemeReportSerializer(report)
            return Response({
                "status": True,
                "message": "Suggestion scheme report created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })

class GetSuggestionSchemeReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SuggestionSchemeReportSerializer
    queryset = SuggestionSchemeReport.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class LotoRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LotoAppliedInfoSerializer
    queryset = LotoAppliedInfo.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            site_name = request.data.get('site_name')
            location_id = request.data.get('location')
            applied_datetime = request.data.get('applied_datetime')
            applied_lock_tag_number = request.data.get('applied_lock_tag_number')
            applied_permit_number = request.data.get('applied_permit_number')
            applied_by_name = request.data.get('applied_by_name')
            applied_by_signature = request.FILES.get('applied_by_signature')
            applied_approved_by_name = request.data.get('applied_approved_by_name')
            applied_approved_by_signature = request.FILES.get('applied_approved_by_signature')

            location_instance = None
            if location_id:
                try:
                    location_instance = LandBankLocation.objects.get(id=location_id)
                except LandBankLocation.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid location ID",
                        "data": []
                    })

            loto_instance = LotoAppliedInfo.objects.create(
                site_name=site_name,
                location=location_instance,
                applied_datetime=applied_datetime,
                applied_lock_tag_number=applied_lock_tag_number,
                applied_permit_number=applied_permit_number,
                applied_by_name=applied_by_name,
                applied_by_signature=applied_by_signature,
                applied_approved_by_name=applied_approved_by_name,
                applied_approved_by_signature=applied_approved_by_signature,
            )

            serializer = LotoAppliedInfoSerializer(loto_instance)
            return Response({
                "status": True,
                "message": "LOTO register created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })


class GetLotoRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LotoRegisterSerializer
    queryset = LotoRegister.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})   
        
    
class LotoClearedInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LotoRegisterSerializer
    queryset = LotoRegister.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            loto_id = request.data.get('loto_id')
            removed_datetime = request.data.get('removed_datetime')
            removed_lock_tag_number = request.data.get('removed_lock_tag_number')
            removed_permit_number = request.data.get('removed_permit_number')
            removed_by_name = request.data.get('removed_by_name')
            removed_by_signature = request.FILES.get('removed_by_signature')
            removed_site_incharge_name = request.data.get('removed_site_incharge_name')
            removed_approved_by_signature = request.FILES.get('removed_approved_by_signature')

            if loto_id:
                try:
                    loto_instance = LotoAppliedInfo.objects.get(id=loto_id)
                except LotoAppliedInfo.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Invalid LOTO ID",
                        "data": []
                    })

            cleared_info = LotoRegister.objects.create(
                applied_info=loto_instance,
                removed_datetime=removed_datetime,
                removed_lock_tag_number=removed_lock_tag_number,
                removed_permit_number=removed_permit_number,
                removed_by_name=removed_by_name,
                removed_by_signature=removed_by_signature,
                removed_site_incharge_name=removed_site_incharge_name,
                removed_approved_by_signature=removed_approved_by_signature,
            )

            serializer = LotoRegisterSerializer(cleared_info)
            return Response({
                "status": True,
                "message": "LOTO clearance recorded successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })
        
class GetLotoClearedInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LotoRegisterSerializer
    queryset = LotoRegister.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs.get('location_id')
            queryset = self.filter_queryset(self.get_queryset())
            if location_id:
                queryset = queryset.filter(location=location_id)
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Permit to work list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})