from django.core.mail import EmailMessage
from django.shortcuts import render
import os
import logging

from sendgrid import sendgrid
from sendgrid.helpers.mail import *


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
    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

        contact_name = request.POST.get('nome')
        from_email = Email(request.POST.get('email'))
        to_email = Email("contato@cohabitat.com.br")
        contact_phone = request.POST.get('telefone')
        message = request.POST.get('mensagem')
        subject = "Novo Contato"
        body = " Nome do contato: " + contact_name + " \n" + " Telefone: " + contact_phone + "\n" + " Email: " + from_email.__str__() + " \n" + "Mensagem: " + message
        content = Content("text/plain", body)

        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        logger.debug(response.status_code)
        logger.debug(response.body)
        logger.debug(response.headers)


    return render(request, 'sobre.html')
