from django.shortcuts import render, redirect, HttpResponse
from . import models
from .models import Login, Item
import bcrypt
from django.contrib import messages
import re
from django.contrib.messages import get_messages
NAME_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z]+$')

def index(request):
    return render(request, 'testapp/index.html')

def add_user(request):
    post = request.POST
    validation = True

    if len(post['first_name']) < 3:
        messages.add_message(request, messages.ERROR, 'First Name Field Must Be At Least 3 Characters Long!')
        validation = False
    elif not NAME_REGEX.match(post['first_name']):
        messages.add_message(request, messages.ERROR, 'First Name Must Contain Only Letters!')
        validation = False

    if len(post['last_name']) < 3:
        messages.add_message(request, messages.ERROR, 'Last Name Field Must Be At Least 3 Characters Long!')
        validation = False
    elif not NAME_REGEX.match(post['last_name']):
        messages.add_message(request, messages.ERROR, 'Last Name Must Contain Only Letters!')
        validation = False

    if len(post['password']) < 8:
        messages.add_message(request, messages.ERROR, 'Password Must Be At Least 8 Characters!')
        validation = False

    if post['password'] != post['pass_confirm']:
        messages.add_message(request, messages.ERROR, 'Your Passwords Did Not Match!')
        validation = False

    if post['username'] < 4:
        messages.add_message(request, messages.ERROR, 'Your Username Must Be At Least 3 Characters!')
        validation = False

    if models.Login.objects.all() and validation:
        check = models.Login.objects.filter(username=post['username'])
        if check:
            if post['username'] == check[0].username:
                messages.add_message(request, messages.ERROR, 'Username Is Invalid!')
                validation = False

    if validation:
        password = post['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Login.objects.create(first_name=post['first_name'], last_name=post['last_name'], username=post['username'], password=hashed)
    return redirect('/')

def verify_user(request):
    validation = True
    passcheck = request.POST['logcheckpass']
    check = False
    if models.Login.objects.all():
        check = models.Login.objects.filter(username=request.POST['username'])
    else:
        messages.add_message(request, messages.ERROR, 'There Are No Users in the Database!')
        validation = False
    if check:
        if check[0].password == bcrypt.hashpw(passcheck.encode('utf-8'), check[0].password.encode('utf-8')):
            request.session['loggeduser'] = check[0].id
        else:
            messages.add_message(request, messages.ERROR, 'Your Password is Incorrect!')
            validation = False
    else:
        messages.add_message(request, messages.ERROR, 'This username Does Not Exist In the Database!')
        validation = False
    if validation:
        return redirect('/home')
    else:
        return redirect('/')

def homepage(request):
    logged = models.Login.objects.filter(id=request.session['loggeduser'])
    mystuff = models.Item.objects.filter(login=logged)
    otherstuff = models.Item.objects.exclude(login=logged)
    content = {
                'mystuff' : mystuff,
                'otherstuff' : otherstuff,
                'user' : logged[0]
    }
    return render(request, 'testapp/success.html', content)

def add_item(request):
    user = models.Login.objects.filter(id=request.session['loggeduser'])
    content = {
                'user' : user[0]
    }
    return render(request, 'testapp/create.html', content)

def add_item_now(request):
    post = request.POST
    if len(post['item_name']) < 1:
        messages.add_message(request, messages.ERROR, 'Item field not be empty!')
        return redirect('/additem')
    elif len(post['item_name']) < 4:
        messages.add_message(request, messages.ERROR, 'Item field must be more than 3 characters long!')
        return redirect('/additem')
    people = Login.objects.filter(id=request.session['loggeduser'])
    person = people[0]
    items = Item.objects.filter(item_name=post['item_name'])
    if items:
        messages.add_message(request, messages.ERROR, 'This item has already been created!')
        print "WHY?!"
        return redirect('/additem')
    else:
        item = Item.objects.create(item_name=post['item_name'])
    print "WHY?!"
    item.login.add(person)
    print "WHY?!"
    return redirect('/home')

def delete_item(request, string):
    Item.objects.filter(item_name=string).delete()
    return redirect('/home')
