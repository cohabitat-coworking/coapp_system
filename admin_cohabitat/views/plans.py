from django.shortcuts import render


def plans(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'planos.html',
    )