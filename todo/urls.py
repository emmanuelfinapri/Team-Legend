from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CustomLoginView,
    RegisterPage,
    ResetPasswordView,
    TaskCreate,
    TaskDelete,
    TaskDetail,
    TaskList,
    TaskUpdate,
    UserInfoView,
)

urlpatterns = [
    path("", TaskList.as_view(), name="task"),
    path("task-create/", TaskCreate.as_view(), name="task-create"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="tasks-detail"),
    path("task-update/<int:pk>/", TaskUpdate.as_view(), name="tasks-update"),
    path("task-delete/<int:pk>/", TaskDelete.as_view(), name="tasks-delete"),
    path("user-info/", UserInfoView.as_view(), name="user-info"),
    # Password reset URLs
    path("reset-password/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
