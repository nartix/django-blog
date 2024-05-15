from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

from users.forms.custom_user_creation_form import CustomUserCreationForm
from core.forms import EmailForm, UsernameForm
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            next_url = request.POST.get('next') or request.GET.get('next')

            # Make sure the 'next' url is safe to redirect to
            if next_url and is_safe_url(next_url, allowed_hosts={request.get_host()}):
                return HttpResponseRedirect(next_url)
            else:
                return redirect('core:index')
        else:
            messages.error(request, _('Invalid username or password.'))

    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Login"), "template": "users/login.html",
               "is_htmx_request": is_htmx_request, "next": request.GET.get('next', '')}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def logout(request):
    auth_logout(request)
    return redirect('core:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Sign Up"), "template": "users/registration/signup.html",
               "is_htmx_request": is_htmx_request, "validation_check": ["username", "email"], 'show_success_message': False,
               'action_url': reverse('users:signup')}

    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            # Redirect to a home page or any other page
            return redirect('core:index')
        else:
            if form.errors.get('username') is None:
                context['show_success_message'] = True

    context['form'] = form

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def signup_username(request):
    if not request.headers.get("HX-Request", False):
        return redirect('core:index')

    form = UsernameForm(request.POST or None)
    context = {'template': 'core/form/form_input_fields.html', 'form': form,
               "validation_check": ['username'], 'show_success_message': False}

    if request.method == 'POST' and form.is_valid():
        # username = form.cleaned_data.get('username')
        context['show_success_message'] = True

    fragment = render_to_string(context["template"], context, request)
    return HttpResponse(fragment)


def signup_email(request):
    if not request.headers.get("HX-Request", False):
        return redirect('core:index')

    form = EmailForm(request.POST or None)
    context = {'template': 'core/form/form_input_fields.html', 'form': form,
               'validation_check': ['email']}

    if request.method == 'POST':
        is_form_valid = form.is_valid()

    fragment = render_to_string(context['template'], context, request)
    return HttpResponse(fragment)


@login_required
def password_change(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            # Name of a url pattern to redirect to after success
            return redirect('users:password_change_done')
    else:
        form = PasswordChangeForm(request.user)

    context = {"title": _("Change Password"), "template": "users/registration/signup.html",
               'is_htmx_request': is_htmx_request, 'action_url': reverse('users:password_change'),
               'button_text': _("Change Password"), 'form': form}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def password_change_done(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Password Change Done"), "template": "users/registration/password_change_done.html",
               'is_htmx_request': is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)
