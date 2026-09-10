from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from .models import *
from django.http import HttpResponseBadRequest, JsonResponse
import json



# initializing razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def home(request):
    return render(request, 'home.html')

def create_order(request):
    if(request.method == 'POST'):
        amount = int(request.POST.get('amount'))
        currency = "INR"

        # creating razorpay order 
        razorpay_order = razorpay_client.order.create(
            dict(amount=amount*100, currency=currency, payment_capture=0)
        )

        Payment.objects.create(
            razorpay_order_id=razorpay_order['id'],
            amount = amount,
            status = "Created"
        )

        context = {
            'razorpay_order_id':razorpay_order['id'],
            'razorpay_merchant_key':settings.RAZORPAY_KEY_ID,
            'razorpay_amount':amount*100,
            'currency':currency,
            'amount':amount
        }

        return render(request, 'checkout.html', context)
    return redirect('home')


@csrf_exempt
def handlePayment(request):

    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id', '')
            razorpay_order_id = data.get('razorpay_order_id', '')
            signature = data.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            razorpay_client.utility.verify_payment_signature(params_dict)

            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            capture_amount = int(payment.amount)*100

            razorpay_client.payment.capture(payment_id, capture_amount)

            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()

            return JsonResponse({"status":"success"})
        except razorpay.errors.SignatureVerificationError:
            Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(status="Failed")
            return JsonResponse({"status":"failed"})
        except Exception as e:
            print("PAYMENT ERROR: ", repr(e))
            return HttpResponseBadRequest(f"Payment Processing Error: {str(e)}")

    else:
        return HttpResponseBadRequest("Invalid Request Method")