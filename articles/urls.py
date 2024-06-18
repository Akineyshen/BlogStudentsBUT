from django.urls import path
from . import views
from .views import generate_pdf

urlpatterns = [
    path('', views.articles_main, name="articles_main"),
    path('articles/', views.articles, name="articles"),
    path('article/<slug:article_slug>/', views.article, name="article"),
    path('article/<slug:article_slug>/pdf/', generate_pdf, name='generate_pdf'),
    path('create/', views.createArticle, name='create_article'),
    path('update-article/<str:pk>/', views.updateArticle, name="update_article"),
    path('tag/<slug:tag_slug>/', views.articles_by_tag, name='tag'),
    path('delete-article/<str:pk>/', views.deleteArticle, name='delete_article'),
    path('edit_comment/<uuid:review_id>/', views.edit_review, name='edit_comment'),
    path('delete_comment/<uuid:review_id>/', views.delete_review, name='delete_comment'),
]