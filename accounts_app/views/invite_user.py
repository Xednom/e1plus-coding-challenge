from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts_app.forms import InviteUserForm
from accounts_app.models import UserInvitation


class InviteUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # This would be the view where the invited user can join.
        # Here we have to check if the provided token points to an invitation which is valid and not expired.
        ...

    def post(self, request, *args, **kwargs):
        form = InviteUserForm(request.POST)
        now = timezone.now()

        if form.is_valid():
            email = form.cleaned_data["email"]

            # We could further improve this here to first check if an invitation for this email already exists and is not expired
            existing_invite = UserInvitation.objects.filter(
                email=email, expires_at__gte=now
            ).first()

            if existing_invite:
                messages.error(request, "An invitation for this email already exists.")
            else:
                # Delete the expired invitation for this email
                UserInvitation.objects.filter(email=email).delete()

                invitation = UserInvitation(email=email, invited_by=request.user)
                invitation.save()
                invitation.send_invitation_email()

                messages.success(request, "Invitation sent successfully.")

            return render(
                request,
                "accounts_app/profile.html",
                {"invite_user_form": form, "invited": True},
            )
        else:
            messages.error(request, "Error sending invitation.")
            return render(
                request, "accounts_app/profile.html", {"invite_user_form": form}
            )
