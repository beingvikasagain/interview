from django.urls import path

from users.views import TaskView

urlpatterns = [
    path('task/',TaskView.as_view()),
]
