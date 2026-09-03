from rest_framework.routers import DefaultRouter

from .views import (
    PBSViewSet,
    OfficeViewSet,
    SubstationViewSet,
    EquipmentTypeViewSet,
    EquipmentViewSet,
    InspectionTypeViewSet,
    TestTypeViewSet,
    InspectionReportViewSet,
    ChecklistTemplateViewSet,
    ChecklistItemViewSet,
    EquipmentPositionViewSet,
    InspectionPhaseViewSet,
    TestResultViewSet,
    ChecklistResponseViewSet,
    AttachmentViewSet,
)


router = DefaultRouter()

router.register(r"pbs", PBSViewSet)
router.register(r"offices", OfficeViewSet)
router.register(r"substations", SubstationViewSet)
router.register(r"equipment-types", EquipmentTypeViewSet)
router.register(r"equipment", EquipmentViewSet)
router.register(r"inspection-types", InspectionTypeViewSet)
router.register(r"test-types", TestTypeViewSet)
router.register(r"inspection-reports", InspectionReportViewSet)
router.register(r"checklist-templates", ChecklistTemplateViewSet)
router.register(r"checklist-items", ChecklistItemViewSet)
router.register(r"equipment-positions", EquipmentPositionViewSet)
router.register(r"inspection-phases", InspectionPhaseViewSet)
router.register(r"test-results", TestResultViewSet)
router.register(r"checklist-responses", ChecklistResponseViewSet)
router.register(r"attachments", AttachmentViewSet)


urlpatterns = router.urls