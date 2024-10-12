from django.contrib.auth.mixins import AccessMixin


class PostOnlyLoginRequiredMixin(AccessMixin):
    """Mixin to require login for POST requests only."""

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and not request.user.is_authenticated:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
