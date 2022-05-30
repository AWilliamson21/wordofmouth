from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import CommentForm
from .models import Recipe, Fork, MultiRecipe, Comment, ForkComment


class wordofmouthListView(generic.ListView):
    template_name = 'wordofmouth/wordofmouth.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()

    '''
    Title: Can I have multiple lists in a Django generic.ListView?
    Author: Frank Wiles
    Date: 09/15/2013
    Code version: Django v4.0
    URL: https://stackoverflow.com/questions/18812505/can-i-have-multiple-lists-in-a-django-generic-listview
    Software License: BSD
    '''

    def get_context_data(self, *args, **kwargs):
        context = super(wordofmouthListView, self).get_context_data(*args, **kwargs)
        context['article_list'] = MultiRecipe.objects.all()
        return context


class recipeListView(generic.ListView):
    template_name = 'wordofmouth/browserecipes.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


class articleListView(generic.ListView):
    template_name = 'wordofmouth/browsearticles.html'

    def get_queryset(self):
        return Recipe.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(articleListView, self).get_context_data(*args, **kwargs)
        context['article_list'] = MultiRecipe.objects.all()
        return context


# def wordofmouth(request):
#     return render(request, 'wordofmouth/wordofmouth.html')

def addrecipe(request):
    return render(request, 'wordofmouth/addrecipe.html')


def addarticle(request):
    context = {
        'recipe_list':Recipe.objects.all(),
        'fork_list':Fork.objects.all()
    }
    return render(request, 'wordofmouth/addarticle.html', context)


def submit(request):
    # TODO: create recipe model, adding title (and other fields eventually), and save to database
    newtitle = request.POST["recipe_title"]
    newingredients = request.POST["ingredients_text"]
    newinstructions = request.POST["recipe_text"]
    newauthor = request.user.username
    # 1. upload photo to gdrive, 2. get photo gdrive link, 3. use fieldfile.save() to make the newphoto variable
    if (len(request.FILES) != 0):
        newphoto = request.FILES['img']
        newrecipe = Recipe(title=newtitle, ingredients=newingredients, recipe=newinstructions, photo=newphoto,
                           author=newauthor)
    else:
        newrecipe = Recipe(title=newtitle, ingredients=newingredients, recipe=newinstructions, author=newauthor)
    newrecipe.save()
    context = {
        'title': newtitle,
        'recipe_list': Recipe.objects.all(),
        'article_list': MultiRecipe.objects.all(),
    }
    # return HttpResponseRedirect(reverse('wordofmouth', context))
    return render(request, 'wordofmouth/wordofmouth.html', context)


def submitarticle(request):
    newtitle = request.POST["article_title"]
    if (newtitle.strip() != ""):  # remove whitespace and check that title is not empty
        newArticle = MultiRecipe(title=newtitle)
        newdescription = request.POST["description_text"]
        newArticle.descriptions.append(newdescription)
        newrecipe1 = request.POST["selectRecipe1"]
        newArticle.author = request.user.username
        if (newrecipe1 != '0'):
            newArticle.recipes.append(newrecipe1)
            newrecipedesc1 = request.POST["description_recipe1"]
            newArticle.descriptions.append(newrecipedesc1)
        newrecipe2 = request.POST["selectRecipe2"]
        if (newrecipe2 != '0'):
            newArticle.recipes.append(newrecipe2)
            newrecipedesc2 = request.POST["description_recipe2"]
            newArticle.descriptions.append(newrecipedesc2)
        newrecipe3 = request.POST["selectRecipe3"]
        if (newrecipe3 != '0'):
            newArticle.recipes.append(newrecipe3)
            newrecipedesc3 = request.POST["description_recipe3"]
            newArticle.descriptions.append(newrecipedesc3)
        newArticle.save()
    context = {
        'recipe_list': Recipe.objects.all(),
        'article_list': MultiRecipe.objects.all(),
        'title': newtitle,
    }
    return render(request, 'wordofmouth/wordofmouth.html', context)


def recipe(request, pk):
    currentRecipe = Recipe.objects.get(pk=pk)
    newauthor = request.user.username

    if request.POST.get('comment_field'):
        newbody = request.POST["comment_field"]
        newname = request.POST["name"]
        newcomment = Comment(recipe=currentRecipe, name=newname, body=newbody,)
        newcomment.save()

    if request.POST.get('recipe_title'):
        newtitle = request.POST["recipe_title"]
        newing = request.POST["ing_text"]
        newinstruc = request.POST["rec_text"]
        if (len(request.FILES) != 0):
            newphoto = request.FILES['img']
            newfork = Fork(recipe=currentRecipe, title=newtitle, ingredients=newing, instructions=newinstruc, author=newauthor, photo=newphoto)
        else:
            newfork = Fork(recipe=currentRecipe, title=newtitle, ingredients=newing, instructions=newinstruc, author=newauthor, photo=currentRecipe.photo)
        newfork.save()
        
    '''
    Title: Django - Google Drive API how to store and retrieve files using Django
    Author: Debraj Bhal
    Date: 07/29/2021
    Code version: v3.0
    URL: https://stackoverflow.com/questions/63460794/django-google-drive-api-how-to-store-and-retrieve-file-using-django
    Software License: BSD-3
    '''

    context = {
        'title': currentRecipe.title,
        'ingredients': currentRecipe.ingredients,
        'instructions': currentRecipe.recipe,
        'photo_url': currentRecipe.photo,
        'pk': pk,
        'forks': currentRecipe.forks.all(),
        'comments': currentRecipe.comments.all(),
        'date': currentRecipe.date,
        'author': currentRecipe.author
    }
    return render(request, 'wordofmouth/recipe.html', context)


def fork(request, pk):
    currentRecipe = Recipe.objects.get(pk=pk)

    context = {
        'title': currentRecipe.title,
        'ingredients': currentRecipe.ingredients,
        'instructions': currentRecipe.recipe,
        'photo_url': currentRecipe.photo,
        'pk': pk,
        'date': currentRecipe.date,
        'author': currentRecipe.author,
    }

    return render(request, 'wordofmouth/forkrecipe.html', context)


def forkpage(request, pk, rpk):
    currentRecipe = Recipe.objects.get(pk=pk)
    currentFork = Fork.objects.get(pk=rpk)
    if request.POST.get('comment_field'):
        newbody = request.POST["comment_field"]
        newname = request.POST["name"]
        newcomment = ForkComment(recipe=currentFork, name=newname, body=newbody)
        newcomment.save()
    context = {
        'oldtitle': currentRecipe.title,
        'title': currentFork.title,
        'ingredients': currentFork.ingredients,
        'instructions': currentFork.instructions,
        'photo_url': currentFork.photo,
        'pk': pk,
        'rpk': rpk,
        'comments': currentFork.comments.all(),
        'date': currentFork.date,
        'author': currentFork.author,
    }

    return render(request, 'wordofmouth/forkedrecipe.html', context)


# def comment(request, pk):

#     recipe = get_object_or_404(Recipe, pk=pk)

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             body = form.cleaned_data['comment_field']
#             name = form.cleaned_data['name']
#             new_comment.recipe = recipe
#             new_comment = Comment(recipe=recipe, body=body, name=name)
#             new_comment.save()

#     newbody = request.POST["comment_field"]
#     newname = request.POST["name"]
#     newcomment = Comment(recipe=recipe, name=newname, body=newbody)
#     print(newcomment.name)
#     print(newcomment.body)
#     newcomment.save()

#     return HttpResponseRedirect(reverse('recipe'))

def article(request, pk):
    currentArticle = MultiRecipe.objects.get(pk=pk)
    context = {
        'title': currentArticle.title,
        'descriptions': currentArticle.descriptions,
        'recipes': currentArticle.recipes,
        'author': currentArticle.author,
        'date': currentArticle.date,
    }
    if (len(currentArticle.recipes) >= 1):
        if (currentArticle.recipes[0][0] == "f"):
            recipepk1 = currentArticle.recipes[0].lstrip("f")
            context['recipetitle1'] = Fork.objects.get(pk=recipepk1).title
            context['recipepk1'] = recipepk1
            context['recipephoto1'] = Fork.objects.get(pk=recipepk1).photo
            context['originalRecipe1'] = Fork.objects.get(pk=recipepk1).recipe
        else:      
            context['recipetitle1'] = Recipe.objects.get(pk=currentArticle.recipes[0]).title
            context['recipepk1'] = currentArticle.recipes[0]
            context['recipephoto1'] = Recipe.objects.get(pk=currentArticle.recipes[0]).photo
    if (len(currentArticle.recipes) >= 2):
        if (currentArticle.recipes[1][0] == "f"):
            recipepk2 = currentArticle.recipes[1].lstrip("f")
            context['recipetitle2'] = Fork.objects.get(pk=recipepk2).title
            context['recipepk2'] = recipepk2
            context['recipephoto2'] = Fork.objects.get(pk=recipepk2).photo
            context['originalRecipe2'] = Fork.objects.get(pk=recipepk2).recipe
        else:
            context['recipetitle2'] = Recipe.objects.get(pk=currentArticle.recipes[1]).title
            context['recipepk2'] = currentArticle.recipes[1]
            context['recipephoto2'] = Recipe.objects.get(pk=currentArticle.recipes[1]).photo
    if (len(currentArticle.recipes) >= 3):
        if (currentArticle.recipes[2][0] == "f"):
            recipepk3 = currentArticle.recipes[2].lstrip("f")
            context['recipetitle3'] = Fork.objects.get(pk=recipepk3).title
            context['recipepk3'] = recipepk3
            context['recipephoto3'] = Fork.objects.get(pk=recipepk3).photo
            context['originalRecipe3'] = Fork.objects.get(pk=recipepk3).recipe
        else:
            context['recipetitle3'] = Recipe.objects.get(pk=currentArticle.recipes[2]).title
            context['recipepk3'] = currentArticle.recipes[2]
            context['recipephoto3'] = Recipe.objects.get(pk=currentArticle.recipes[2]).photo
    return render(request, 'wordofmouth/article.html', context)
