from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django. contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


import json
import datetime
from .models import *

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order={'ger_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)

def products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order={'ger_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request,'store/all_products.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order={'ger_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']


    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order={'ger_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

from django.views.decorators.csrf import csrf_exempt

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action:',action)
    print('productId:',productId)


    customer=request.user.customer
    product= Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_td=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_td

        if total==order.get_cart_total:
            order.complete=True
        order.save()

        # if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    # else:
    #     print("User is not logged in")
    return JsonResponse('Payment complete!',safe=False)

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save();
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'store/register.html',{'form':form})

@login_required
def profile(request):
    Customer.objects.get_or_create(user=request.user)
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.customer)

    context={
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request,'store/profile.html',context)

class PostDetailView(DetailView):
    model = Product

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name','price','image','description']

    success_url = ''
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/')
    
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Product
    fields = ['name','price','image']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product
    success_url= '/'

    def test_func(self):
        return True