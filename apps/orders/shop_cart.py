
from apps.products.models import Product
# _________________________________________________________________

class ShopCart:
    def __init__(self, request):
        self.session = request.session
        
        temp = self.session.get('shop_cart')
        if not temp:
            temp = self.session['shop_cart'] = {}
            
        self.shop_cart = temp
        self.count = len(self.shop_cart.keys())
        
    # -----------------------------------------
    
    def save(self):
        self.session.modified = True
        
    # -----------------------------------------
    
    def add_shop_cart(self,product,qty):
        productId = str(product.id)
        qty = int(qty)
        
        if productId not in self.shop_cart.keys():
            self.shop_cart[productId]={'price':product.product_price,'qty':0,'price_by_discount':product.price_by_discount()}
            
        temp = self.shop_cart[productId]['qty']+qty
        if temp > product.number_product_warehouse():
            self.shop_cart[productId]['qty'] = product.number_product_warehouse()
        else:
            self.shop_cart[productId]['qty']+=qty
        
        self.count = len(self.shop_cart.keys())
        self.save()    
    # -----------------------------------------
    
    def __iter__(self):
        products = Product.objects.filter(id__in=self.shop_cart.keys())
        
        for product in products:
            self.shop_cart[str(product.id)]['product'] = product
            
        for item in self.shop_cart.values():
            item['total_price']=item['qty']*item['price_by_discount']
            yield item
    # -----------------------------------------
    
    def remove_shop_cart(self,product):
        productId = str(product.id)
        if productId in self.shop_cart.keys():
            del self.shop_cart[productId]
            
        self.count = len(self.shop_cart.keys())
        self.save()    
    # -----------------------------------------
    
    def update_shop_cart(self,product,qty):
        productId = str(product.id)
        qty = int(qty)
        
        if productId in self.shop_cart.keys():
            self.shop_cart[productId]['qty'] = qty
        
        self.count = len(self.shop_cart.keys())
        self.save() 
    # -----------------------------------------
    
    def get_final_price(self):
        sum = 0
        for item in self.shop_cart.values():
            total_price = item['qty']*item['price_by_discount']
            sum+=total_price
            
        return sum
    # -----------------------------------------
    
    def clear_shop_cart(self):
        shop_cart = self.session.get('shop_cart')
        if shop_cart:
            del self.session['shop_cart']
            
        self.save()
    # -----------------------------------------