from django.shortcuts import render
from apps.products.models import Product
from my_modules import get_object_or_404
from my_modules import login_required
from my_modules import redirect
from my_modules import HttpResponse
from .models import Scoring
# _________________________________________________________________

def scorings_partial(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'scorings_app/scorings_partial.html',{'product':product})
# _________________________________________________________________

@login_required
def add_score(request):
    product_id = request.GET.get('product_id')
    score = request.GET.get('score')
    product = Product.objects.get(id=product_id)
    flag = Scoring.objects.filter(scoring_user=request.user,product=product).exists()
    
    if not flag:
        Scoring.objects.create(
            scoring_user = request.user,
            product = product,
            score = score
        )
        
    return redirect('scorings:scorings_partial',product.slug)
# _________________________________________________________________