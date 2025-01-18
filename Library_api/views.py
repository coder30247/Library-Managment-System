from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, datetime

from .models import *
from .serializer import *
# Create your views here.

def home(request):
	return render(request, 'Library_api/home.html')

class Book_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Book_Data.objects.all()
    serializer_class = Book_Data_Serializer

    @action(detail=True, methods=['get'])
    def retrieve_book(self, request, pk=None):
        book_id = pk
        try:
            book = Book_Data.objects.get(book_id=book_id)
        except Book_Data.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Book_Data_Serializer(book)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_book(self, request):
        serializer = Book_Data_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'])
    def update_book(self, request, pk=None):
        try:
            book = Book_Data.objects.get(book_id=pk)
        except Book_Data.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Book_Data_Serializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_book(self, request, pk=None):
        try:
            book = Book_Data.objects.get(book_id=pk)
        except Book_Data.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    # extra actions
    @action(detail=True, methods=['get'])
    def get_book_by_author(self, request, pk=None):
        try:
            author_name = pk
            books = Book_Data.objects.filter(author_name=author_name)
            serializer = Book_Data_Serializer(books, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # extra actions
    @action(detail=True, methods=['get'])
    def get_book_by_name(self, request, pk=None):
        try:
            book_name = pk
            books = Book_Data.objects.filter(book_name=book_name)
            serializer = Book_Data_Serializer(books, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


