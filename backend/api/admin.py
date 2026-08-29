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


# =========================================================
# PBS
# =========================================================

@admin.register(PBS)
class PBSAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "zone_office",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "zone_office",
    )

    list_filter = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# SUBSTATION
# =========================================================

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
        "pbs__code",
    )

    list_filter = (
        "pbs",
        "voltage_level",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# EQUIPMENT TYPE
# =========================================================

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# EQUIPMENT POSITION INLINE
# =========================================================

class EquipmentPositionInline(admin.TabularInline):
    model = EquipmentPosition
    extra = 1

    fields = (
        "position_code",
        "position_name",
        "sequence",
        "is_active",
    )


# =========================================================
# EQUIPMENT
# =========================================================

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
        "model",
        "substation__name",
    )

    list_filter = (
        "equipment_type",
        "substation",
        "status",
    )

    inlines = (
        EquipmentPositionInline,
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# INSPECTION TYPE
# =========================================================

@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# INSPECTION PHASE INLINE
# =========================================================

class InspectionPhaseInline(admin.TabularInline):
    model = InspectionPhase
    extra = 0

    fields = (
        "equipment",
        "phase",
    )


# =========================================================
# CHECKLIST RESPONSE INLINE
# =========================================================

class ChecklistResponseInline(admin.TabularInline):
    model = ChecklistResponse
    extra = 0

    fields = (
        "equipment",
        "checklist_item",
        "phase",
        "position",
        "value_text",
        "value_number",
        "value_boolean",
        "value_choice",
        "remarks",
    )


# =========================================================
# INSPECTION REPORT
# =========================================================

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
        "inspection_type__name",
        "created_by__username",
    )

    list_filter = (
        "inspection_type",
        "status",
        "inspection_date",
        "substation",
    )

    date_hierarchy = "inspection_date"

    inlines = (
        InspectionPhaseInline,
        ChecklistResponseInline,
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# CHECKLIST ITEM INLINE
# =========================================================

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1

    fields = (
        "item_code",
        "item_label",
        "section",
        "response_type",
        "sequence",
        "required",
        "help_text",
    )


# =========================================================
# CHECKLIST TEMPLATE
# =========================================================

@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "section_name",
        "inspection_type",
        "equipment_type",
        "version",
        "is_active",
    )

    search_fields = (
        "section_name",
        "version",
        "inspection_type__name",
        "equipment_type__name",
    )

    list_filter = (
        "inspection_type",
        "equipment_type",
        "is_active",
    )

    inlines = (
        ChecklistItemInline,
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# CHECKLIST ITEM
# =========================================================

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

    search_fields = (
        "item_code",
        "item_label",
        "template__section_name",
    )

    list_filter = (
        "response_type",
        "required",
        "template",
    )

    ordering = (
        "template",
        "sequence",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# EQUIPMENT POSITION
# =========================================================

@admin.register(EquipmentPosition)
class EquipmentPositionAdmin(admin.ModelAdmin):
    list_display = (
        "position_code",
        "position_name",
        "equipment",
        "sequence",
        "is_active",
    )

    search_fields = (
        "position_code",
        "position_name",
        "equipment__name",
        "equipment__equipment_code",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "equipment",
        "sequence",
    )

    readonly_fields = (
        "created_at",
    )


# =========================================================
# INSPECTION PHASE
# =========================================================

@admin.register(InspectionPhase)
class InspectionPhaseAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "equipment",
        "phase",
    )

    search_fields = (
        "report__report_no",
        "equipment__name",
        "equipment__equipment_code",
    )

    list_filter = (
        "phase",
    )


# =========================================================
# CHECKLIST RESPONSE
# =========================================================

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
        "equipment__equipment_code",
        "checklist_item__item_code",
        "checklist_item__item_label",
    )

    list_filter = (
        "phase",
        "equipment",
        "report",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )