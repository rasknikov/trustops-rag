from dataclasses import dataclass

@dataclass
class AccessInput:
    tenant_id: str
    resource_tenant_id: str
    resource_allowed: bool
    contains_sensitive_data: bool

@dataclass
class AccessDecision:
    allowed: bool
    reason: str

def validate_access_input(access_input: AccessInput) -> None:
    if not access_input.tenant_id.strip():
        raise ValueError("Tenant id cannot be empty.")
    
    if not access_input.resource_tenant_id.strip():
        raise ValueError("Resource tenant id cannot be empty.")
    
def is_tenant_allowed(access_input: AccessInput) -> bool:
    if access_input.tenant_id == access_input.resource_tenant_id and access_input.resource_allowed:
        return True
    else:
        return False

def check_access(access_input: AccessInput) -> AccessDecision:
    
    validate_access_input(access_input)

    is_allowed = is_tenant_allowed(access_input)

    if is_allowed:
        return AccessDecision(
        allowed=is_allowed,
        reason="tenant_match"
        )

    if access_input.contains_sensitive_data and not access_input.resource_allowed:
        return AccessDecision(
        allowed=is_allowed,
        reason="sensitive_resource_denied"
        )
    
    return AccessDecision(
        allowed=is_allowed,
        reason="tenant_mismatch_or_resource_denied"
        )

    
