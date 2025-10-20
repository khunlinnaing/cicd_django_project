from django.urls import path
from . import views

app_name='website'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_post, name='create-post'),
    path('<int:pk>/post', views.get_detail, name='get-detail'),
    path('<int:pk>/edit', views.update_post, name='update-post'),
]
