from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('books/', views.Book_Data_ViewSet.as_view({'get': 'list', 'post': 'create'}), name='books'),
]
