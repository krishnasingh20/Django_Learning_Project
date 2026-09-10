from django.shortcuts import render
from django.http import JsonResponse, response, FileResponse, Http404, HttpResponse
from .models import *
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .tasks import send_agenda_email, send_workshop_email
import razorpay
import json


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def home(request):
    speaker = Speaker.objects.all()[:10]
    session = Session.objects.all()[:5]
    workshop = Workshop.objects.all()
    sponsor = Sponsor.objects.all()
    return render(request, 'dhs26/home.html', {
        "speakers":speaker,
        "sessions":session,
        "workshops":workshop,
        "sponsors":sponsor,
    })


def speakers(request):
    speaker = Speaker.objects.all()
    return render(request, 'dhs26/speakers.html', {
        "speakers":speaker,
    })


def speaker_detail(request, id):
    s = Speaker.objects.get(id=id)
    return render(request, 'dhs26/speaker_detail.html', {
        "speaker":s
    })


def sponsors(request):

    sponsor = Sponsor.objects.all()

    group = {}
    for s in sponsor:
        group.setdefault(s.type, []).append(s)

    group = dict(sorted(group.items(), key=lambda item: len(item[1])))

    return render(request, 'dhs26/sponsors.html', {"sponsors":group})



def sponsor_detail(request, id):
    s = Sponsor.objects.get(id=id)
    return render(request, 'dhs26/sponsor_detail.html', {"sponsor":s})



def sessions(request):
    session = Session.objects.all()
    return render(request, "dhs26/sessions.html", {"sessions":session})



def session_detail(request, id):
    s = Session.objects.get(id=id)
    return render(request, "dhs26/session_detail.html", {"session": s})



def workshop_detail(request, id):
    w = Workshop.objects.get(id=id)
    return render(request, "dhs26/workshop_detail.html", {
        "workshop":w
    })



def awards(request):
    jury = Jury.objects.all()
    return render(request, 'dhs26/awards.html', {
        "jury": jury,
    })



def download_file(request):
    file_path = Path(settings.BASE_DIR) / "downloads" / "DHS26_Agenda.pdf"

    if(not file_path.is_file()):
        raise Http404("File Not Found")
    
    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=file_path.name
    )



@csrf_exempt
def send_workshop_detail(request):
    if(request.method == "POST"):
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        DownloadDetail.objects.create(phone=phone, email=email)

        send_workshop_email.delay(email)

        return JsonResponse({"message":"Workshop detail send on mail"})



@csrf_exempt
def emailAgenda(request):
    if(request.method == "POST"):
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        DownloadDetail.objects.create(phone=phone, email=email)

        send_agenda_email.delay(email)

        return JsonResponse({"message":"Agenda Detail send on mail"})


def buy_workshop(request, id):
    workshop = Workshop.objects.get(id=id)
    return render(request, 'dhs26/buy_workshop.html', {
        "workshop": workshop,
    })


def checkout_conference(request):
    return render(request, 'dhs26/checkout_conference.html', {})


def checkout_conference_workshop(request):
    workshops = Workshop.objects.all()

    preselected_id = None
    id = request.GET.get('workshop')
    if id:
        try:
            preselected_id = int(id)
        except ValueError:
            preselected_id = None

    return render(request, 'dhs26/checkout_conference_workshop.html', {
        "workshops": workshops,
        "preselected_id": preselected_id,
    })

@csrf_exempt
def create_order(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        workshop_id = request.POST.get("workshop_id")

        workshop = Workshop.objects.get(id=workshop_id)

        amount = workshop.final_price

        razorpay_order = razorpay_client.order.create({
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": 0
        })

        Payment.objects.create(
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            payment_type="Workshop",
            status="Created"
        )

        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "amount": int(amount * 100),
            "order_id": razorpay_order["id"]
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=400)

@csrf_exempt
def create_order_conference(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=400
        )

    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")

        amount = 21999

        razorpay_order = razorpay_client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": 0
        })

        Payment.objects.create(
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            payment_type="Conference",
            status="Created"
        )

        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "amount": amount * 100,
            "order_id": razorpay_order["id"]
        })

    except Exception as e:

        return JsonResponse({
            "error": "Unable to create payment order"
        }, status=400)


@csrf_exempt
def create_order_workshop(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=400
        )

    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")

        workshop_ids = request.POST.getlist("workshops")

        if not workshop_ids:
            return JsonResponse(
                {"error": "Please select at least one workshop"},
                status=400
            )

        workshops = Workshop.objects.filter(
            id__in=workshop_ids,
            is_sold_out=False
        )

        if workshops.count() != len(set(workshop_ids)):
            return JsonResponse(
                {"error": "One or more selected workshops are unavailable"},
                status=400
            )

        total_amount = sum(
            workshop.final_price for workshop in workshops
        )

        razorpay_order = razorpay_client.order.create({
            "amount": int(total_amount * 100),
            "currency": "INR",
            "payment_capture": 0
        })

        payment = Payment.objects.create(
            razorpay_order_id=razorpay_order["id"],
            amount=total_amount,
            status="Created"
        )

        payment.workshops.set(workshops)

        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "amount": int(total_amount * 100),
            "order_id": razorpay_order["id"]
        })

    except Exception as e:

        return JsonResponse(
            {"error": "Unable to create payment order"},
            status=400
        )

@csrf_exempt
def handlePayment(request):

    if request.method != "POST":
        return JsonResponse({"status": "failed"}, status=400)

    try:
        data = json.loads(request.body)

        payment_id = data["razorpay_payment_id"]
        order_id = data["razorpay_order_id"]
        signature = data["razorpay_signature"]

        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

        payment = Payment.objects.get(
            razorpay_order_id=order_id
        )

        razorpay_client.payment.capture(
            payment_id,
            int(payment.amount * 100)
        )

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "Success"
        payment.save()

        return JsonResponse({
            "status": "success"
        })

    except razorpay.errors.SignatureVerificationError:

        Payment.objects.filter(
            razorpay_order_id=order_id
        ).update(status="Failed")

        return JsonResponse({
            "status": "failed"
        })

    except Exception as e:

        return JsonResponse({
            "status": "failed"
        }, status=400)