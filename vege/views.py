from django.shortcuts import render ,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login

# Create your views here.
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description  = data.get('recipe_description')

        Recipes.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        return redirect('/recipes/')
    query_set = Recipes.objects.all()
    if request.GET.get('search'):
        
        query_set = query_set.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': query_set}
    return render(request, 'recipes.html', context)

def delete_recipe(request, id):
    query_set = Recipes.objects.get(id = id)
    query_set.delete()
    return redirect('/recipes/')

def update_recipe(request, id):
    query_set = Recipes.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        query_set.recipe_name = recipe_name 
        query_set.recipe_description = recipe_description

        if recipe_image:
            query_set.recipe_image = recipe_image

        query_set.save()
        return redirect('/recipes/')

    context = {'recipe': query_set}
    return render(request, 'update_recipes.html', context)

def login_page(request): 
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
                messages.error(request, 'invalid user name')
                return redirect('/login/')
        user = authenticate(username = username , password = password)
        if user is None:
            messages.error(request, 'invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
        
    return render(request,'login.html')

def logout_page(request):
    User(request)
    return redirect("/login/")


def register_page(request):
    if request.method == 'POST':
     
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User already exists')
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')
        return redirect('/register/')

    return render(request, 'register.html')