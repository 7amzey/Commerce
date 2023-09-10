from django import forms
from .models import Product, Category, Bid, Comment

class create_post(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "title_input", "autocomplete": "off"}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "description_input"}))
    start_price = forms.FloatField(label="", min_value=0, widget=forms.NumberInput(attrs={"class": "price_input"}))
    category = forms.ModelChoiceField(label="", queryset=Category.objects.all(), widget=forms.Select(attrs={"class": "category_input"}))
    image = forms.ImageField(label="", required = False ,widget=forms.FileInput(attrs={"class": "image", "id":"file"}))

    class Meta:
        model = Product
        fields = ('title', 'description', 'start_price', 'category', 'image', )

class NewBidForm(forms.ModelForm):
    offer = forms.FloatField(label="", min_value=0, widget=forms.NumberInput(attrs={"class": "form-control", "id": "example-number-input"}))

    class Meta:
        model = Bid
        fields = ('offer',)

class CommentsForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "rows":"3", "name": "comment"}))

    class Meta:
        model =  Comment
        fields = ('content',)

class Search_barForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={}))
