from django.shortcuts import render
from . forms import ContactForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.


def portfolio_home(request):

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            message = "from: " + email + "\n\n" + message

            # Process Email send
            try:
                send_mail(subject, message, email, ['elvismulowayi@gmail.com'])
                logger.info(f"Email sent: Subject={subject}, From={email}, To=elvismulowayi@gmail.com")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                return HttpResponse(f'Error: {e}')
            return render(request, 'index/email_sender.html', {
                'email': email,
                'subject': subject,
                'message': message,
                'is_superuser': request.user.is_superuser})

    # Else Present empty form to user
    else:
        form = ContactForm()
        

    return render(request, 'index/portfolio.html', {'form': form})
