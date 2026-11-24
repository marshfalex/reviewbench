from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """Result of a permission check. Callers must look at .allowed; the reason is for audit logs."""
    allowed: bool
    reason: str


def can_edit(user, doc) -> Decision:
    if user.is_admin:
        return Decision(True, "admin")
    if doc.owner_id == user.id:
        return Decision(True, "owner")
    if user.id in doc.editor_ids:
        return Decision(True, "shared editor")
    return Decision(False, "not owner or editor")
