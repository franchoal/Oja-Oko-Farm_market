from django.contrib import admin
from django.urls import path, include  # ✅ Add missing imports
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
# from api.views import register_farmer 

def home_redirect(request):
    return JsonResponse({"message": "Welcome to the Farm Marketplace API"}, status=200)


urlpatterns = [
    # path("api/register/", register_farmer, name="register"),
    path("", home_redirect),  # Redirects '/' to a simple response
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # ✅ API routes
   
   
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


