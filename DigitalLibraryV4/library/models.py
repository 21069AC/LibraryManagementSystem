from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def get_return_date():
    # Gets return date 7 days (one week) from the current time
    return timezone.now() + timedelta(days=7)

# Create your models here.

class StudentProfile(models.Model):
    # FIELDS
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=5, primary_key=True)

    # Displaying the StudentProfiles's: username & student ID.
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
        # EXAMPLE: bob - 21026

class Book(models.Model):
    # A list consisting of tuples on popular categories of books
    CATEGORY_CHOICES = [
        ("children", "Children's"),
        ("pre-teen", "Pre-teen"),
        ("classic", "Classic"),
        ("fantasy", "Fantasy"),
        ("programming", "Programming"),
        ("sci-fi", "Sci-Fi"),
        ("mystery", "Mystery"),
        ("misc", "Miscellaneous"),
    ]

    # FIELDS
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=80)
    year = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="misc")
    total_copies = models.PositiveIntegerField(default=3)
    available_copies = models.PositiveIntegerField(default=3)
    isbn = models.CharField(max_length=13, unique=True, null=True) # ISBN-13 (13 digits)

    # METHODS

    # Overwriting the save() method
    def save(self, *args, **kwargs):
        # If the Book object is being created, set the available copies to total copies
        if not self.pk:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

    # Displaying the Book's: title, author, and year
    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"
        # EXAMPLE: The Lorax by Dr. Seuss (1971)

class BorrowRecord(models.Model):
    # FIELDS
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    date_to_return = models.DateTimeField(default=get_return_date)
    date_returned = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    # METHODS

    # Displaying the BorrowRecord's: return status, username, book title, and return date
    def __str__(self):
        borrow_date = self.borrow_date.strftime("%d/%m/%y")
        date_to_return = self.date_to_return.strftime("%d/%m/%y")
        return_status = "RETURNED" if self.returned else "BORROWED"

        return f"[{return_status}] USER: {self.user.username} \
        BORROWED: {self.book.title} at: {borrow_date} Return by: {date_to_return}"
        # Example: [BORROWED] USER: bob BORROWED: The Lorax at: 24/07/2025 Return by: 31/07/2025
    
    # Determines whether book is overdue by returning a boolean (True or False)
    def is_overdue(self):
        return timezone.now() > self.date_to_return
    
    # Evaluates the amount of days till the return date
    def days_to_return(self):
        return (self.date_to_return - timezone.now()).days
