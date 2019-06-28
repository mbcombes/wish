from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Wish
from datetime import datetime
import bcrypt

def index(request):     # GET /
    return render(request, 'wish/index.html')

def create(request):    # POST /create
    # to check if there are errors.
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['username']=new_user.first_name
        request.session['id']=new_user.id
        print("this is the submit path")
        print(new_user)
        return redirect('/dashboard')

def login(request):    # POST /login
    # to check if there are errors.
    print(request.POST['email'])
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        user=User.objects.get(email=request.POST['email'])
        request.session['username']=user.first_name
        request.session['id']=user.id
    return redirect('/dashboard')

def dashboard(request):   # GET /dashboard
    if 'id' in request.session:
        user_wish=Wish.objects.filter(wisher=User.objects.get(id=request.session['id']))
        granted_wishes_liked=Wish.objects.filter(liker=User.objects.get(id=request.session['id']))
        granted_wishes_unliked=Wish.objects.filter(granted=True).exclude(liker=User.objects.get(id=request.session['id']))
        context={
            "user_wish": user_wish,
            'granted_wishes_liked': granted_wishes_liked,
            'granted_wishes_unliked': granted_wishes_unliked,
        }
        return render(request, 'wish/dashboard.html', context)
    else:
        messages.error(request, 'Please Log In.', extra_tags='fail')
        return redirect('/')

def destroy(request):  # /destroy
    del request.session['username']
    del request.session['id']
    print('session cleared')
    return redirect('/')

def newwish(request): # /wish/new
    return render(request, 'wish/new.html')

def create_wish(request): # /wishes/create
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/wishes/new')
    elif request.method == "POST":
        Wish.objects.create(item=request.POST['item'], description=request.POST['description'], wisher=User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def edit_wish(request, id): # /wishes/<id>/edit
    this_wish=Wish.objects.get(id=id)
    context={
        'this_wish': this_wish
    }
    return render(request, 'wish/edit.html', context)

def update_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect(f"/wishes/{request.POST['wishid']}/edit")
    elif request.method == 'POST':
        this_wish=Wish.objects.get(id=request.POST['wishid'])
        this_wish.item=request.POST['item']
        this_wish.description=request.POST['description']
        this_wish.save()
        print("wish was updated")
    return redirect('/dashboard')

def destroy_wish(request, id):
    this_wish=Wish.objects.get(id=id)
    this_wish.delete()
    return redirect('/dashboard')

def wish_granted(request, id):
    this_wish=Wish.objects.get(id=id)
    this_wish.granted=True
    this_wish.date_granted=datetime.now()
    this_wish.save()
    print("this wish was granted")
    return redirect('/dashboard')

def wish_like(request, id):
    this_wish=Wish.objects.get(id=id)
    this_wish.likes=this_wish.likes+1
    this_wish.save()
    this_user=User.objects.get(id=request.session['id'])
    this_wish.liker.add(this_user)
    print("this wish was liked")
    return redirect('/dashboard')

def stats(request):
    total_granted=Wish.objects.filter(granted=True).count()
    my_granted=Wish.objects.filter(granted=True, wisher=User.objects.get(id=request.session['id'])).count()
    my_pending=Wish.objects.filter(granted=False, wisher=User.objects.get(id=request.session['id'])).count()
    context={
        'total_granted': total_granted,
        'my_granted': my_granted,
        "my_pending": my_pending,
    }
    return render(request, 'wish/stats.html', context)

