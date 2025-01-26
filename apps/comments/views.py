from django.shortcuts import render,redirect
from apps.products.models import Product
from apps.accounts.models import CustomUser
from .forms import CommentProductForm,CommentChildForm
from .models import CommentProduct,CommentLike,CommentLikeType
from my_modules import get_object_or_404
from my_modules import login_required
from my_modules import HttpResponse
from my_modules import messages
# _________________________________________________________________

def create_comment_product(request,slug):
    if request.method == "GET":
        product = get_object_or_404(Product,slug=slug)
        form = CommentProductForm()
        return render(request,'comments_app/comment_product.html',{'form':form,'product':product})
    
    if request.method == "POST":
        form = CommentProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            product = get_object_or_404(Product,slug=slug)
            CommentProduct.objects.create(
                user_commenter = request.user,
                product = product,
                fullname = data['fullname'],
                email = data['email'],
                comment_text = data['comment_text']
            )
            messages.success(request,'دیدگاه با موفقیت ثبت شد','success')
            return redirect("products:product",product.slug)
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نیست','danger')
            return render(request,'comments_app/comment_product.html',{'form':form,'product':product})
        
# _________________________________________________________________

@login_required
def create_comment_child(request):
    if request.method == "GET":
        productId = request.GET.get('product_id')
        commentId = request.GET.get('comment_id')

        
        initial_data = {
            'product_id' : productId,
            'comment_id' : commentId
        }
        
        form = CommentChildForm(initial=initial_data)
        
        return render(request,'comments_app/comment_child.html',{'form':form,'comment_id':commentId})
    
    if request.method == "POST":
        form = CommentChildForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            product = get_object_or_404(Product,id=data['product_id'])
            CommentProduct.objects.create(
                user_commenter = request.user,
                product_id = data['product_id'],
                fullname = request.user.name,
                comment_text = data['comment_text_child'],
                comment_parent_id = data['comment_id']
            )
            messages.success(request,'پاسخ نظر درج شد','success')
            return redirect("products:product",product.slug)
        else:
            messages.error(request,'اطلاعات نامعتبر می باشد','danger')   
            # return redirect("products:product",slug=product.slug)

# _________________________________________________________________

def like_comment_partial(request,id):
    comment_like = []
    comment = get_object_or_404(CommentProduct,id=id)
    like_number,dislike_number = comment.get_number_like_dislike()
    flag = CommentLike.objects.filter(comment=comment,user_like=request.user)
    if flag:
        comment_like = flag[0]
    
    context={
        'comment':comment,
        'comment_like':comment_like,
        'like_number':like_number,
        'dislike_number':dislike_number,
        }    
    return render(request,'comments_app/partials/comment_like.html',context)
# _________________________________________________________________

def add_like_comment(request):
    commentId = request.GET.get('comment_id')
    likeType = request.GET.get('like_type')
    comment = get_object_or_404(CommentProduct,id=commentId)
    
    flag = CommentLike.objects.filter(comment=comment,user_like=request.user).exists()
    
    if not flag:
        comment_like = CommentLike.objects.create(
            comment = comment,
            user_like = request.user,
            like_type = CommentLikeType.objects.get(like_type=likeType)
            
        )
        comment_like.like_number+=1
        comment_like.save()
        
    return redirect('comments:like_comment_partial',comment.id)
    
# _________________________________________________________________

