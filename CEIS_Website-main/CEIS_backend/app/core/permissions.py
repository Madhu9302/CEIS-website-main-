from typing import Callable, List
from fastapi import Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.user import User

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Ensures the user has administrative privileges (either 'admin' or 'super_admin').
    """
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin portal privileges required",
        )
    return current_user

# Alias for backwards compatibility with existing route imports
require_admin = get_current_admin

def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Restricts access strictly to 'super_admin'.
    """
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin privileges required",
        )
    return current_user

def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Factory dependency to enforce specific roles.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Requires one of {', '.join(allowed_roles)}",
            )
        return current_user
    return role_checker

def require_permission(permission_name: str) -> Callable:
    """
    Permission-based RBAC dependency.
    Super admin automatically possesses all permissions; other roles are verified.
    """
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role == "super_admin":
            return current_user
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_name}' required",
            )
        return current_user
    return permission_checker
