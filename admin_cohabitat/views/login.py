<<<<<<< HEAD
from django.shortcuts import render


def login(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
    )
=======
from django.shortcuts import render


def login(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'registration/login.html',
    )
>>>>>>> b7dbd304e55ba402e2a7130abf0e95403d58b581
