from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

# it uses Comment model to build the form that the user uses
# i have explicity telling django that to use 'name','email' and 'body' fields from Comment medel
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name','email','body')

