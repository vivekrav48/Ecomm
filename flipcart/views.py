from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from.serializers import RegSerializer
from rest_framework import viewsets


def index(request):
    if request.method == "POST":
        product_id = request.POST.get("cartid")
        remove = request.POST.get('minus')
        # print("product_id", product_id)
        cart_id = request.session.get('cart')
        # print("cart_id", cart_id)

        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity  <=1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id]=quantity-1
                else:
                    cart_id[product_id] = quantity+1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1

        request.session['cart'] = cart_id
        # print(request.session['cart'])


    # catid =request.GET.get('cat_id')
    # pro_name = request.GET.get('name')

    category_info = Category.objects.all()
    catid = request.GET.get('cat_id')
    search = request.GET.get('search')

    if catid:
        product_info = Product.objects.filter(category=catid)
    elif search:
        product_info = Product.objects.filter(pro_name__icontains=search)
    else:
        product_info = Product.objects.all()


    context = {
        'category': category_info,
        'product': product_info
    }

    return render(request, "home.html", context=context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')




def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')

    

        c_obj = Registration(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = make_password(password),
            mobile = mobile,
            gender = gender
        )

        c_obj.save()
        return redirect('home')
    

def login(request):
    if request.method =="POST":
        email = request.POST.get('emailid')
        password = request.POST.get("password")
        try:
            fetch_email = Registration.objects.get(email = email)
            if check_password(password,fetch_email.password):
                # return HttpResponse("Login successful")
                request.session['name'] = fetch_email.first_name
                request.session['customer_id'] = fetch_email.id
                return redirect('home')
            else:
                return HttpResponse("You have Entered wrong password")
        except:
            return HttpResponse("Email id doesen't exists")
        
def logout(request):
    request.session.clear()
    request.session['cart'] = {}
    return redirect('home')

def cart_details(request):
    # prod_dtls = "please add product"
    # if request.session.get('cart'):
    try:
        error = None
        ids = list(request.session.get('cart').keys())
        prod_dtls = Product.objects.filter(id__in = ids)
    except:
        error = "no product found"
        prod_dtls = None

    return render(request, 'cart.html',{'prod_dtls':prod_dtls, 'error':error})

def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        customer_id = request.session.get('customer_id')
        if not customer_id:
            return HttpResponse("please login first")
        cart = request.session.get('cart')
        product = Product.objects.filter(id__in = list(cart))
        for p in product:
            oreder_info = Order(
                address = address,
                mobile = mobile,
                price = p.price,
                product = p,
                quantity = cart.get(str(p.id)),
                customer = Registration(id=customer_id),
            )
            oreder_info.save()
        request.session.cart = {}
        return redirect('order')
    
def Order_dtls(request):
    ord_dtls = Order.objects.all()
    tp = 0
    for t in ord_dtls:
        tp = tp + (t.price*t.quantity)
    return render(request, 'order.html', {'ord_dtls':ord_dtls, 'tp':tp})


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegSerializer


