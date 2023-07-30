# flake8: noqa WPS430
def add_created_by(function):
    """Decorator for adding created_by into the request.data."""

    def _add_created_by(request, *args, **kwargs):
        """Decorator method."""
        request.data['created_by'] = request.user.id
        return function(request, *args, **kwargs)

    return _add_created_by


def add_updated_by(function):
    """Decorator for adding updated_by into the request.data."""

    def _add_updated_by(request, *args, **kwargs):
        """Decorator method."""
        request.data['updated_by'] = request.user.id
        return function(request, *args, **kwargs)

    return _add_updated_by


def add_deleted_by(function):
    """Decorator for adding created_by into the request.data."""

    def _add_deleted_by(request, *args, **kwargs):
        """Decorator method."""
        request.data['created_by'] = request.user.id
        return function(request, *args, **kwargs)

    return _add_deleted_by
