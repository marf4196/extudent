from django.urls import path
from .views import (
    RegisterApiView,
    ProfileViewSet,
    UserDocAdminViewSet,
    ProfileDocsViewSet,
    LogoutView,
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("token/login/", ObtainAuthToken.as_view(), name="token_obtain"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path(
        "user/profile/<int:pk>/",
        ProfileViewSet.as_view({"get": "retrive", "patch": "partial_update"}),
        name="profile",
    ),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    # list of accounts with is_complete=False
    path(
        "admin/userdocs/",
        UserDocAdminViewSet.as_view({"get": "list", "post": "create"}),
        name="user-docs-list",
    ),
    path(
        "admin/userdocs/<int:pk>/",
        UserDocAdminViewSet.as_view(
            {"get": "retrive", "put": "update", "patch": "partial_update"}
        ),
        name="user-docs-detail",
    ),
    path(
        "userdocs/<int:pk>/",
        ProfileDocsViewSet.as_view(
            {
                "get": "retrive",
            }
        ),
        name="retrive-user-docs",
    ),
    path(
        "userdocs/",
        ProfileDocsViewSet.as_view({"post": "create"}),
        name="upload-user-docs",
    ),
]
