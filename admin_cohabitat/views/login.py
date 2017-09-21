from django.shortcuts import render


def login(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
    )
