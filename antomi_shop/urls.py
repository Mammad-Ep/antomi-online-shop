"""
URL configuration for antomi_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from my_modules import static
from my_modules import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls',namespace='main'),name='main'),
    path('', include('apps.accounts.urls',namespace='accounts'),name='accounts'),
    path('', include('apps.products.urls',namespace='products'),name='products'),
    path('', include('apps.scorings.urls',namespace='scorings'),name='scorings'),
    path('', include('apps.comments.urls',namespace='comments'),name='comments'),
    path('', include('apps.favorites.urls',namespace='favorites'),name='favorites'),
    path('', include('apps.orders.urls',namespace='orders'),name='orders'),
    path('', include('apps.search.urls',namespace='search'),name='search'),
    path('payments/', include('apps.payments.urls',namespace='payments'),name='payments'),
    
	path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
