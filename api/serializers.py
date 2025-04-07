from rest_framework import serializers
from authentication.models import User  # Use only this import
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product
from .models import PaymentProof

# ✅ Register Serializer using only Django default User fields
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        # Ensure password and confirm_password match
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        # Check that username is unique
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        # Check that the email is unique
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])  # Hash password properly
        user.save()
        return user

# ✅ Login Serializer (Using Django Authentication with SimpleJWT)
class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({"error": "Invalid username or password"})

        refresh = TokenObtainPairSerializer.get_token(user)  # Ensure correct token generation
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email,
        }

# ✅ Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Prevent manual user assignment
    user_email = serializers.CharField(source="user.email", read_only=True)  # Display email of the product owner
    created_at = serializers.DateTimeField(read_only=True)  # Display-only field
    image_url = serializers.SerializerMethodField()  # Handle image URL properly

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image', 'image_url', 'user', 'user_email', 'created_at']  # Include all necessary fields
        read_only_fields = ['user']  # Prevent manual assignment of user

    def get_image_url(self, obj):
        """Return the full image URL."""
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def validate(self, data):
        """Ensure product data is valid (e.g., price > 0)."""
        if data.get("price", 0) <= 0:
            raise serializers.ValidationError({"price": "Price must be greater than zero."})
        return data
# ✅ Farmer Dashboard Serializer (Now using ProductSerializer for nested product representation)
class FarmerDashboardSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.CharField()
    total_products = serializers.IntegerField()
    products = ProductSerializer(many=True)  # Directly use ProductSerializer for proper data structure

class PaymentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProof
        fields = '__all__'