from django.urls import path
from . import views

app_name='website'
urlpatterns = [
    path('', views.index, name='index'),
    path('getform/', views.get_create_post, name='get-create-post'),
    path('create/', views.post_create_post, name='post-create-post'),
    path('<int:pk>/post', views.get_detail, name='get-detail'),
    path('<int:pk>/edit', views.update_post, name='update-post'),
]
