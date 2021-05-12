"""User application URLS."""

# django modules
from django.urls import path

# views
from users import views

urlpatterns = [

    # posts
    path(
        route='find/<str:username>/',
        view=views.UserDetailView.as_view(),
        name='detail',
    ),

    # management
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('me/profile/', views.UpdateProfileView.as_view(), name='update'),

]