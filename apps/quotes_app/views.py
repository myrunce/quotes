# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'quotes_app/index.html')

def process(request):
    errors = User.objects.validation(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        found_users = User.objects.filter(email = request.POST['email'])
        if found_users.count() > 0:
            messages.error(request, 'Email already taken', extra_tags='email')
            return redirect('/')
        else:
            passwordDB = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            created_user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'] , email = request.POST['email'], password = passwordDB, birthday = request.POST['birthday'])
            request.session['user_id'] = created_user.id 
            request.session['user_name'] = created_user.name
            return redirect('/quotes')

def login(request):
    found_users = User.objects.filter(email = request.POST['email'])
    if found_users.count() > 0:
        found_user = found_users.first()
        if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
            request.session['user_id'] = found_user.id 
            request.session['user_name'] = found_user.name
            return redirect('/quotes') 
        else:
            messages.error(request, 'Login Failed', extra_tags='fail')
            return redirect('/')
    else:
        messages.error(request, 'Login Failed', extra_tags='fail')
        return redirect('/')

def quotes(request):
    the_user = User.objects.get(id = request.session['user_id'])
    context = {
        'quotes': Quote.objects.exclude(id__in=[elem.quote.id for elem in Favorite.objects.all()]),
        'favorites': Favorite.objects.filter(user = the_user) 
    }
    return render(request, 'quotes_app/quotes.html', context)

def contribute(request):
    errors = Quote.objects.validation(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/quotes')
    else:
        the_user = User.objects.get(id = request.session['user_id'])
        new_quote = Quote.objects.create(quoted_by = request.POST['quoted_by'], desc = request.POST['quote'], user = the_user )
        return redirect('/quotes')

def favorite(request):
    the_user = User.objects.get(id = request.session['user_id'])
    the_quote = Quote.objects.get(id = request.POST['quote_id'])
    new_favorite = Favorite.objects.create(user = the_user, quote = the_quote)
    return redirect('/quotes')

def users(request, user_id):
    the_user = User.objects.get(id = user_id)
    the_count = Quote.objects.filter(user = user_id).count()
    context = {
        'the_user': User.objects.get(id = user_id),
        'the_quotes': Quote.objects.filter(user = the_user),
        'the_count': the_count
    }
    return render(request, 'quotes_app/users.html', context)

def logout(request):
    del request.session['user_id']
    del request.session['user_name']
    messages.error(request, 'Logout Successful', extra_tags='Logout')
    return redirect ('/')

def remove(request):
    Favorite.objects.get(id = request.POST['favorite_id']).delete()
    return redirect('/quotes')