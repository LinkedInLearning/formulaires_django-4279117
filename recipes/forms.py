from django import forms
from .models import Recipe

class SearchForm(forms.Form):
    query = forms.CharField(label='Nom ou ingrédient', required=False)
    vegan = forms.BooleanField(label='Végane', required=False)
    sort = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'vegan', 'category', 'quantity', 'description' ]
        labels = {
            'title': 'Nom',
            'vegan': 'Végane',
            'category': 'Catégorie',
            'quantity': 'Quantité',
            'description': 'Description',
        }