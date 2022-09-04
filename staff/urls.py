from django.urls import path
from . import views

urlpatterns = [
    path("edit-test/<int:id>", views.edit_test, name="edit_test"),
    path("new-test/", views.new_test, name="new_test"),
    path("delete-test/<int:id>", views.delete_test, name="delete_test"),    
    path("tests/", views.tests, name="tests"),
    path("preview-test/<int:id>", views.preview_test, name="preview_test"),
] 