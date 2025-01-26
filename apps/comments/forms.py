from django import forms

# _________________________________________________________________

class CommentProductForm(forms.Form):
    fullname = forms.CharField(max_length=70,
                               widget=forms.TextInput(attrs={
                                   "id":"author-comment",}),
                               error_messages={'required':'فیلد نام اجباری است'})
    
    email = forms.EmailField(max_length=150, required=False,
                               widget=forms.EmailInput(attrs={
                                   "id":"email-comment","dir":"ltr"}),
                               )
    
    comment_text = forms.CharField(max_length=70,
                               widget=forms.Textarea(attrs={
                                   "id":"review_comment",}),
                               error_messages={'required':'فیلد متن نظر اجباری است'})
    
# _________________________________________________________________

class CommentChildForm(forms.Form):
    product_id = forms.CharField(max_length=10, required=False,widget=forms.HiddenInput())
    comment_id = forms.CharField(max_length=10, required=False,widget=forms.HiddenInput())
    comment_text_child = forms.CharField(max_length=70,
                               widget=forms.Textarea(attrs={
                                   "id":"comment-child","cols":"20","rows":"3",
                                   "class":"form-control","placeholder":"پاسخ خود را درج کنید"}),
                               error_messages={'required':'فیلد متن نظر اجباری است'})
    
# _________________________________________________________________