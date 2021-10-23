from django.db.models import Q
from django.shortcuts import render,redirect
from .models import*
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def home(request):
    Ds = Destination.objects.all()
    d = {'destination':Ds}
    return render(request,'index.html',d)

def user_sign(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            print("success")
            return redirect('/login/')

    else:
        fm = SignupForm()
    return render(request,'signup.html',{'form':fm})
def user_login(request):
    if not  request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password = upass)
                if user.is_staff:
                    login(request,user)
                    return redirect('/admin_home/')
                elif user is not None:
                    login(request, user)
                    return redirect('/home/')
        else:
            fm = AuthenticationForm()
        return render(request,'login.html',{'form':fm})


def user_logout(request):
    logout(request)
    return redirect('login')

def detail(request,pr_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    dt = Destination.objects.get(id=pr_id)
    if request.method == 'POST':
        date = request.POST['date']
        price = request.POST['price']
        t = request.POST['travel']
        f = request.POST['food']
        user= request.user
        if t==dt.price_by_bus:
            str1="Bus"
        elif t==dt.price_by_Train:
            str1="Train"
        elif t==dt.price_by_Flight:
            str1="Flight"
        if int(f)>0:
            str1=str1+","+"Food"

        book=Booking.objects.create(user=user,destination=dt,Fname = "",Lname = "", Email = "",gender = "",date=date,address="",number="",price=price,used_facility=str1)
        messages.success(request, 'Booking Successfully')
        return redirect('booking',book.id)
    d = {'detail':dt}
    return render(request,'place_detail.html',d)


def destination(request):
    Ds = Destination.objects.all()
    d = {'destination': Ds}
    return render(request,'destination.html',d)

def contact(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        fnam = request.POST['cfname']
        lnam = request.POST['clname']
        em = request.POST['cemail']
        sub = request.POST['csubject']
        msg = request.POST['cmessage']
        user = request.user

        Contact.objects.create(first_Name = fnam,last_Name = lnam, email = em, subject = sub,message = msg,user=user)
        messages.success(request,'Your Message is Succesfully Send !!!')

    return render(request,'contact.html')

def discount(request):
    return render(request,'discount.html')

def booking(request,pr_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    data=Booking.objects.get(id=pr_id)
    if request.method == 'POST':
       if request.method == 'POST':
        bfn = request.POST['bfname']
        bln = request.POST['blname']
        be = request.POST['bemail']
        bg = request.POST['bgender']
        date = request.POST['date']
        add = request.POST['address']
        number = request.POST['number']
        price = request.POST['price']
        used_facility = request.POST['used_facility']
        user= request.user
        data.Fname=bfn
        data.Lname=bln
        data.Email=be
        data.gender=bg
        data.date=date
        data.address=add
        data.number=number
        data.price=price
        data.used_facility=used_facility
        data.user=user
        data.save()
        messages.success(request, 'Booking Update Successfully')
        return redirect('payment')
    d={"data":data}
    return render(request,'booking.html',d)


def about(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')

def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Destination.objects.filter(Q(place__icontains=srch) | Q(country__icontains=srch))
            if match:
                return render(request,'search.html',{'sr':match})
        else:
            return redirect('/home/')
    return render(request,'index.html')


############################################ADMIN---------------Work##########################################

def admin_home(request):
    c=Destination.objects.all().count()
    b=Booking.objects.all().count()
    u=User.objects.filter(is_staff=False).count()
    d={'c':c,'b':b,'u':u}
    return render(request,'admin_home.html',d)

def all_user(request):
    user = User.objects.filter(is_staff=False)
    d = {'user':user}
    return render(request, 'view_user.html', d)

def add_destination(request):
    if request.method == "POST":
        p = request.POST['place']
        c = request.POST['country']
        i = request.FILES['image']
        pb = request.POST['pricebus']
        pt = request.POST['pricetrain']
        pf = request.POST['priceflight']
        fp = request.POST['foodprice']
        np = request.POST['person']
        d = request.POST['days']
        n = request.POST['nights']
        des = request.POST['description']
        obj = Destination.objects.create(price_by_bus=pb,price_by_Train=pt,price_by_Flight=pf,country=c, image=i,food_price=fp,number_of_person=np,days=d,nights=n,place=p,description=des)
        messages.success(request, 'Destination added successfully')
        return redirect('view_destination')
    return render(request, 'add_destination.html')

def delete_user(request, pid):
    user = User.objects.get(id = pid)
    user.delete()
    messages.info(request, 'User deleted successfully')
    return redirect('all_user')

def view_booking(request):
    c=Booking.objects.all()
    d={'c':c}
    return render(request,'view_booking.html',d)

def delete_booking(request,pid):
    data=Booking.objects.get(id=pid)
    data.delete()
    messages.info(request, 'Booking deleted successfully')
    return redirect('view_booking')

def view_destination(request):
    c=Destination.objects.all()
    d={'c':c}
    return render(request,'view_destination.html',d)

def delete_destination(request,pid):
    data=Destination.objects.get(id=pid)
    data.delete()
    messages.info(request, 'Destination deleted successfully')
    return redirect('view_destination')
def my_booking(request):
    data=Booking.objects.filter(user=request.user)
    d={'data':data}
    return render(request,'my_booking.html',d)
def delete_booking(request,pid):
    data=Booking.objects.get(id=pid)
    data.delete()
    messages.info(request, 'Booking deleted successfully')
    return redirect('my_booking')
def Payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        messages.info(request, 'Payment successfully')
        return redirect('my_booking')
    return render(request, 'payment.html')
def edit_destination(request,pid):
    data=Destination.objects.get(id=pid)
    if request.method == "POST":
        p = request.POST['place']
        c = request.POST['country']
        pb = request.POST['pricebus']
        pt = request.POST['pricetrain']
        pf = request.POST['priceflight']
        fp = request.POST['foodprice']
        np = request.POST['person']
        d = request.POST['days']
        n = request.POST['nights']
        des = request.POST['description']
        data.description=des
        data.place=p
        data.country=c
        data.price_by_bus=pb
        data.price_by_Train=pt
        data.price_by_Flight=pf
        data.food_price=fp
        data.number_of_person=np
        data.days=d
        data.nights=n
        data.save()
        try:
            i = request.FILES['image']
            data.image=i
            data.save()
        except:
            pass
        messages.success(request,'Destination Edit successfully')
        return redirect('view_destination')
    d={'data':data}
    return render(request,'edit_destination.html',d)
