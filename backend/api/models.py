from django.db import models


class PBS(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pbs"
        ordering = ["name"]
        verbose_name = "PBS"
        verbose_name_plural = "PBS"

    def __str__(self):
        return f"{self.name} ({self.code})"

class Office(models.Model):
    OFFICE_TYPE_CHOICES = [
        ("SADAR", "Sadar Office"),
        ("ZONAL", "Zonal Office"),
        ("SUB_ZONAL", "Sub-Zonal Office"),
    ]

    pbs = models.ForeignKey(
        PBS,
        on_delete=models.PROTECT,
        related_name="offices",
    )

    name = models.CharField(max_length=150)

    code = models.CharField(max_length=50)

    office_type = models.CharField(
        max_length=20,
        choices=OFFICE_TYPE_CHOICES,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        max_length=150,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "office"
        ordering = ["office_type", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["pbs", "code"],
                name="unique_office_code_per_pbs",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Substation(models.Model):
    pbs = models.ForeignKey(
        PBS,
        on_delete=models.PROTECT,
        related_name="substations",
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    capacity_mva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    voltage_level = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    commissioning_date = models.DateField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "substation"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["pbs", "code"],
                name="unique_substation_code_per_pbs",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class EquipmentType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "equipment_type"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Equipment(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("UNDER_MAINTENANCE", "Under Maintenance"),
        ("RETIRED", "Retired"),
    ]

    substation = models.ForeignKey(
        Substation,
        on_delete=models.PROTECT,
        related_name="equipment",
    )

    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="equipment",
    )

    name = models.CharField(max_length=150)
    equipment_code = models.CharField(max_length=100)

    manufacturer = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    model = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    serial_no = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    rating = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    installation_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "equipment"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["substation", "equipment_code"],
                name="unique_equipment_code_per_substation",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.equipment_code})"


class InspectionType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspection_type"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class InspectionReport(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("REJECTED", "Rejected"),
        ("FINAL_APPROVED", "Final Approved"),
        ("CLOSED", "Closed"),
    ]

    report_no = models.CharField(
        max_length=100,
        unique=True,
    )

    substation = models.ForeignKey(
        Substation,
        on_delete=models.PROTECT,
        related_name="inspection_reports",
    )

    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.PROTECT,
        related_name="inspection_reports",
    )

    inspection_date = models.DateField()

    peak_load_mw = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        related_name="created_inspection_reports",
    )

    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    general_comment = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspection_report"
        ordering = ["-inspection_date", "-id"]

    def __str__(self):
        return self.report_no

class ChecklistTemplate(models.Model):
    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.PROTECT,
        related_name="checklist_templates",
    )

    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="checklist_templates",
        blank=True,
        null=True,
    )

    section_name = models.CharField(max_length=150)

    version = models.CharField(
        max_length=30,
        default="1.0",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "checklist_template"
        ordering = ["section_name", "version"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "inspection_type",
                    "equipment_type",
                    "section_name",
                    "version",
                ],
                name="unique_checklist_template_version",
            )
        ]

    def __str__(self):
        equipment = (
            self.equipment_type.name
            if self.equipment_type
            else "General"
        )

        return f"{self.section_name} - {equipment} v{self.version}"


class ChecklistItem(models.Model):
    RESPONSE_TYPE_CHOICES = [
        ("YES_NO", "Yes / No"),
        ("OK_NOT_OK", "OK / Not OK"),
        ("SATISFACTORY", "Satisfactory"),
        ("TEXT", "Text"),
        ("NUMBER", "Number"),
        ("DECIMAL", "Decimal"),
        ("DATE", "Date"),
        ("CHOICE", "Choice"),
    ]

    template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.CASCADE,
        related_name="items",
    )

    item_code = models.CharField(max_length=50)

    item_label = models.CharField(max_length=500)

    section = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    response_type = models.CharField(
        max_length=30,
        choices=RESPONSE_TYPE_CHOICES,
        default="TEXT",
    )

    sequence = models.PositiveIntegerField(default=1)

    required = models.BooleanField(default=False)

    help_text = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "checklist_item"
        ordering = ["sequence", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["template", "item_code"],
                name="unique_item_code_per_template",
            )
        ]

    def __str__(self):
        return f"{self.item_code} - {self.item_label}"


class EquipmentPosition(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="positions",
    )

    position_code = models.CharField(max_length=50)

    position_name = models.CharField(max_length=150)

    sequence = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "equipment_position"
        ordering = ["sequence", "position_code"]
        constraints = [
            models.UniqueConstraint(
                fields=["equipment", "position_code"],
                name="unique_position_per_equipment",
            )
        ]

    def __str__(self):
        return f"{self.equipment.name} - {self.position_code}"


class InspectionPhase(models.Model):
    PHASE_CHOICES = [
        ("R", "R Phase"),
        ("Y", "Y Phase"),
        ("B", "B Phase"),
        ("A", "A Phase"),
        ("B2", "B Phase"),
        ("C", "C Phase"),
    ]

    report = models.ForeignKey(
        InspectionReport,
        on_delete=models.CASCADE,
        related_name="phases",
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="inspection_phases",
    )

    phase = models.CharField(
        max_length=10,
        choices=PHASE_CHOICES,
    )

    class Meta:
        db_table = "inspection_phase"
        constraints = [
            models.UniqueConstraint(
                fields=["report", "equipment", "phase"],
                name="unique_phase_per_report_equipment",
            )
        ]

    def __str__(self):
        return f"{self.equipment.name} - {self.phase}"


class TestResult(models.Model):
    RESULT_STATUS_CHOICES = [
        ("PASS", "Pass"),
        ("FAIL", "Fail"),
        ("SATISFACTORY", "Satisfactory"),
        ("UNSATISFACTORY", "Unsatisfactory"),
        ("NOT_TESTED", "Not Tested"),
    ]

    report = models.ForeignKey(
        InspectionReport,
        on_delete=models.CASCADE,
        related_name="test_results",
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name="test_results",
    )

    test_name = models.CharField(
        max_length=200,
    )

    phase = models.ForeignKey(
        InspectionPhase,
        on_delete=models.CASCADE,
        related_name="test_results",
        blank=True,
        null=True,
    )

    position = models.ForeignKey(
        EquipmentPosition,
        on_delete=models.CASCADE,
        related_name="test_results",
        blank=True,
        null=True,
    )

    test_date = models.DateField(
        blank=True,
        null=True,
    )

    measured_value = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        blank=True,
        null=True,
    )

    unit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    result_status = models.CharField(
        max_length=30,
        choices=RESULT_STATUS_CHOICES,
        default="NOT_TESTED",
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "test_result"
        ordering = ["-test_date", "-id"]

    def __str__(self):
        return (
            f"{self.report.report_no} - "
            f"{self.equipment.name} - "
            f"{self.test_name}"
        )


class ChecklistResponse(models.Model):
    report = models.ForeignKey(
        InspectionReport,
        on_delete=models.CASCADE,
        related_name="checklist_responses",
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="checklist_responses",
    )

    checklist_item = models.ForeignKey(
        ChecklistItem,
        on_delete=models.PROTECT,
        related_name="responses",
    )

    phase = models.ForeignKey(
        InspectionPhase,
        on_delete=models.CASCADE,
        related_name="responses",
        blank=True,
        null=True,
    )

    position = models.ForeignKey(
        EquipmentPosition,
        on_delete=models.CASCADE,
        related_name="responses",
        blank=True,
        null=True,
    )

    value_text = models.TextField(
        blank=True,
        null=True,
    )

    value_number = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        blank=True,
        null=True,
    )

    value_boolean = models.BooleanField(
        blank=True,
        null=True,
    )

    value_choice = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "checklist_response"
        ordering = ["checklist_item__sequence", "id"]

    def __str__(self):
        return (
            f"{self.report.report_no} - "
            f"{self.checklist_item.item_code}"
        )


