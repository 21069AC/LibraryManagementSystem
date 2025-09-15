from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Using UserCreationForm to register new users
# UserCreationForm allows the ability to create custom fields (like student_id)
# Username, password, and password confirmation are default fields

class RegisterForm(UserCreationForm):
    # FIELDS
    username = forms.CharField(min_length=3, max_length=30, required=True)
    email = forms.EmailField(required=False)
    student_id = forms.CharField(max_length=5, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'student_id',
            'password1',
            'password2',
        ]

    # Validating the StudentID by making sure it's a string consisting of 5 digits
    def clean_student_id(self):
        # Retrieving the student ID
        student_id = self.cleaned_data["student_id"]

        if len(student_id) != 5: # If student_id is not 5 characters in length, raise an error
            raise forms.ValidationError("StudentID must be exactly 5 digits long!")
        elif not student_id.isdigit(): # In the case of characters other than digits are used, raise an error 
            raise forms.ValidationError("StudentID must only consist of digits!")
        else: # Else, return student_id as it is (all conditions are met, and are valid)
            return student_id

# A form for administrators to add books within the /addbook page
# Regular users are unable to access this

class AddBook(forms.ModelForm):
    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "year",
            "cover",
            "category",
            "total_copies",
            "isbn"
        ]