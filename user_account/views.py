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

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request,f'User with email: {email} does not exists!')
            return redirect('login-url')
        elif email=='admin@gmail.com' and password=='admin':
            user = authenticate(request,email=email,password=password)
            if user is None:
                messages.error(request,'Wrong password!')
            else:
                login(request,user)
                return redirect('/admin')
        else:
            user = authenticate(request,email=email,password=password)
            if user is None:
                messages.error(request,'Wrong password!')
            else:
                login(request,user)
                return redirect('user-homepage-url')
    return render(request,'login_page.html')

def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email_id')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phone = request.POST.get('mobile_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if confirm_password != password:
            messages.info(request,f'Password does not match!')
            return redirect('signup-url')
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request,f'Email {email} already exists!')
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
            user = authenticate(request,email=email,password=password)
            login(request,user)
            return redirect('user-homepage-url')
    return render(request,'signup_page.html')

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def user_homepage(request):
    trending_books = Books.objects.annotate(
        borrowed_books = Count('librarymanagement')
    ).order_by('-borrowed_books')[:4]
    all_books = Books.objects.values('id','title','cover_image','author')
    context = {
        'trending_books': trending_books,
        'all_books': all_books
    }
    return render(request,'user_home.html',context=context)

@login_required(login_url='/login/')
def user_update(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            user = request.user
            if first_name and first_name != '':
                user.first_name = first_name
            else:
                messages.warning(request,'First Name cannot be empty!')
            if last_name and last_name != '':
                user.last_name = last_name
            else:
                messages.warning(request,'Last Name cannot be empty!')
            if username and username != '':
                user.username = username
            else:
                messages.warning(request,'Username cannot be empty!')
            if email and email != '':
                user.email = email
            else:
                messages.warning(request,'Email cannot be empty!')
            if phone and phone != '':
                user.phone = phone
            else:
                messages.warning(request,'Mobile Number cannot be empty!')
            user.save()
            messages.success(request,f'Profile successfully updated!')
            return redirect('user-update-url')
        except Exception as e:
            messages.error(request,f'Error {str(e)} while updating profile!')
            return redirect('user-update-url')
    else:
        return render(request, 'user_profile.html')