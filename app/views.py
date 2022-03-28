from cProfile import Profile
from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .views_accounts import *
from .models import *

# manager
@login_required
def dashboard_view(request):
    profile_pic_url=[]
    try:
        profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    except:
        profile_pic_url =[]
    product =Product.objects.all().order_by('-date_added')
    chefs =User.objects.filter(is_staff=False)
    categories=Category.objects.all()
    headchef_username='suravi'
    headchef=[]
    fruits=[]
    veggies=[]
    try:
        headchef=ProfilePic.objects.get(user=User.objects.get(username=headchef_username))
    except:
        headchef=[]
    try:
        fruits =product.filter(category=Category.objects.get(name__iexact='fruit'))
    except:
        fruits =[]
    try:
        veggies =product.filter(category=Category.objects.get(name__iexact='veggies'))
    except:
        veggies =[]
    context={
        "product": product,
        "products_count":len(product),
        "chefs":chefs,
        'headchef':headchef,
        "chefs_count":len(chefs),
        "fruits":fruits,
        "fruits_count":len(fruits),
        "veggies":veggies,
        "veggies_count":len(veggies),
        "categories_count":len(categories),
        "dashboard_active":True,
        "profile_pic":profile_pic_url
    }
    return render(request, 'dashboard.html', context)

@login_required
def dashboard_profile_view(request):
    user = User.objects.get(username=request.user)
    profile =[]
    try:
        profile =ProfilePic.objects.get(user=user)
    except:
        profile =[]
    print(profile)
    if request.method == 'POST':
        instance = get_object_or_404(ProfilePic, user=request.user)
        form = ProfilePicForm(request.POST or None, request.FILES, instance=instance)
        if form.is_valid():
            profile_form = form.save(commit=False)
            profile_form.user = User.objects.get(username=request.user)
            profile_form = profile_form.save()
            form.save()
            return redirect('dashboard_profile_view')
    else:
        form = ProfilePicForm()
    context={
        "profile_pic":profile,
        "user":user,
        "form":form,
        "dashboard_active":True,
    }
    return render(request, 'profile.html', context)

@login_required
def supplies_view(request):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    product =Product.objects.all()
    if request.method == 'POST':
        try:
            product = product.filter(name__icontains=request.POST['search_product'])
        except:
            pass
    context={
        "product": product,
        "supplies_active":True,
        "profile_pic":profile_pic_url,
    }
    return render(request, 'supplies.html', context)

@login_required
def supplies_use_view(request, id):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    product =Product.objects.filter(id=id)
    product_detail =Product.objects.get(id=id)
    error=''
    if request.method =='POST':
        quantity = request.POST['quantity']
        try:
            final_quantity =(int(product_detail.quantity)-int(quantity))
            if final_quantity<0:
                error='Quantity selected exceeds the amount in database.'
            else:
                product.update(quantity=final_quantity)
                History.objects.create(content=f"{request.user.first_name} used {quantity} {product_detail.name} from category of {product_detail.category.name}")
                if not product_detail.quantity <= product_detail.notify_quantity:
                    if final_quantity < (product_detail.notify_quantity+1):
                        Notification.objects.create(content=f"{product_detail.name} is going to reach its minimum limit in {product_detail.notify_by}")
                return redirect('supplies_use_view', product_detail.id)
        except:
            error='Enter product quantity before submitting.'
    context={
        "product": product_detail,
        "supplies_active":True,
        "profile_pic":profile_pic_url,
        "error":error,
    }
    return render(request, 'supplies_detail.html', context)

@login_required
def chefs_view(request):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    chefs =User.objects.filter(is_staff=False)
    first_name = ''
    last_name = ''
    username = ''
    email = ''
    error=''
    if request.method == 'POST':
        first_name = request.POST['first_name'].strip().capitalize()
        last_name = request.POST['last_name'].strip().capitalize()
        email = request.POST['email'].lower()
        username = request.POST['username'].strip().lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if first_name == '':
            error = "First name is required."
        elif last_name == '':
            error = "Last name is required."
        elif email == '':
            error = "Email address is required."
        elif username == '':
            error = "Username is required."
        else:
            try:
                user = User.objects.get(username=username)
                error = 'Username already exists'
            except:
                try:
                    user = User.objects.get(email=email)
                    error = 'Email address already exists.'
                except:
                    result = password_check(password1, password2)
                    if result == '':
                        error = ''
                        user = User.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,email=email,
                            password=password1,
                            is_active=True,
                            is_staff=False,
                            )
                        ProfilePic.objects.create(user=user)
                    else:
                        error = result
    context={
        "chefs":chefs,
        "profile_pic":profile_pic_url,
        "chefs_active":True,
        'error': error,
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
    }
    return render(request, 'chefs.html', context)


@login_required
def chefs_detail_view(request, id):
    profile_pic=''
    try:
        profile_pic =ProfilePic.objects.get(user__id = id)
    except:
        profile_pic=''
    context={
        "chef":User.objects.get(id=id),
        "profile_pic":profile_pic,
        "chefs_active":True,
    }
    return render(request, 'chefs_detail.html', context)

def notifications_view(request):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    context={
        "notifications_active":True,
        "profile_pic":profile_pic_url,
        "notifications":Notification.objects.all().order_by('-id'),
    }
    return render(request, 'notifications.html', context)

@login_required
def history_view(request):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    context={
        "history":History.objects.all().order_by('-id'),
        "profile_pic":profile_pic_url,
        "history_active":True,
    }
    return render(request, 'history.html', context)


@login_required
def inventory_view(request):
    profile_pic_url =ProfilePic.objects.get(user=User.objects.get(username=request.user))
    product = Product.objects.all()
    total_inventory_size=0
    total_quantity=0
    total_inventory_available=0
    for i in product:
        total_inventory_size = total_inventory_size+ i.inventory_size
        total_quantity = total_quantity + i.quantity
        total_inventory_available =total_inventory_available+(i.inventory_size-i.quantity)
    context={
        "profile_pic":profile_pic_url,
        "inventory_active":True,
        "product":product,
        "total_inventory_size":total_inventory_size,
        "total_quantity":total_quantity,
        "total_inventory_available":total_inventory_available,
    }
    return render(request, 'inventory.html', context)

@login_required
def chef_dashboard_view(request):
    context={
    }
    return HttpResponse('Done')