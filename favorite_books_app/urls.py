from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.welcomePage),
    path('books/<int:bookId>', views.bookDetails),
    path('user/create_user', views.createUser),
    path('books/create_book', views.createBook),
    path('books/<int:bookId>/update', views.updateBook),
    path('books/<int:bookId>/delete', views.deleteBook),
    path('books/<int:bookId>/favorite', views.favorite),
    path('books/<int:bookId>/unfavorite', views.unfavorite),
    path('user/login', views.login),
    path('user/logout', views.logout),
]