from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

def index(request):
    return render(request, 'index.html')

def createUser(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name= request.POST['first_name'],
            last_name= request.POST['last_name'],
            email= request.POST['email'],
            password= hash_pw
        )
        request.session['logged_user'] = new_user.id

        return redirect('/books')
    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]
            
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/books')
            messages.error(request, "email or password are incorrect")

    return redirect("/")

def welcomePage(request):
    if "logged_user" not in request.session:
        return redirect('/')
    else:
        this_user= User.objects.get(id=request.session['logged_user'])
        books= Book.objects.all()
        context = {
            "logged_user": User.objects.get(id=request.session['logged_user']),
            "books": books,
            "this_user": this_user,
        }
        return render(request, 'welcome.html', context)

def createBook(request):
        errors = Book.objects.book_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            if request.method == "POST":
                user = User.objects.get(id=request.session['logged_user'])
                book= Book.objects.create(
                    title= request.POST['title'],
                    description= request.POST['description'],
                    uploaded_by= user
                )
                user.liked_books.add(book)

                return redirect(f'/books/{book.id}')

def bookDetails(request, bookId):
    context = {
        'book': Book.objects.get(id=bookId),
        'current_user': User.objects.get(id=request.session['logged_user'])
    }
    return render(request, 'bookDetails.html', context)

def favorite(request, bookId):
    user = User.objects.get(id=request.session['logged_user'])
    book = Book.objects.get(id= bookId)
    user.liked_books.add(book)

    return redirect(f'/books/{bookId}')

def unfavorite(request, bookId):
    user= User.objects.get(id=request.session['logged_user'])
    book= Book.objects.get(id=bookId)
    user.liked_books.remove(book)

    return redirect(f'/books/{bookId}')

def updateBook(request, bookId):
    errors= Book.objects.editBook_validator(request.POST)

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{bookId}')
    else:
        if request.method == "POST":
            book= Book.objects.get(id=bookId)
            book.description= request.POST['description']
            book.save()

            return redirect(f'/books/{bookId}')

def deleteBook(request, bookId):
    book= Book.objects.get(id=bookId)
    book.delete()

    return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')

