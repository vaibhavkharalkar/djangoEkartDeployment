from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,Cart,Order
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail

# Create your views here.
def product(request):
    
    p=Product.objects.filter(is_active=True)
    context={'data':p}
    # print(p)
    return render(request,'index.html',context)

def register(request):
    context={}
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        un=request.POST['uname']
        email=request.POST['email']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        '''
        print(un)
        print(email)
        print(p)
        print(cp)'''

        if un==""or email=="" or p=="" or cp=="":
           # print("Field can not be empty.!")
            context['errmsg'] = "Field can not be empty.!"
            return render(request,"register.html",context)
        elif p!=cp:
           # print("Password & comform password didn't match")
            context['errmsg'] = "Password & comform password didn't match"
            return render(request,"register.html",context)
        elif len(p)<8:
           # print("Password must be atleast 8 Characters")
            context['errmsg'] = "Password must be atleast 8 Characters"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(username=un,email=email,password=p)
                u.set_password(p)
                u.save()
                context['success'] = "!User Create Successfully."
                return render(request,"register.html",context)
            except Exception:
                context["errmsg"]="User already exist.. please try another name..!!"
                return render(request,"register.html",context)

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else: 
        un = request.POST['uname']
        p = request.POST['upass']

       # print(un)
        #print(p)
        u=authenticate(username=un,password=p)
        #print(u)

        if u is not None:
            login(request,u)
            return redirect('/product')
        else:
            context={}
            context['errmsg'] = "Invalid username and password"
            return render(request,'login.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/product')

def catfilter(request,cid):
    q1=Q(cat=cid)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)
def sortfilter(request,sv):
    if sv=='1':
        p=Product.objects.order_by('-price')
    else:
        p=Product.objects.order_by('price')

    context={}
    context['data']=p
    return render(request,'index.html',context)

def pricefilter(request):
    min=request.GET['min']
    max=request.GET['max']
    #print(min)
    #print(max)
    q1=Q(price__gte=min) 
    q2=Q(price__lte=max) 
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def search(request):
    s=request.GET['search']
    pname=Product.objects.filter(name__icontains=s)
    pdet=Product.objects.filter(pdetail__icontains=s)
    pcat=Product.objects.filter(cat__icontains=s)

    allprod=pname.union(pcat,pdet)
    context={}
    if allprod.count()==0:
        context['errmsg']='Product Not Found'
        return render(request,'index.html',context)
    else:
        context['data']=allprod
        return render(request,'index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context = {}
    context['data'] = p
    return render(request,'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        #uid=request.user.id
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['data']=p
        if n==1:
            context['errmsg'] = "Product already exist in cart"
            return render(request,'product_details.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']= "Product added successfully"
            return render(request,'product_details.html',context)
    else:
        return redirect('/login')
         
def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    sum=0
    for i in  c:
        sum=sum+i.pid.price*i.qty

    context={}
    context['data']=c 
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1


    c.update(qty=q)
    return redirect('/viewcart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        amount=i.pid.price*i.qty
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=amount)
        o.save()
        i.delete()

        return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    for i in o:
        sum=sum+i.amt

    context={}
    context['data']=o
    context['total']=sum
    context['n']=len(o)
    return render(request,'placeorder.html',context)


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_hAdtc6mIaDYF1i", "T6wZ2ZZiyqRGnXXmn0Q5Kvr9"))
    oid=random.randrange(1000,9999)
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    for i in o:
        sum=sum+i.amt

    data = { "amount": sum*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['payment']=payment
   # return HttpRespons ("Success")
    return render(request,'pay.html',context)

def paymentsuccess(request):
    sub="ISB416 Order Status"
    msg="Thanks for shopping...!!"
    frm='vaibhavkharalkar01@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'paymentsuccess.html')
    
def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request,'about.html')


    