from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="login/")
def home(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'menu.html',
    )
