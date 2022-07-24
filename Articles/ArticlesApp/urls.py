from django.urls import path
from . import views

app_name = "ArticlesApp"

urlpatterns = [
    path("add_Bookmark/", views.add_Bookmark, name="add_Bookmark"),
    path("all_Bookmark/", views.list_Bookmark, name="list_Bookmark"),
    path("delete_Bookmark/<Bookmark_id>/", views.delete_Bookmark, name="delete_Bookmark"),

]
