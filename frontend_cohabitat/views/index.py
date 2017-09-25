from django.core.mail import EmailMessage
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


def send_email(request):
    if request.method == 'POST':
        contact_name = request.POST.get('nome')
        contact_email = request.POST.get('email')
        contact_phone = request.POST.get('telefone')
        message = request.POST.get('mensagem')

        body = " Nome do contato: " + contact_name + " \n" + " Telefone: " + contact_phone + "\n" + " Email: " + contact_email + " \n" + "Mensagem: " + message

        email = EmailMessage(
            subject='Novo Contato',
            body=body,
            from_email=contact_email,
            to=['contato@cohabitat.com.br', ],
            headers={'Reply-To': contact_email, 'Content-Type': 'text/plain'},

        )

        email.send(fail_silently=False)

    return render(request, 'sobre.html')
