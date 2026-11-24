def login_required(view):
    """Rejects anonymous requests before the view runs."""
    def wrapper(request, *args, **kwargs):
        if request.user is None:
            raise PermissionError("login required")
        return view(request, *args, **kwargs)
    wrapper.__name__ = view.__name__
    return wrapper
