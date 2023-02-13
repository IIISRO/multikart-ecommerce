"""multicart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('social-auth/', include('social_django.urls', namespace="social")),
]


urlpatterns += i18n_patterns(
    path('orders/',include('orders.urls', namespace='orders')),
    path('account/',include('accounts.urls', namespace='accounts')),
    path('api/', include('accounts.api.urls', namespace='accounts_api')),
    path('api/', include('products.api.urls', namespace='products_api')),
    path('api/', include('orders.api.urls', namespace='orders_api')),
    path('', include('products.urls', namespace='products')),
    path('', include('core.urls' , namespace='core')),
    prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]


handler404 = 'core.views.error_404_view'
