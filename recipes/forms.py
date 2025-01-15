from django import forms
from .models import Recipe, Category, Ingredient
from tinymce.widgets import TinyMCE


class SearchForm(forms.Form):
    query = forms.CharField(label='Nom ou ingrédient', required=False)
    vegan = forms.BooleanField(label='Végane', required=False)
    sort = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'vegan', 'category', 'quantity', 'image', 'description', 'password', 'confirmation', 'instructions' ]
        labels = {
            'title': 'Nom',
            'vegan': 'Végane',
            'category': 'Catégorie',
            'quantity': 'Quantité',
            'image': 'Image',
            'description': 'Description',
            'password': 'Mot de passe',
            'instructions': 'Instructions',
        },
        widgets = {
            'image': forms.FileInput(),
            'instructions': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'password': forms.PasswordInput(),
        }
    confirmation = forms.CharField(
        label='Confirmer le mot de passe', 
        widget=forms.PasswordInput(),
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('order'),
        widget=forms.RadioSelect()
    )

    def clean_confirmation(self):
        password     = self.cleaned_data.get('password')
        confirmation = self.cleaned_data.get('confirmation')
        if password != confirmation:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        return confirmation


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'optional']
        labels = {
            'name': 'Nom',
            'optional': 'Facultatif',
        }