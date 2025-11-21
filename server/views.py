import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# --------------------
#   REGISTER
# --------------------
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })

    return Response(serializer.errors, status=400)


# --------------------
#   LOGIN
# --------------------
@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if not user:
        return Response({"error": "Credenciales incorrectas"}, status=400)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "user": UserSerializer(user).data
    })


# --------------------
#   CREATE CHECKOUT SESSION (Stripe)
# --------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):

    session = stripe.checkout.Session.create(
        mode="payment",  # ← YA NO ES SUBSCRIPTION
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Pago Premium"  # Nombre que verá el usuario en Stripe
                },
                "unit_amount": 1000,  # precio en centavos → 1000 = $10.00 USD
            },
            "quantity": 1
        }],
        metadata={
            "user_id": request.user.id
        },
        success_url="https://tu-frontend.com/success",
        cancel_url="https://tu-frontend.com/cancel"
    )

    return Response({"checkout_url": session.url})


# --------------------
#   WEBHOOK STRIPE
# --------------------
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]

        user = User.objects.filter(id=user_id).first()
        if user:
            user.is_premium = True
            user.stripe_subscription_status = "active"
            user.save()

    return Response({"status": "success"})



@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def anda(request):
    return Response({"message": "Anda piola"})