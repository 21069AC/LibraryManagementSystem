from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Using UserCreationForm to register new users
# UserCreationForm allows the ability to create custom fields (like student_id)
# Username, password, and password confirmation are default fields

class RegisterForm(UserCreationForm):
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

    # Validating StudentID by making sure it's a string consisting of 5 digits
    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"]

        if len(student_id) != 5: # Raise an error if its not 5 characters in length
            raise forms.ValidationError("StudentID must be exactly 5 digits long!")
        elif not student_id.isdigit(): # Raise an error if characters other than digits are used
            raise forms.ValidationError("StudentID must only consist of digits!")
        else: # Else, return student_id as it is (already valid)
            return student_id
