class CompareProduct:
    def __init__(self, request):
        self.session = request.session
        temp_product = self.session.get('compare_product')
        temp_group = self.session.get('compare_group')
        
        if not temp_product and not temp_group:
            temp_product = self.session['compare_product']=[]
            temp_group = self.session['compare_group']=[]
            
        self.compare_product = temp_product
        self.compare_group = temp_group
        
        self.count = len(self.compare_product)
    
    # ---------------------------------------------------------
    
    def save(self):
        self.session.modified = True
    
    # ---------------------------------------------------------
    
    def __iter__(self):
      return self
    # ---------------------------------------------------------
    
    def add_compare_product(self,product_id,group_id):
        productId = int(product_id)
        groupId = int(group_id)
        
        if self.compare_product:
            if productId not in self.compare_product and groupId in self.compare_group:
                self.compare_product.append(productId)
                self.compare_group.append(groupId)
        else:
            self.compare_product.append(productId)
            self.compare_group.append(groupId)
        
        self.count = len(self.compare_product)
        self.save()
    # ---------------------------------------------------------
    
    def remove_compare_product(self,product_id,group_id):
        productId = int(product_id)
        groupId = int(group_id)
        
        if productId in self.compare_product:
            self.compare_product.remove(productId)
            self.compare_group.remove(groupId)
            
        self.count = len(self.compare_product)
        self.save()
    
    # ---------------------------------------------------------
    
    def clear_compare_product(self):
        if self.compare_product:
            del self.session['compare_product']
            del self.session['compare_group']
            
        self.save()
    # ---------------------------------------------------------