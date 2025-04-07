from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RegisterSerializer, ProductSerializer, LoginSerializer
from .models import Product
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import PaymentProof
from .serializers import PaymentProofSerializer
import urllib.parse
from django.conf import settings
from django.http import JsonResponse
from .models import ContactMessage
from django.views.decorators.csrf import csrf_exempt
import json



User = get_user_model()

# ✅ Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            full_name = f"{user.first_name} {user.last_name}".strip()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "full_name": full_name,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Login View (JWT Authentication)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

# ✅ Product ViewSet (Public products for homepage)
class FarmerProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Filter products to only show those marked as "pending"
        return Product.objects.filter(status="pending")

# ✅ Farmer Product Management ViewSet (Authenticated user only)
class FarmerProductManagementViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users
    parser_classes = (MultiPartParser, FormParser)  # Add support for file uploads

    def get_queryset(self):
        # Only allow a farmer to access their own products
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the product owner
        serializer.save(user=self.request.user)

# ✅ Dashboard View (Authenticated user only)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class FarmerDashboardViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        products = Product.objects.filter(user=user)

        # Prepare the dashboard data
        dashboard_data = {
            "message": f"Welcome {user.first_name} {user.last_name} to your dashboard!",
            "email": user.email,
            "total_products": products.count(),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "image_url": request.build_absolute_uri(p.image.url) if p.image else None  # Ensure absolute URL
                }
                for p in products
            ],
        }

        return Response(dashboard_data, status=status.HTTP_200_OK)

# ✅ Product Upload View (Authenticated user only)
class ProductUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Support file uploads

    def post(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        # Use the ProductSerializer to validate the incoming data (including image)
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            print("Serializer is valid:", serializer.validated_data)  # Debugging validated data
            product = serializer.save(user=request.user)  # Automatically assign the logged-in user
            return Response({"message": "Product uploaded successfully!", "product": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditProductView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, user=request.user)
        except Product.DoesNotExist:
            return Response({"message": "Product not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully!", "product": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentProofUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        # Step 1: Validate the incoming data using PaymentProofSerializer
        serializer = PaymentProofSerializer(data=request.data)
        if serializer.is_valid():
            # Step 2: Save PaymentProof object to the database
            payment_proof = serializer.save()

            # Step 3: Prepare the WhatsApp message
            # Get the URL of the uploaded file (proof file)
            file_url = request.build_absolute_uri(payment_proof.proof_file.url)  # Generate full URL for the file

            # Create the WhatsApp message with order summary and file link
            message = (
                f"Hello, this is {payment_proof.customer_name}.\n\n"
                f"Order Summary:\n{payment_proof.order_summary}\n\n"
                f"Proof of payment: {file_url}"
            )

            # Step 4: URL encode the message
            encoded_message = urllib.parse.quote(message)

            # Step 5: Construct the WhatsApp link with the encoded message
            whatsapp_number = '2349012345678'  # Replace with your WhatsApp Business number
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

            # Step 6: Return the response with the WhatsApp link
            return Response(
                {
                    "message": "Payment proof submitted successfully.",
                    "whatsapp_url": whatsapp_url  # Send the WhatsApp link to the frontend
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   # ✅ Contact View (Public form handler)

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            if not name or not email or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            return JsonResponse({"message": "Thank you for contacting us!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)