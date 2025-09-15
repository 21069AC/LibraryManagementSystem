from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import StudentProfile, Book, BorrowRecord
from .forms import RegisterForm, AddBook
from django.db.models import Q, Prefetch
from django.utils import timezone
from django.db.models import Count

# Create your views here.

@login_required
def home_view(request):
    user = request.user
    # Getting relevant information to display on the homepage
    borrow_records = BorrowRecord.objects.filter(user=user).select_related('book').order_by('date_to_return')
    borrowed_books = borrow_records.filter(returned=False) # Books currently borrowed (not yet returned)
    returned_books = borrow_records.filter(returned=True).count() # Amount of books returned
    borrowed_amount = borrowed_books.count() # Amount of books borrowed
    overdue_amount = BorrowRecord.objects.filter( # Amount of books overdue
        user=request.user,
        returned=False,
        date_to_return__lt=timezone.now()
    ).count()

    # Dividing by 6 because borrow limit is 6, and multiplying by 100 to convert to a percentage value
    borrowed_percentage = int(borrowed_amount / 6 * 100)
    overdue_percentage = int(overdue_amount / 6 * 100)

    # Getting the user's favourite category based on previously borrowed books
    favourite_category = (
        BorrowRecord.objects
        .filter(user=user)
        .values("book__category")
        .annotate(count=Count("book__category"))
        .order_by("-count")
        .first()
    )

    # If a favourite category exists, set favourite to a displayable string
    if favourite_category:
        favourite_category = dict(Book.CATEGORY_CHOICES).get(favourite_category["book__category"])

    context = {
        "borrow_records": borrow_records,
        "returned_books": returned_books, 
        "borrowed_books": borrowed_books,
        "borrowed_amount": borrowed_amount,
        "overdue_amount": overdue_amount,
        "borrowed_percentage": borrowed_percentage,
        "overdue_percentage": overdue_percentage,
        "favourite_category": favourite_category,
        "total_books": Book.objects.count()
    }

    return render(request, 'home.html', context=context)

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        # Creating new user, logging them in, and redirecting them to the homepage
        if form.is_valid():
            user = form.save()
            # Automatically logging the user in
            login(request, user)
            # Retrieving the student ID from the form
            student_id = form.cleaned_data.get("student_id")
            # Creating the user's StudentProfile with their student ID
            StudentProfile.objects.create(user=user, student_id=student_id)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {"form": form, "hide_navbar": True})

def login_view(request):
    error_message = None
    if request.method == "POST":
        # Retrieving the username and password given from the form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticating the user with the authenticate() function
        user = authenticate(request, username=username, password=password)

        # If user already exists, automatically login and redirect to the homepage
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid Credentials. Please retry your username or password."
    return render(request, 'login.html', {"error": error_message, "hide_navbar": True})

def logout_view(request):
    if request.method == "POST":
        # Log the user out, and redirect them to the login page
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

@login_required
def library_view(request):
    user = request.user
    # Retrieving the user's selected category
    selected_category = request.GET.get("category")
    # Retrieving the user's search query
    search_query = request.GET.get("q")
    # Retrieving each book object, and ordering by title
    books = Book.objects.all().order_by("title")
    # Retriving each book ISBN the user has currently borrowed. Converted to a list so it's iterable.
    borrowed_isbns = list(BorrowRecord.objects.filter(user=user, returned=False).values_list("book__isbn", flat=True))

    # If user has selected a category, filter by chosen category
    if selected_category:
        books = books.filter(category=selected_category)

    # If user has searched via searchbar, display by either book title, author, or ISBN number
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    context = {
        "books": books,
        "borrowed_isbns": borrowed_isbns,
        "categories": Book.CATEGORY_CHOICES
    }

    return render(request, 'library.html', context=context)

@login_required
def return_view(request):
    user = request.user
    # Retrieving each BorrowRecord object ordered by date_to_return
    borrow_records = BorrowRecord.objects.filter(user=user, returned=False).select_related("book").order_by("date_to_return")

    context = {
        "borrow_records": borrow_records,
    }

    return render(request, 'return.html', context=context)

@staff_member_required
def add_book(request):
    if request.method == "POST":
        form = AddBook(request.POST, request.FILES)

        if form.is_valid(): # If form was valid, add book
            form.save()
            messages.success(request, "Book was added successfully!")
        else: # Else, display an error message
            messages.error(request, "There was an error")
    else:
        form = AddBook()
    return render(request, 'addbook.html', {"form": form})

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.all()
    total_books = Book.objects.count()
    total_borrowed_books = BorrowRecord.objects.filter(returned=False).count()
    overdue_count = BorrowRecord.objects.filter(returned=False, date_to_return__lt=timezone.now()).count()

    users = User.objects.prefetch_related(
    Prefetch(
        "borrowrecord_set",
        queryset=BorrowRecord.objects.filter(returned=False).select_related("book")
    ))

    context = {
        "total_users": total_users.count(),
        "total_books": total_books,
        "total_borrowed_books": total_borrowed_books,
        "overdue_count": overdue_count,
        "users": users,
    }

    return render(request, 'admin-dashboard.html', context=context)

@login_required
def borrow_book(request, book_isbn):
    try:
        # Checking if book was found by searching for book ISBN
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        # If not, display an error message
        return messages.warning(request, "Book does not exist")

    # Getting the current amount of books borrowed
    borrow_count = BorrowRecord.objects.filter(user=request.user, returned=False).count()
    # Checks if the requested book has already been borrowed (returns True or False)
    already_borrowed = BorrowRecord.objects.filter(user=request.user, book=book, returned=False).exists()

    # If borrow_count exceeds 6, display a warning message
    if borrow_count >= 6:
        messages.error(request, "You can only borrow up to 6 books at a time.")
        return redirect('library')

    # If book has been already borrowed, display a warning message
    if already_borrowed:
        messages.error(request, "You've already borrowed this book.")
        return redirect('library')
    
    # If available copies are in stock (available_copies > 0), borrow book
    if book.available_copies > 0:
        messages.success(request, f'"{book.title}" was successfully borrowed!')
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
        # Display a successful message
        messages.success(request, f'"{book.title}" was successfully returned!')
    except BorrowRecord.DoesNotExist:
        messages.error(request, "BorrowRecord does not exist")

    return redirect('return')
