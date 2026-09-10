from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


def home(request):
    return render(request, 'home.html', {})

def send_pdf(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        print("Mobile:", mobile)
        print("Email:", email)

        # PDF location
        pdf_path = "media/pdfs/DHS26_Agenda.pdf"

        mail = EmailMessage(
            subject="DataHack Summit 2026 PDF",
            body=f"""
Hello,

Thank you for your interest in DataHack Summit 2026.

Please find the requested PDF attached.

Regards,
DataHack Summit Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        print("email object created")

        mail.attach_file(pdf_path)

        print("Email file attached and ready to send")

        mail.send()

        print("Email Send Successfully")

        send_mail(
            subject="Good Morning",
            message="Hello Brother how are you",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list = [email],
            fail_silently=False
        )

        print("mail Send")

        return HttpResponse("<h1> Email Send Successfully please see your mail </h1>")

    return redirect("home")



# workshop_detail_link = https://analyticsvepl-my.sharepoint.com/:b:/g/personal/mohammad_asad_analyticsvidhya_com/IQArBZc7QNWlRIH4x3g9O7N-AYUyxkY0O8b0pYBI0jwQ9MI?e=KoZthf
# adenda_detail_link = https://analyticsvepl-my.sharepoint.com/:b:/g/personal/mohammad_asad_analyticsvidhya_com/IQCSV9c6KKm-RrooIsRMt9ndASffEt-5HPcgA7R2f4T--go?e=3nOUgU