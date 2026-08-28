from django.contrib import admin

from .models import (
    PBS,
    Substation,
    EquipmentType,
    Equipment,
    InspectionType,
    InspectionReport,
    ChecklistTemplate,
    ChecklistItem,
    EquipmentPosition,
    InspectionPhase,
    ChecklistResponse,
)


@admin.register(PBS)
class PBSAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "zone_office",
        "is_active",
        "created_at",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(Substation)
class SubstationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "pbs",
        "voltage_level",
        "capacity_mva",
        "is_active",
    )
    search_fields = (
        "name",
        "code",
        "pbs__name",
    )
    list_filter = (
        "pbs",
        "voltage_level",
        "is_active",
    )


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "equipment_code",
        "equipment_type",
        "substation",
        "manufacturer",
        "status",
    )
    search_fields = (
        "name",
        "equipment_code",
        "serial_no",
        "manufacturer",
    )
    list_filter = (
        "equipment_type",
        "substation",
        "status",
    )


@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_no",
        "substation",
        "inspection_type",
        "inspection_date",
        "status",
        "created_by",
    )
    search_fields = (
        "report_no",
        "substation__name",
        "substation__code",
    )
    list_filter = (
        "inspection_type",
        "status",
        "inspection_date",
    )
    date_hierarchy = "inspection_date"
@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "section_name",
        "inspection_type",
        "equipment_type",
        "version",
        "is_active",
    )

    list_filter = (
        "inspection_type",
        "equipment_type",
        "is_active",
    )

    search_fields = (
        "section_name",
        "version",
    )


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_code",
        "item_label",
        "template",
        "response_type",
        "sequence",
        "required",
    )

    list_filter = (
        "response_type",
        "required",
    )

    search_fields = (
        "item_code",
        "item_label",
    )


@admin.register(EquipmentPosition)
class EquipmentPositionAdmin(admin.ModelAdmin):
    list_display = (
        "position_code",
        "position_name",
        "equipment",
        "sequence",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "position_code",
        "position_name",
        "equipment__name",
    )


@admin.register(InspectionPhase)
class InspectionPhaseAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "equipment",
        "phase",
    )

    list_filter = (
        "phase",
    )


@admin.register(ChecklistResponse)
class ChecklistResponseAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "equipment",
        "checklist_item",
        "phase",
        "position",
        "updated_at",
    )

    search_fields = (
        "report__report_no",
        "equipment__name",
        "checklist_item__item_label",
    )

    list_filter = (
        "phase",
    )
