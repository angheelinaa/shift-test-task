from functools import wraps

from fastapi import HTTPException, status


def check_admin_role(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs.get("current_user")
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required role"
            )
        result = func(*args, **kwargs)
        return result
    return wrapper
