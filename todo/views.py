from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = context["task"].filter(user=self.request.user)
        context["count"] = context["task"].filter(complete=False).count()

        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["task"] = context["task"].filter(title__icontains=search_input)
            context["search_input"] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "todo/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"]
    # fields = ['title', 'description']
    success_url = reverse_lazy("task")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("task")


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task")


class CustomLoginView(LoginView):
    template_name = "todo/login.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("task")


class RegisterPage(FormView):
    template_name = "todo/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("task")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task")
        return super(RegisterPage, self).get(*args, *kwargs)

    def post(self, *args, **kwargs):
        form = self.get_form(self.form_class)
        if not form.is_valid():
            return self.form_invalid(form)

        return super(RegisterPage, self).post(*args, *kwargs)


class UserInfoView(LoginRequiredMixin, TemplateView):
    template_name = "todo/user-info.html"  # Replace 'user_info.html' with the actual template name for the user info page


class ResetPasswordView(PasswordResetView):
    template_name = (
        "todo/reset-password.html"  # Specify the template for the password reset form
    )
    email_template_name = "todo/reset_password_email.html"  # Optional: Specify the template for the email sent for password reset
    success_url = reverse_lazy(
        "password_reset_done"
    )  # Specify the URL to redirect to after a password reset request is submitted
