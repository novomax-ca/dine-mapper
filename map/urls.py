from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_marker", views.add_marker, name="add_marker"),
    path("get_markers", views.get_markers, name="get_markers"),
    path("delete_marker/<int:marker_id>", views.delete_marker, name="delete_marker"),
    path("load_marker_form", views.load_marker_form, name="load_marker_form"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
]

