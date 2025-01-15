from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import Category, Recipe
from .forms import SearchForm, RecipeForm


SORTS = [('Likes', '-likes'), ('Récents', '-published'), ('Alphabétique', 'title')]


def filter(recipes, keyword, vegan_only):
    filter = Q(title__icontains=keyword) | Q(ingredient__name__icontains=keyword)
    if vegan_only:
        filter &= Q(vegan=True)
    return recipes.filter(filter).distinct()


def get_context(request, context):
    like = request.GET.get('like', None)
    if like:
        recipe = Recipe.objects.get(pk=like)
        recipe.likes += 1
        recipe.save()
    return {
        'categories': Category.objects.all().order_by('order'),
        'category_id': None,
    }|context


def index(request, category_id=None):
    sort_id = int(request.GET.get('sort', 0))
    recipes = Recipe.objects.filter(category=category_id) if category_id else Recipe.objects.all()
    search = SearchForm(request.GET.dict()|{'sort': sort_id})
    if(search.is_valid()):
        recipes = filter(
            recipes, 
            search.cleaned_data['query'], 
            search.cleaned_data['vegan']
        )
    context = get_context(request, {
        'sorts'      : [sort[0] for sort in SORTS],
        'sort_id'    : sort_id,
        'recipes'    : recipes.order_by(SORTS[sort_id][1]),
        'category_id': category_id,
        'search'     : search,
    })
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    context = get_context(request, {
        'recipe': recipe,
        'category_id': recipe.category.pk
    })
    template = loader.get_template('detail.html')
    return HttpResponse(template.render(context, request))


def edit(request, recipe_id=None):
    recipe = Recipe.objects.get(pk=recipe_id) if recipe_id else None
    form = RecipeForm(
        request.POST or None, 
        request.FILES or None, 
        instance=recipe
    )
    ok = request.method == 'POST' and form.is_valid()
    if ok:
        form.save()
    context = get_context(request, { 
        'ok': ok, 
        'form': form, 
        'recipe': recipe,
    })
    template = loader.get_template('edit.html')
    return HttpResponse(template.render(context, request))
