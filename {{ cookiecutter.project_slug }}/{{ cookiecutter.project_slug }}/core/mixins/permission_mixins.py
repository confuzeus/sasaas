from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerRequiredMixin(LoginRequiredMixin):
    object_owner_attr = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if (
            not request.user.is_staff
            and getattr(obj, self.object_owner_attr) != request.user
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
