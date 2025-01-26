from django.shortcuts import render
from my_modules import View
from my_modules import settings
# _________________________________________________________________

class Index(View):
    template_name = 'main_app/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
# _________________________________________________________________

def media_admin(request):
    return {'media_url':settings.MEDIA_URL}
# _________________________________________________________________

def handler404(request,*exc):
    return render(request,'main_app/404.html')
# _________________________________________________________________
