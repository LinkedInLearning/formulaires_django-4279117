from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Nom ou ingrédient', required=False)
    vegan = forms.BooleanField(label='Végane', required=False)
    sort = forms.IntegerField(widget=forms.HiddenInput(), initial=0)