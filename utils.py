import random
import os
import uuid
# ___________________________________________________________________________

def get_random_code(num):
    num-=1    
    return random.randint(10**num,10**(num+1)-1)

# print(get_random_code(7))
# ============================================================================

class FileUpload:
    def __init__(self, folder_app, folder_model):
        self.dir = 'images'
        self.folder_app = folder_app
        self.folder_model = folder_model
        
    def upload_to(self,instance,filename):
        file,exe=os.path.splitext(filename)
        return f'{self.dir}/{self.folder_app}/{self.folder_model}/{file}{uuid.uuid4}{exe}'
        
# ============================================================================

def get_price_delivery_tax(price,discount=0):
    delivery = 200000
    if price >=1000000:
        delivery = 0
        
    tax = price * 0.09
    
    price_discount = price - price*(discount/100)
    
    order_final_price = price_discount +delivery +tax
    
    return order_final_price,tax,delivery
# ============================================================================

from kavenegar import *
def send_sms(mobile_number,message):
    pass
    # try:
    #     api = KavenegarAPI('71576930522B30684E67736A482B4643625765316B4649564F7548384D494D7463505543613575724F63593D')
    #     params = { 'sender' : '', 'receptor': mobile_number, 'message' :message }
    #     response = api.sms_send( params)
    #     return response
    
    # except APIException as error:
    #     print(f'error1: {error}')
        
    # except HTTPException as error:
    #     print(f'error2: {error}')
    
# ============================================================================
