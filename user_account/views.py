from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from user_account.models import CustomUser
from books.models import Books
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'main.html')

def login_page(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')
        
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(req,f'User with email: {email} does not exists!')
            return redirect('login-url')
        elif email=='admin@gmail.com' and password=='admin':
            user = authenticate(req,email=email,password=password)
            if user is None:
                messages.error(req,'Wrong password!')
            else:
                login(req,user)
                return redirect('/admin')
        else:
            user = authenticate(req,email=email,password=password)
            if user is None:
                messages.error(req,'Wrong password!')
            else:
                login(req,user)
                return redirect('user-homepage-url')
    return render(req,'login_page.html')

def signup_page(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email_id')
        firstname = req.POST.get('first_name')
        lastname = req.POST.get('last_name')
        phone = req.POST.get('mobile_number')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if confirm_password != password:
            messages.info(req,f'Password does not match!')
            return redirect('signup-url')
        if CustomUser.objects.filter(email=email).exists():
            messages.info(req,f'Email {email} already exists!')
            return redirect('signup-url')
        else:
            user = CustomUser.objects.create_user(
                username = username,
                email=email,
                first_name = firstname,
                last_name = lastname,
                phone = phone,
                password = password
            )
            user.save()
            user = authenticate(req,email=email,password=password)
            login(req,user)
            return redirect('user-homepage-url')
    return render(req,'signup_page.html')

@login_required(login_url='/login/')
def logout_user(req):
    logout(req)
    return redirect('home')

@login_required(login_url='/login/')
def user_homepage(req):
    trending_books = Books.objects.annotate(
        borrowed_books = Count('librarymanagement')
    ).order_by('-borrowed_books')[:4]
    all_books = Books.objects.values('title','cover_image','author')
    context = {
        'trending_books': trending_books,
        'all_books': all_books
    }
    return render(req,'user_home.html',context=context)