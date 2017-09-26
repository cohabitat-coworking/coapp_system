from django.shortcuts import render


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
    )


def planos(request):
    return render(request, 'planos.html')


def sobre(request):
    return render(request, 'sobre.html')
