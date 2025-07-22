from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/auth/', include('authotp.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/kitchen/', include('kitchen.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),

    # Frontend-related paths (optional if serving frontend separately)
    path('pricing/', include('pricing.urls')),
    path('pricing-table/', include('pricingtable.urls')),
    path('contact/', include('contact.urls')),
    path('hero/', include('hero.urls')),
    path('footer/', include('footer.urls')),

    # Optional: Redirect root to frontend
    path('', RedirectView.as_view(url='http://localhost:3000/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin titles
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.INDEX_TITLE
