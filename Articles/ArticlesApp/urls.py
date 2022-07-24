from django.urls import path
from . import views

app_name = "ArticlesApp"

urlpatterns = [
    path("add_bookmark/", views.add_bookmark, name="add_bookmark"),
    path("all_bookmark/", views.list_bookmark, name="list_bookmark"),
    path("delete_bookmark/<bookmark_id>/", views.delete_bookmark, name="delete_bookmark"),
    path("top5/", views.top5_Article, name="top5_Article"),
    path("search/", views.search_for_article, name="search_for_article"),

    path("add_comment/<article_id>/", views.add_comment, name="add_comment"),
    path("view_comment", views.view_comment, name="view_comment"),
    path("delete_comment/<comment_id>/", views.delete_comment, name="delete_comment"),

    path('article/', views.add_article, name='article'),
    path('all_articles/', views.all_articles, name='all_articles'),
    path('update_article/<article_id>/', views.update_article, name='update_article'),
    path('delete_article/<article_id>/', views.delete_article, name='delete_article'),
    path('posted_articles_per_publisher/<publisher_id>/', views.posted_articles_per_publisher, name='posted_articles_per_publisher'),

]
