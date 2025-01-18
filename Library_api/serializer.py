from rest_framework import serializers
from .models import Student_Data, Book_Data, Issued_Book_Data
from datetime import date, timedelta


class Student_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Data
        fields = ['register_number', 'student_name','student_email', 'due_amount', 'borrowed_book_count']


class Book_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Data
        fields = ['book_id', 'book_name', 'author_name']


class Issued_Book_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Issued_Book_Data
        fields = ['borrower', 'issued_book', 'issue_date', 'due_date']

    def create(self, validated_data):
        validated_data['issue_date'] = date.today()
        validated_data['due_date'] = date.today() + timedelta(days=14)
        return super().create(validated_data)

    def update(self, instance):
        instance.due_date = date.today() + timedelta(days=14)
        instance.save()
        return instance
