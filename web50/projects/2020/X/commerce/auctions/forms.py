from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        
class BidForm(forms.Form):
    bid_amount = forms.DecimalField(min_value=0.01, required=True)
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
