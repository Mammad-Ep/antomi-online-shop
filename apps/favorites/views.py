from django.shortcuts import render,redirect
from apps.products.models import Product
from .models import Favorites
from my_modules import login_required
from my_modules import View
from my_modules import HttpResponse
from my_modules import get_object_or_404
# _________________________________________________________________

def add_favorite_product(request):
    productId = request.GET.get('product_id')
    product = get_object_or_404(Product,id=productId)
    # temp=product.check_favorite_product(request)
    temp = Favorites.objects.filter(favorite_user=request.user,product=product)
    message = ''
    if not temp:
        Favorites.objects.create(
            favorite_user = request.user,
            product = product
        )
        message = 'محصول به علاقه مندی اضافه شد'
    else:
        message = 'محصول در علاقه مندی وجود دارد'    
    
    return HttpResponse(message)
# _________________________________________________________________

def status_favorite_product(request):
    count = 0
    if request.user.is_authenticated:
        favorites = Favorites.objects.filter(favorite_user=request.user)
        count = favorites.count()
        
    return HttpResponse(count)
# _________________________________________________________________

def remove_favorite_product(request):
    productId = request.GET.get('product_id')
    Favorites.objects.filter(product_id=productId).delete()
    
    return redirect('favorites:show_wishlist')
# _________________________________________________________________

class Wishlist(View):
    template_name = 'favorites_app/wishlist.html'
    def get(self, request, *args, **kwargs):
        
        return render(request,self.template_name)
# _________________________________________________________________

@login_required
def show_wishlist(request):
    favorites = Favorites.objects.filter(favorite_user=request.user)
    return render(request,'favorites_app/partials/show_wishlist.html',{'favorites':favorites})
# _________________________________________________________________
