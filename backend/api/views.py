from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import ApprovalActionPermission
from .permissions import InspectionReportPermission
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})
    
from .models import (
    PBS,
    Office,
    Substation,
    EquipmentType,
    Equipment,
    InspectionType,
    TestType,
    InspectionReport,
    ChecklistTemplate,
    ChecklistItem,
    EquipmentPosition,
    InspectionPhase,
    TestResult,
    ChecklistResponse,
    Attachment,
    Approval,
    MaintenanceAction,
    AuditLog,
)

from .serializers import (
    PBSSerializer,
    OfficeSerializer,
    SubstationSerializer,
    EquipmentTypeSerializer,
    EquipmentSerializer,
    InspectionTypeSerializer,
    TestTypeSerializer,
    InspectionReportSerializer,
    ChecklistTemplateSerializer,
    ChecklistItemSerializer,
    EquipmentPositionSerializer,
    InspectionPhaseSerializer,
    TestResultSerializer,
    ChecklistResponseSerializer,
    AttachmentSerializer,
    ApprovalSerializer,
    MaintenanceActionSerializer,
    AuditLogSerializer,
)


class PBSViewSet(viewsets.ModelViewSet):
    queryset = PBS.objects.all()
    serializer_class = PBSSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class SubstationViewSet(viewsets.ModelViewSet):
    queryset = Substation.objects.all()
    serializer_class = SubstationSerializer


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class InspectionTypeViewSet(viewsets.ModelViewSet):
    queryset = InspectionType.objects.all()
    serializer_class = InspectionTypeSerializer


class TestTypeViewSet(viewsets.ModelViewSet):
    queryset = TestType.objects.all()
    serializer_class = TestTypeSerializer


class InspectionReportViewSet(viewsets.ModelViewSet):

    queryset = InspectionReport.objects.all()

    serializer_class = InspectionReportSerializer

    permission_classes = [InspectionReportPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def change_status(self, request, pk=None):
        report = self.get_object()

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {
                    "detail": "Status is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            report.change_status(
                new_status,
                acted_by=request.user,
                comment=request.data.get("comment", "")
    )
        except ValueError as e:
            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": report.id,
                "report_no": report.report_no,
                "status": report.status,
            },
            status=status.HTTP_200_OK,
        )

    filterset_fields = [
        "status",
        "inspection_type",
        "substation",
        "created_by",
    ]

    search_fields = [
        "report_no",
        "general_comment",
    ]

    ordering_fields = [
        "inspection_date",
        "created_at",
        "updated_at",
        "report_no",
    ]

    ordering = [
        "-inspection_date",
        "-id",
    ]


class ChecklistTemplateViewSet(viewsets.ModelViewSet):
    queryset = ChecklistTemplate.objects.all()
    serializer_class = ChecklistTemplateSerializer


class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer


class EquipmentPositionViewSet(viewsets.ModelViewSet):
    queryset = EquipmentPosition.objects.all()
    serializer_class = EquipmentPositionSerializer


class InspectionPhaseViewSet(viewsets.ModelViewSet):
    queryset = InspectionPhase.objects.all()
    serializer_class = InspectionPhaseSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer


class ChecklistResponseViewSet(viewsets.ModelViewSet):
    queryset = ChecklistResponse.objects.all()
    serializer_class = ChecklistResponseSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        queryset = Attachment.objects.all()

        report_id = self.request.query_params.get("report")

        if report_id:
            queryset = queryset.filter(report_id=report_id)

        return queryset

class MaintenanceActionViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceAction.objects.all()
    serializer_class = MaintenanceActionSerializer

    filterset_fields = [
        "priority",
        "status",
        "report",
        "equipment",
        "assigned_to",
    ]

    search_fields = [
        "action_required",
        "remarks",
    ]

    ordering_fields = [
        "priority",
        "status",
        "due_date",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at",
    ]

class ApprovalViewSet(viewsets.ModelViewSet):

    queryset = Approval.objects.all()

    serializer_class = ApprovalSerializer

    permission_classes = [ApprovalActionPermission]

    def get_queryset(self):
        queryset = Approval.objects.all()

        report_id = self.request.query_params.get("report")

        if report_id:
            queryset = queryset.filter(report_id=report_id)

        return queryset

    def update(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "Approval records cannot be modified."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "Approval records cannot be deleted."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    def create(self, request, *args, **kwargs):
        action = request.data.get("action")

        if request.user.is_superuser:
            allowed_actions = {
                "SUBMITTED",
                "APPROVED",
                "REJECTED",
                "RETURNED",
            }
        else:
            user_roles = set(
                request.user.groups.values_list("name", flat=True)
            )

            allowed_actions = set()

            if "ADMIN" in user_roles:
                allowed_actions.update(
                    {"SUBMITTED", "APPROVED", "REJECTED", "RETURNED"}
                )

            if "REVIEWER" in user_roles:
                allowed_actions.update(
                    {"RETURNED", "REJECTED"}
                )

            if "APPROVER" in user_roles:
                allowed_actions.update(
                    {"APPROVED", "REJECTED"}
                )

        if action not in allowed_actions:
            return Response(
                {
                    "detail": (
                        f"You are not allowed to perform "
                        f"the '{action}' action."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(acted_by=request.user)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    filterset_fields = [
        "action",
        "report",
        "performed_by",
    ]

    search_fields = [
        "comment",
        "old_status",
        "new_status",
    ]

    ordering_fields = [
        "created_at",
        "action",
        "old_status",
        "new_status",
    ]

    ordering = [
        "-created_at",
    ]