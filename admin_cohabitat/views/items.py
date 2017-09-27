from django.shortcuts import render


def itens(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'itens.html',
    )
