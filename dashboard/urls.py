from django.urls import path

from dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("logon/", views.logon, name="logon"),
    path("<str:instance_id>/logoff/", views.logoff, name="logoff"),
    path("<str:instance_id>/statuses/", views.pointer_statuses, name="statuses")
]
