from django.shortcuts import render,redirect
from django.contrib import messages
# from django.contrib import sessions
from .models import*
import random
import requests
from django.core.mail import send_mail 

# Create your views here.
def index(request):
    if 'email' in request.session:
        uid=signup.objects.get(email=request.session['email'])
        mid = categories.objects.all()
        product = products.objects.all()
        mid2 = request.GET.get("mid2")
        if mid2:
            product = products.objects.filter(categories_id= mid2)
        else:
            product = products.objects.all()

        con={"uid" : uid, "mid" : mid, "product" : product,}
        print(request.session.get('email'))
        return render(request, "index.html",con) 
    else:
        return render(request, "login.html") 

def about(request):
    return render(request,"about.html")

def blog_detail(request):
    return render(request, "blog_detail.html")

def blog(request):
    return render(request, "blog.html")

def contact(request):
    return render(request, "contact.html")

def product_detail(request):
    return render(request, "product_detail.html") 

def product(request):
    mid = categories.objects.all()
    product = products.objects.all()
    mid2=request.GET.get("mid2")

    if mid2:
        product = products.objects.filter(categories_id=mid2)
    else:
        product = products.objects.all()

    context = {'mid' : mid , 'product' : product}
    print({'product': product})
    return render(request, "product.html", context)

def price_filter(request):
    if 'email' in request.session:
        get_categories = categories.objects.all()
        get_products = products.objects.all()
        min_price = request.GET.get("min")
        max_price = request.GET.get("max")

        print(get_categories)
        print(get_products)
        if not min_price and not max_price:
            print('hello')
            return redirect("product")
        else:
            try:
                print('hrllo1')
                get_products = products.objects.filter(price__gte = min_price, price__lte = max_price) 
            except ValueError:
                return redirect("product")
        
            con = {"get_products": get_products, "get_categories": get_categories}
            print({"get_products": get_products})
            return render(request, "product.html", con)
    else:
        return render(request, "login.html")
    
def color_filter(request):
    if 'email' in request.session:
        get_categories = categories.objects.all()
        get_products = products.objects.all()
        color = request.GET.get("color")

        if not color:
            return redirect("product")
        else:
            get_products = products.objects.filter(color=color)
        
        con = {"get_products": get_products, "get_categories": get_categories}
        return render(request, "product.html", con)
    else:
        return render(request, "login.html")
    
def shoping_cart(request):
    return render(request, "shoping_cart.html") 

def login(request):
    return render(request, "login.html")

def signups(request):
    return render(request, "signups.html")

def reset_pass(request):
    return render(request, 'reset_pass.html')

def creates(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key=6089bc4afeb248cfbae263ac6dd99ef8&email={email}")

        try:
            uid = signup.objects.get(email=email)
            message_for_email = "email already exist"
            return render(request,"signups.html",{"message_for_email":message_for_email})
        except:
               if response.status_code == 200:
                    data = response.json()
                    if data["deliverability"] == "DELIVERABLE":
                        if password == c_password:
                            if len(password) >= 8:
                                lower = []
                                uper = []
                                digit = []
                                special = []
                                for i in password:
                                    if i.islower():
                                        lower.append(i)
                                    elif i.isupper():
                                        uper.append(i)
                                    elif i.isdigit():
                                        digit.append(i)
                                    else:
                                        special.append(i)
                                print(lower , uper , digit , special)
                                if len(lower) == 0 or len(uper) == 0 or len(digit) == 0 or len(special) == 0 :
                                    message_for_password_critearia = "please create a strong password !"
                                    return render(request,"signups.html",{"message_for_password_critearia":message_for_password_critearia})
                                else:
                                    signup.objects.create(name=name,email=email,password=password)
                                    messages.success(request,'Registration are successfully completed.')
                                    return redirect("login")
                            else:
                                message_for_password_length = "password length must have 8 character"
                                return render(request,"signups.html",{"message_for_password_length":message_for_password_length})
                        else:
                            message_for_password = "please enter same password"
                            return render(request,"signups.html",{"message_for_password": message_for_password})
                    else:
                        message_for_email_valid = "email are not valid please enter the valid email."  
                        return render(request,'signups.html',{"message_for_email_valid" : message_for_email_valid} ) 

    else:
        return render(request,"signup.html")

def check_login(request):
    if "email" in request.session:
        uid = signup.objects.get(email = request.session['email'])
        return render(request,'index.html')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        try :
            data= signup.objects.get(email=email , password=password)
            request.session['email']=data.email    
            return redirect('index')      
        except:
            massages_for_login = 'invilid user.... :) '
            return render(request, 'login.html', {"massages_for_login" : massages_for_login })

def log_out(request):
    if 'email' in request.session:
        del(request.session['email'])
        return redirect('login')
    else:
        return redirect('login')

def otp(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        
        try:
            uid=signup.objects.get(email=email)
            uid.otp=otp
            uid.save()
            send_mail("Django",f"your OTP is :  {otp} don't share to any one. ","ishanbaraiya21@gmail.com",[email])
            context={"uid":uid,"email":email}
            return render(request,"reset_pass.html",context)
        except:
            print('wordl')
            return render(request,"otp.html")
    else:
        return render(request,"otp.html")

def check_otp(request):
    if request.POST:
        otp = request.POST['otp']
        password = request.POST['password']
        c_password = request.POST['c_password']

        try:
            uid = signup.objects.get(otp=otp)
            if uid.otp == otp:
                if password == c_password:
                    if len(password) >= 8:
                        lower = []
                        uper = []
                        digit = []
                        special = []
                        for i in password:
                            if i.islower():
                                lower.append(i)
                            elif i.isupper():
                                uper.append(i)
                            elif i.isdigit():
                                digit.append(i)
                            else:
                                special.append(i)
                        if len(lower) == 0 or len(uper) == 0 or len(digit) == 0 or len(special) == 0 :
                            message_for_password_critearia = "please create a strong password !"
                            return render(request,"reset_pass.html",{"message_for_password_critearia":message_for_password_critearia})
                        else:
                            uid.password = password
                            uid.otp = None  # Clear the OTP after successful password reset
                            uid.save()
                            messages.success(request, 'Your password has been updated sucessfully. :) ')
                            return redirect('login')
                    else:
                        message_for_password_length = "Password length must be at least 8 characters"
                        return render(request, "reset_pass.html", {"message_for_password_length": message_for_password_length, "otp": otp})
                else:
                    message_for_password = "Passwords do not match"
                    return render(request, "reset_pass.html", {"message_for_password": message_for_password, "otp": otp})
            else:
                message_for_otp = "Invalid OTP"
                return render(request, "reset_pass.html", {"message_for_otp": message_for_otp, "otp": otp})
        except signup.DoesNotExist:
            message_for_email = "Email does not exist"
            return render(request, "reset_pass.html", {"message_for_email": message_for_email, "otp": otp})
    else:
        return render(request, "reset_pass.html")    
