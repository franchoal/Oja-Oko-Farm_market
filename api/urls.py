from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, 
    LoginView, 
    FarmerProductViewSet, 
    FarmerProductManagementViewSet, 
    FarmerDashboardViewSet, 
    ProductUploadView,
    EditProductView,
    PaymentProofUploadView,
    contact_view,
)

# Initialize the router
router = DefaultRouter()

# Register views for products and farmer's product management
router.register(r'products', FarmerProductViewSet, basename='product')  # Public products (pending)
router.register(r'farmer-products', FarmerProductManagementViewSet, basename='farmer-product')  # Farmer's own products

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    
    # Farmer dashboard endpoint
    path('dashboard/', FarmerDashboardViewSet.as_view(), name='farmer-dashboard'),

    # Product upload endpoint
    path('upload-product/', ProductUploadView.as_view(), name='upload-product'),  # Add this line
    
    # Edit product endpoint (PUT method)
    path('edit-product/<int:pk>/', EditProductView.as_view(), name='edit-product'),  # New URL pattern for editing products

    # Include router-generated routes (for public products and farmer's product management)
    path('', include(router.urls)),
    
    path("upload-payment-proof/", PaymentProofUploadView.as_view(), name="upload-payment-proof"),
    
    path('contact/', contact_view, name='contact'),
]
