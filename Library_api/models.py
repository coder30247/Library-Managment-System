from django.db import models

# Create your models here.

class Book_Data(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return self.book_name

class Student_Data(models.Model):
    register_number = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=100, null=True, blank=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True, blank=True)
    borrowed_book_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.student_name

class Issued_Book_Data(models.Model):
    borrower = models.ForeignKey(Student_Data, on_delete=models.CASCADE)
    issued_book = models.ForeignKey(Book_Data, on_delete=models.CASCADE)
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower.student_name} - {self.issued_book.book_name}"
