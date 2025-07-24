from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, Book, BorrowRecord
from .forms import RegisterForm
from django.utils import timezone

# Create your views here.

@login_required
def home_view(request):
    user = request.user
    # Getting relevant data to display on the homepage
    borrow_records = BorrowRecord.objects.filter(user=user).select_related('book').order_by('date_to_return')
    borrowed_books = borrow_records.filter(returned=False) # Books that haven't been returned (borrowed)
    borrowed_amount = borrowed_books.count() # Amount of books borrowed

    # Dividing by 6 because borrow limit is 6, and multiplying by 100 to convert to percentage
    borrowed_percentage = int(borrowed_amount / 6 * 100)

    context = {
        "borrow_records": borrow_records,
        "borrowed_books": borrowed_books,
        "borrowed_amount": borrowed_amount,
        "borrowed_percentage": borrowed_percentage,
    }

    return render(request, "home.html", context=context)

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        # Creating new user, logging them in, and redirecting them to the homepage
        if form.is_valid():
            user = form.save()
            login(request, user)
            student_id = form.cleaned_data.get('student_id')
            StudentProfile.objects.create(user=user, student_id=student_id)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == "POST":
        # Retrieving the data given from form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticating the user with the authenticate() function
        user = authenticate(request, username=username, password=password)

        # If user exists, log them in and redirect to homepage
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid Credentials!"
    return render(request, 'login.html', {'error': error_message})

def logout_view(request):
    if request.method == "POST":
        # Log the user out, and redirect to login page
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

@login_required
def library_view(request):
    user = request.user
    selected_category = request.GET.get("category")
    # Retrieving each book object, and ordering by title
    books = Book.objects.all().order_by("title")
    # Retriving each book ISBN the user has currently borrowed. Converted to a list.
    borrowed_isbns = list(BorrowRecord.objects.filter(user=user, returned=False).values_list("book__isbn", flat=True))

    # If user has selected a category, filter by chosen category
    if selected_category:
        books = books.filter(category=selected_category)

    context = {
        "books": books,
        "borrowed_isbns": borrowed_isbns,
        "categories": Book.CATEGORY_CHOICES
    }

    return render(request, "library.html", context=context)

@login_required
def return_view(request):
    user = request.user
    # Retrieving each BorrowRecord object ordered by date to return
    borrow_records = BorrowRecord.objects.filter(user=user).select_related('book').order_by('date_to_return')

    context = {
        "borrow_records": borrow_records,
    }

    return render(request, "return.html", context=context)

@login_required
def borrow_book(request, book_isbn):
    try:
        # Checking if book was found
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        # If not, display error message
        return messages.warning(request, "Book does not exist")

    borrow_count = BorrowRecord.objects.filter(user=request.user, returned=False).count()
    already_borrowed = BorrowRecord.objects.filter(user=request.user, book=book, returned=False).exists()

    # If borrow_count exceeds 6, display a warning message
    if borrow_count >= 6:
        messages.warning(request, "You can only borrow up to 6 books at a time.")
        return redirect('library')

    # If book has been already borrowed, display a warning message
    if already_borrowed:
        messages.warning(request, "You've already borrowed this book.")
        return redirect('library')
    
    # If available copies are in stock, borrow book.
    if book.available_copies > 0:
        BorrowRecord.objects.create(user=request.user, book=book)
        book.available_copies -= 1
        book.save()

    return redirect('library')

@login_required
def return_book(request, record_id):
    user = request.user

    try:
        record = BorrowRecord.objects.get(user=user, id=record_id)
        book = record.book
        # Setting the "returned" state to True
        record.returned = True
        record.date_returned = timezone.now()
        record.save()
        # Incrementing available copies of the book by 1
        book.available_copies += 1
        book.save()
    except BorrowRecord.DoesNotExist:
        messages.warning(request, "Borrow record does not exist")

    return redirect('return')