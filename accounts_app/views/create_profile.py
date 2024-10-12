from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext as _


from accounts_app.forms import RegistrationForm


class CreateProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in."))
            return redirect("home")  # Redirect logged-in users to the home page
        return render(
            request, "accounts_app/register.html", {"form": RegistrationForm()}
        )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in."))
            return redirect("home")  # Prevent authenticated users from registering

        form = RegistrationForm(request.POST)

        print("form: ", form)

        if form.is_valid():
            print("form email: ", form.cleaned_data)
            form.save()

            print("request: ", request)
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            print("user: ", user)
            if user is not None:
                login(request, user)
                messages.success(request, _("Registration successful! Welcome!"))
                return redirect(request.GET.get("next", "/"))
            else:
                messages.error(request, _("Authentication failed. Please try again."))
        else:
            messages.error(
                request, _("Error in registration. Please correct the form.")
            )

        return render(request, "accounts_app/register.html", {"form": form})
