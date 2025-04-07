from django.contrib import admin
from .models import Product, Order
from authentication.models import User
from .models import PaymentProof
from .models import ContactMessage  # Import your model

# Register the User model if it is not already registered
if User not in admin.site._registry:
    admin.site.register(User)

# Register the Product model if it is not already registered
if Product not in admin.site._registry:
    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        list_display = ("name", "price", "user", "status", "created_at")
        search_fields = ("name", "user__email")
        list_filter = ("status", "created_at")

# Register the Order model if it is not already registered
if Order not in admin.site._registry:
    @admin.register(Order)
    class OrderAdmin(admin.ModelAdmin):
        list_display = ("customer", "product", "quantity", "total_price", "status", "created_at")
        search_fields = ("customer__email", "product__name")
        list_filter = ("status", "created_at")
@admin.register(PaymentProof)

class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'submitted_at', 'is_verified')
    list_filter = ('is_verified', 'submitted_at')
    search_fields = ('customer_name', 'phone_number')
    readonly_fields = ('proof_file', 'submitted_at')
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} payment(s) marked as verified.")
    mark_as_verified.short_description = "Mark selected payments as verified"
    
    
class ContactMessageAdmin(admin.ModelAdmin):
    # Proper indentation (4 spaces)
    list_display = ('name', 'email', 'message', 'created_at')  # Display these fields in the list view
    search_fields = ('name', 'email')  # Allow searching by name or email
    list_filter = ('created_at',)  # Optional: Filter by creation date

# Register the model with the admin panel
admin.site.register(ContactMessage, ContactMessageAdmin)