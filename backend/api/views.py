from rest_framework import viewsets

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