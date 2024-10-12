from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts_app.forms import InviteUserForm, RegistrationForm
from accounts_app.models import UserInvitation
from accounts_app.utils.mixins import PostOnlyLoginRequiredMixin


class InviteUserView(PostOnlyLoginRequiredMixin, View):

    def get(self, request, token=None, *args, **kwargs):
        # This would be the view where the invited user can join.
        # Here we have to check if the provided token points to an invitation which is valid and not expired.
        token = kwargs.get("id")
        print("token: ", token)

        # We validate the token here
        validated_token = UserInvitation.objects.filter(
            id=token, expires_at__gte=timezone.now()
        ).first()

        invitation = get_object_or_404(UserInvitation, id=token)

        if invitation.expires_at < timezone.now():
            messages.error(request, "This invitation has expired.")
            return render(request, "accounts_app/expired.html")

        if invitation.id:
            return render(
                request,
                "accounts_app/register.html",
                {"form": RegistrationForm, "invitation": invitation},
            )

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
