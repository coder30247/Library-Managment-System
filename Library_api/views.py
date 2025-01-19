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
        
        # Extract only the fields that are allowed to be updated
        allowed_fields = ['book_name', 'author_name']
        update_data = {field: value for field, value in request.data.items() if field in allowed_fields}
        
        serializer = Book_Data_Serializer(book, data=update_data, partial=True)  # Use `partial=True` to allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

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


class Student_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Student_Data.objects.all()
    serializer_class = Student_Data_Serializer

    @action(detail=True, methods=['get'])
    def retrieve_student(self, request, pk=None):
        register_number = pk
        try:
            student = Student_Data.objects.get(register_number=register_number)
        except Student_Data.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Student_Data_Serializer(student)
        issued_books = Issued_Book_Data.objects.filter(borrower_id=register_number)

        # Convert serializer data to a dictionary to modify it
        student_data = serializer.data

        if issued_books.exists():
            issued_books_serializer = Issued_Book_Data_Serializer(issued_books, many=True)
            for book in issued_books_serializer.data:
                due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
                fine_amount = (date.today() - due_date).days * 1  # 1 Rs per day
                if fine_amount < 0:
                    fine_amount = 0
                book['fine_amount'] = fine_amount

                # Get the book details
                book_id = book['issued_book']
                book_details = Book_Data.objects.get(book_id=book_id)
                book['book_name'] = book_details.book_name
                book['author_name'] = book_details.author_name

            student_data['issued_books'] = issued_books_serializer.data
        else:
            student_data['issued_books'] = 'No book due to be returned'

        return Response(student_data)

    @action(detail=False, methods=['post'])
    def add_student(self, request):
        serializer = Student_Data_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_student(self, request, pk=None):
        try:
            student = Student_Data.objects.get(register_number=pk)
        except Student_Data.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define the fields that are allowed to be updated
        allowed_fields = ['student_name', 'student_email','student_due_amount','borrowed_book_count']
        update_data = {field: value for field, value in request.data.items() if field in allowed_fields}

        serializer = Student_Data_Serializer(student, data=update_data, partial=True)  # Use `partial=True` to allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['delete'])
    def delete_student(self, request, pk=None):
        try:
            student = Student_Data.objects.get(register_number=pk)
        except Student_Data.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class Issued_Book_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Issued_Book_Data.objects.all()
    serializer_class = Issued_Book_Data_Serializer

    @action(detail=True, methods=['get'])
    def retrieve_issued_book(self, request, pk=None):
        try:
            # Attempt to retrieve issued books by the given book ID
            issued_books = Issued_Book_Data.objects.filter(issued_book_id=pk)
            
            if not issued_books.exists():
                # If no issued books found, check if the book exists in Book_Data
                if Book_Data.objects.filter(book_id=pk).exists():
                    book = Book_Data.objects.get(book_id=pk)
                    book_serializer = Book_Data_Serializer(book)
                    return Response({'message': 'Book Not Issued', 'book_details': book_serializer.data})
                return Response({'error': 'Book Not Available'}, status=status.HTTP_404_NOT_FOUND)
            
            # If issued books found, serialize them
            serializer = Issued_Book_Data_Serializer(issued_books, many=True)
            issued_books_data = serializer.data
            
            # Add borrower details to the issued books data
            for issued_book_data in issued_books_data:
                borrower_register_number = issued_book_data['borrower']
                borrower = Student_Data.objects.get(register_number=borrower_register_number)
                borrower_serializer = Student_Data_Serializer(borrower)
                issued_book_data['borrower_details'] = borrower_serializer.data
            
            return Response(issued_books_data)
        
        except (Issued_Book_Data.DoesNotExist, Book_Data.DoesNotExist, Student_Data.DoesNotExist):
            return Response({'error': 'Book Not Available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def issue_book(self, request):
        serializer = Issued_Book_Data_Serializer(data=request.data)
        if serializer.is_valid():
            student_register_number = request.data.get('borrower')  # Assuming borrower is the register_number
            book_id = request.data.get('issued_book')  # The ID of the book being issued

            # Check if the book is already issued
            if Issued_Book_Data.objects.filter(issued_book_id=book_id).exists():
                return Response({'error': 'This book is already issued to another borrower'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the student
            try:
                student = Student_Data.objects.get(register_number=student_register_number)
            except Student_Data.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the student has reached the borrowing limit
            if student.borrowed_book_count < 3:
                # Save the book issue record
                issued_book = serializer.save()
                student.borrowed_book_count += 1
                student.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Cannot borrow more than 3 books'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def renew_issued_book(self, request, pk=None):
        try:
            issued_book = Issued_Book_Data.objects.get(pk=pk)
        except Issued_Book_Data.DoesNotExist:
            return Response({'error': 'Issued book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the due_date has exceeded today's date
        if issued_book.due_date < date.today():
            # Calculate the number of days the book is overdue
            days_overdue = (date.today() - issued_book.due_date).days

            # Calculate the fine amount
            fine_amount = days_overdue * 1  # 1 Rs per day

            # Update the student's due_amount
            student = Student_Data.objects.get(register_number=issued_book.borrower.register_number)
            student.due_amount += fine_amount
            student.save()

        # Update only the due_date
        issued_book.due_date = date.today() + timedelta(days=14)
        issued_book.save()

        # Serialize and return the updated instance
        serializer = Issued_Book_Data_Serializer(issued_book)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def return_issued_book(self, request, pk=None):
        try:
            issued_book = Issued_Book_Data.objects.get(pk=pk)
        except Issued_Book_Data.DoesNotExist:
            return Response({'error': 'Issued book not found'}, status=status.HTTP_404_NOT_FOUND)

        borrower = issued_book.borrower

        # Decrease the student's borrowed book count
        borrower.borrowed_book_count -= 1
        borrower.save()

        # Remove the issued book record
        issued_book.delete()
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def get_books_due(self, request, pk=None):
        try:
            borrower = pk
            issued_books = Issued_Book_Data.objects.filter(borrower=borrower)
            serializer = Issued_Book_Data_Serializer(issued_books, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)