from django.shortcuts import render


def resources(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'recursos.html',
    )
