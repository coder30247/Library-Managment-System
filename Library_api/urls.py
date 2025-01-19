from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Student Data URLS
	path("student_data/", Student_Data_ViewSet.as_view({'get': 'list'}), name="student_data"),
    path("student_data/retrieve_student/<int:pk>/", Student_Data_ViewSet.as_view({'get': 'retrieve_student'}), name="retrieve_student"),
    path("student_data/add_student/", Student_Data_ViewSet.as_view({'post': 'add_student'}), name="add_student"),
    path("student_data/update_student/<int:pk>/", Student_Data_ViewSet.as_view({'put': 'update_student'}), name="update_student"),
    path("student_data/delete_student/<int:pk>/", Student_Data_ViewSet.as_view({'delete': 'delete_student'}), name="delete_student"),
    # Book Data URLS
    path("book_data/", Book_Data_ViewSet.as_view({'get': 'list'}), name="book_data"),
    path("book_data/retrieve_book/<int:pk>/", Book_Data_ViewSet.as_view({'get': 'retrieve_book'}), name="retrieve_book"),
    path("book_data/add_book/", Book_Data_ViewSet.as_view({'post': 'add_book'}), name="add_book"),
    path("book_data/update_book/<int:pk>/", Book_Data_ViewSet.as_view({'put': 'update_book'}), name="update_book"),
    path("book_data/delete_book/<int:pk>/", Book_Data_ViewSet.as_view({'delete': 'delete_book'}), name="delete_book"),
    # Issued Book Data URLS
    path("issued_book_data/", Issued_Book_Data_ViewSet.as_view({'get': 'list'}), name="issued_book_data"),
    path("issued_book_data/retrieve_issued_book/<int:pk>/", Issued_Book_Data_ViewSet.as_view({'get': 'retrieve_issued_book'}), name="retrieve_issued_books"),
    path("issued_book_data/issue_book/", Issued_Book_Data_ViewSet.as_view({'post': 'issue_book'}), name="issue_book"),
    path("issued_book_data/renew_book/<int:pk>/", Issued_Book_Data_ViewSet.as_view({'put': 'renew_issued_book'}), name="renew_issued_book"),
    path("issued_book_data/return_book/<int:pk>/", Issued_Book_Data_ViewSet.as_view({'delete': 'return_issued_book'}), name="return_issued_book"),
]