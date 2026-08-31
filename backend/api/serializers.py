from rest_framework import serializers

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
)


class PBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PBS
        fields = "__all__"


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"


class SubstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substation
        fields = "__all__"


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        fields = "__all__"


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = "__all__"


class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = "__all__"


class ChecklistTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistTemplate
        fields = "__all__"


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = "__all__"


class EquipmentPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentPosition
        fields = "__all__"


class InspectionPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionPhase
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = "__all__"


class ChecklistResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistResponse
        fields = "__all__"