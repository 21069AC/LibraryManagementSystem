from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # Register, login, and logout URL's
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # Home, library and return books URL's
    path('', views.home_view, name="home"),
    path('library/', views.library_view, name="library"),
    path('return/', views.return_view, name="return"),

    path('borrow/<str:book_isbn>/', views.borrow_book, name='borrow_book'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
