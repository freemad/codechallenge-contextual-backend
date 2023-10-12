from django.urls import path

from analytics import views

app_name = "analytics"
urlpatterns = [
    path("sync/", views.sync, name="sync"),
    path("<str:instance_id>/events/<int:pk>/", views.event, name="event"),
    path("<str:instance_id>/events/", views.event_list, name="events"),
]
