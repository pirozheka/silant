def get_user_role(user):
    if not user.is_authenticated:
        return "guest"
    if user.is_superuser:
        return "manager"
    if hasattr(user, "client"):
        return "client"
    if hasattr(user, "servicecompany"):
        return "service"
    if hasattr(user, "manager"):
        return "manager"
    return "unknown"