from django.contrib import admin
from .models import StudentProfile, Book, BorrowRecord

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(Book)
admin.site.register(BorrowRecord)