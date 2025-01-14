from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>', views.index, name='category'),
    path('detail/<int:recipe_id>', views.detail, name='detail'),
    path('edit', views.edit, name='new'),
]
