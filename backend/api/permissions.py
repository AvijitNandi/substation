from rest_framework.permissions import BasePermission


class IsInspector(BasePermission):
    """
    Allows access only to users in the INSPECTOR group.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="INSPECTOR").exists()
        )


class IsAdminReviewerApprover(BasePermission):
    """
    Allows access to ADMIN, REVIEWER, or APPROVER users.
    Superusers are also treated as ADMIN.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(
                    name__in=["ADMIN", "REVIEWER", "APPROVER"]
                ).exists()
            )
        )

class InspectionReportPermission(BasePermission):
    """
    Role-based permissions for InspectionReport.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser = ADMIN
        if request.user.is_superuser:
            return True

        user_roles = set(
            request.user.groups.values_list("name", flat=True)
        )

        # POST requests
        if request.method == "POST":

            # Status transition action
            if getattr(view, "action", None) == "change_status":
                return bool(
                    user_roles
                    & {
                        "ADMIN",
                        "INSPECTOR",
                        "REVIEWER",
                        "APPROVER",
                    }
                )

            # Normal report creation
            return bool(
                user_roles
                & {
                    "ADMIN",
                    "INSPECTOR",
                }
            )

        # All four functional roles can view reports
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return bool(
                user_roles
                & {
                    "ADMIN",
                    "INSPECTOR",
                    "REVIEWER",
                    "APPROVER",
                }
            )

        # PATCH, PUT, DELETE are checked at object level
        return bool(
            user_roles
            & {
                "ADMIN",
                "INSPECTOR",
                "REVIEWER",
                "APPROVER",
            }
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        user_roles = set(
            request.user.groups.values_list("name", flat=True)
        )

        # ADMIN can perform all actions
        if "ADMIN" in user_roles:
            return True

        # Status transition action
        if (
            getattr(view, "action", None) == "change_status"
            and request.method == "POST"
        ):
            new_status = request.data.get("status")

            # INSPECTOR
            if "INSPECTOR" in user_roles:
                return (
                    obj.created_by == request.user
                    and (
                        (obj.status == "DRAFT" and new_status == "SUBMITTED")
                        or (
                            obj.status == "REJECTED"
                            and new_status == "SUBMITTED"
                        )
                    )
                )

            # REVIEWER
            if "REVIEWER" in user_roles:
                return (
                    (obj.status == "SUBMITTED" and new_status == "UNDER_REVIEW")
                    or (
                        obj.status == "UNDER_REVIEW"
                        and new_status == "REJECTED"
                    )
                )

            # APPROVER
            if "APPROVER" in user_roles:
                return (
                    (obj.status == "UNDER_REVIEW"
                    and new_status == "FINAL_APPROVED")
                    or (
                        obj.status == "FINAL_APPROVED"
                        and new_status == "CLOSED"
                    )
                )

            return False

        # Everyone with an authorized role can view reports
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return bool(
                user_roles
                & {"INSPECTOR", "REVIEWER", "APPROVER"}
            )

        # INSPECTOR can modify only their own DRAFT or REJECTED report
        if "INSPECTOR" in user_roles:
            return (
                obj.created_by == request.user
                and obj.status in ["DRAFT", "REJECTED"]
            )

        # REVIEWER and APPROVER cannot directly modify reports
        return False

class ApprovalActionPermission(BasePermission):
    """
    Controls Approval actions based on user role.
    """

    ROLE_ACTIONS = {
        "ADMIN": {
            "SUBMITTED",
            "APPROVED",
            "REJECTED",
            "RETURNED",
        },
        "REVIEWER": {
            "RETURNED",
            "REJECTED",
        },
        "APPROVER": {
            "APPROVED",
            "REJECTED",
        },
    }

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser = ADMIN
        if request.user.is_superuser:
            return True

        user_roles = set(
            request.user.groups.values_list("name", flat=True)
        )

        allowed_roles = {"ADMIN", "REVIEWER", "APPROVER"}

        return bool(user_roles & allowed_roles)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # All authorized roles can view approval history
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            user_roles = set(
                request.user.groups.values_list("name", flat=True)
            )

            allowed_roles = {
                "ADMIN",
                "REVIEWER",
                "APPROVER",
            }

            return bool(user_roles & allowed_roles)

        # Approval records cannot be modified or deleted
        return False