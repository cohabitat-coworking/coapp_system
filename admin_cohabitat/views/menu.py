from django.shortcuts import render


def menu(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'menu.html',
    )
