
from django.test import TestCase

from django.urls import reverse

from .models import Recipe, MultiRecipe, Comment, Fork, ForkComment

from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from django.core.files.uploadedfile import SimpleUploadedFile

# Reference for testing:
'''
Title: Django Tutorial Part 10: Testing a django web application
Author: MDN contributors
Date: 1998 - 2022
Code version: Django v4.0
URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
Software License: BSD
'''

#################################################### Tests for Sprint #3 ##############################################################

class TrivialTest(TestCase):

    ''' 
    Test Name: Trivial Test
    Input: None
    Expected output: None
    Written By: Anna
    '''
    def test_is_trivial(self):
        """
        trivial test for checking Github Actions CI
        """
        self.assertTrue(True)

''' 
Test Name: Google Login Test
Input: google credentials
Expected output: login to site, username displayed
Written By: Anna

This test was conducted manually and falls under the umbrella of UI testing. I visited the site, clicked 
"Login with Google" and entered my google credentials. The output matched the expected output: 
I was granted access to the site with "Welcome, [username]!". I completed this test with three different
google accounts of different endings (i.e. gmail.com, virginia.edu, bedford.k12.va.us).
'''

class GoogleLogin(TestCase):
    ''' 
    Test Name: Test no login to site
    Input: N/A
    Expected output: Prompt the user to login
    Written By: Anna
    '''
    def test_no_login(self):
        response = self.client.get(reverse('wordofmouth'))
        self.assertContains(response, "Login")

    ''' 
    Test Name: Test user login to site
    Input: User login
    Expected output: Welcome the user
    Written By: Anna
    '''
    def test_user_login(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User',
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('wordofmouth'))
        self.assertContains(response, "Welcome, Test User")


############################################################ Tests for Sprint # 4 #######################################################


class RecipeModel(TestCase):

    # setup Recipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")

    ''' 
    Test Name: Test Recipe model title field
    Input: Create Recipe
    Expected output: Correct Recipe title
    Written By: Anna
    '''
    def test_title_field(self):
        recipe = Recipe.objects.get(pk=1)
        title_field = recipe.title
        self.assertEqual(title_field, "Recipe A")

    ''' 
    Test Name: Test Recipe model title length
    Input: Create Recipe
    Expected output: Correct Recipe title max length
    Written By: Anna
    '''
    def test_title_length(self):
        recipe = Recipe.objects.get(pk=1)
        title_length = recipe._meta.get_field('title').max_length
        self.assertEqual(title_length, 200)

    ''' 
    Test Name: Test Recipe model ingredients
    Input: Create Recipe
    Expected output: Correct Recipe ingredients
    Written By: Anna
    '''
    def test_ingredients_field(self):
        recipe = Recipe.objects.get(pk=1)
        ingredients_field = recipe.ingredients
        self.assertEqual(ingredients_field, "flour")

    ''' 
    Test Name: Test Recipe model ingredients empty (default value)
    Input: Create Recipe
    Expected output: Recipe ingredients is an empty string
    Written By: Anna
    '''
    def test_ingredients_field_empty(self):
        recipe = Recipe.objects.create(title="Recipe B")
        ingredients_field = recipe.ingredients
        self.assertEqual(ingredients_field, "")

    ''' 
    Test Name: Test Recipe model recipe
    Input: Create Recipe
    Expected output: Correct Recipe recipe/instructions
    Written By: Anna
    '''
    def test_recipe_field(self):
        recipe = Recipe.objects.get(pk=1)
        recipe_field = recipe.recipe
        self.assertEqual(recipe_field, "mix")

    ''' 
    Test Name: Test Recipe model recipe empty (default value)
    Input: Create Recipe
    Expected output: Recipe recipe/instructions is an empty string
    Written By: Anna
    '''
    def test_recipe_field_empty(self):
        recipe = Recipe.objects.create(title="Recipe B")
        recipe_field = recipe.recipe
        self.assertEqual(recipe_field, "")

    ''' 
    Test Name: Test Recipe string/print override method
    Input: Create Recipe
    Expected output: Recipe is printed correctly (title)
    Written By: Anna
    '''
    def test_recipe_print(self):
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(str(recipe), "Recipe A")
    

class RecipeListViewTests(TestCase):

    ''' 
    Test Name: Test WordOfMouth home page with no recipes
    Input: User login
    Expected output: "No recipes are available."
    Written By: Anna
    '''
    def test_no_recipes(self):

        # method here for creating and logging in a test user
        '''
        Title: django-socialregistration-with-google-apps
        Author: flashingpumpkin, lizrice
        Date: 10/05/2009 - 02/01/2013
        Code version: Django v4.0
        URL: https://github.com/zapier/django-socialregistration-with-google-apps/blob/master/socialregistration/tests.py
        Software License: BSD
        '''
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('wordofmouth'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes are available.")
        self.assertQuerysetEqual(response.context['recipe_list'], [])

    ''' 
    Test Name: Test WordOfMouth home page with multiple recipes
    Input: User login
    Expected output: Recipe names displayed on page
    Written By: Anna
    '''
    def test_multiple_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        recipe2 = Recipe.objects.create(title="Recipe B", ingredients="water", recipe="boil")

        response = self.client.get(reverse('wordofmouth'))
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "Recipe B")
        self.assertQuerysetEqual(
            list(response.context['recipe_list']),
            [recipe1, recipe2],
        )


class RecipeSubmission(TestCase):
    ''' 
    Test Name: Test recipe submission page
    Input: User login, submitted recipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_recipe_form(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        response = self.client.post("/add/", {'recipe_title':'New Recipe', 'ingredients_text':'flour', 'recipe_text':'stir'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

class RecipeDisplay(TestCase):
    ''' 
    Test Name: Test recipe display page
    Input: User login, clicked recipe to view
    Expected output: error free display of recipe title, ingredients, instructions
    Written By: Anna
    '''
    def test_recipe_display(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        '''
        Title: Django Reverse with arguments '()' and keyword arguments '{}' not found
        Author: miki725
        Date: 11/02/2012
        Code version: Django v4.0
        URL: https://stackoverflow.com/questions/13202385/django-reverse-with-arguments-and-keyword-arguments-not-found
        Software License: BSD
        '''
        response = self.client.get(reverse('recipe', kwargs={'pk':recipe1.pk})) 
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "flour")
        self.assertContains(response, "mix")


############################################################ Tests for Sprint # 5 #######################################################


class RecipePhotoModel(TestCase):

    # setup Recipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")

    ''' 
    Test Name: Test Recipe model photo field
    Input: Create Recipe
    Expected output: Recipe photo is saved to google drive (check new photo url!)
    Written By: Anna
    '''
    def test_photo_field(self):
        recipe = Recipe.objects.get(pk=1)
        '''
        Title: Source code for django.core.files.uploadedfile
        Author: Django Software Foundation and individual contributors
        Date: 2005-2022
        Code version: Django v3.0
        URL: https://docs.djangoproject.com/en/3.0/_modules/django/core/files/uploadedfile/
        Software License: BSD
        '''
        recipe.photo = SimpleUploadedFile(name='pie.jpg', content=b'', content_type='image/jpeg') 
        self.assertTrue("https://drive.google.com/" in recipe.photo.url) # if the saved url for the image include "drive.google.com", assume that the image has been successfully saved to google drive


    ''' 
    Test Name: Recipe image display
    Input: Submit a Recipe with an image
    Expected output: Recipe is displayed with the appropriate image
    Written By: Anna

    This test was conducted manually and falls under the umbrella of UI testing. I visited the site,
    and determined that Recipes with images had their images displayed on the browser. Recipes without
    images displayed as normal (i.e. no change from original implementation). 
    '''

class MultiRecipeModel(TestCase):

    # setup Recipe objects and MultiRecipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        recipe2 = Recipe.objects.create(title="Recipe B", ingredients="water", recipe="boil")
        recipe3 = Recipe.objects.create(title="Recipe C", ingredients="sugar", recipe="add")
        article = MultiRecipe.objects.create(title="Recipes for April Fools Day!", author="anon")

    ''' 
    Test Name: Test MultiRecipe model title field
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe title
    Written By: Anna
    '''
    def test_title_field(self):
        article1 = MultiRecipe.objects.get(pk=1)
        title_field = article1.title
        self.assertEqual(title_field, "Recipes for April Fools Day!")

    ''' 
    Test Name: Test MultiRecipe model author field
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe author
    Written By: Anna
    '''
    def test_author_field(self):
        article1 = MultiRecipe.objects.get(pk=1)
        author_field = article1.author
        self.assertEqual(author_field, "anon")

    ''' 
    Test Name: Test MultiRecipe model date field
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe date
    Written By: Anna
    '''
    def test_date_field(self):
        article1 = MultiRecipe.objects.get(pk=1)
        diff = timezone.now() - article1.date
        self.assertTrue(diff <= datetime.timedelta(seconds=2))

    ''' 
    Test Name: Test MultiRecipe model title length
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe title max length
    Written By: Anna
    '''
    def test_title_length(self):
        article1 = MultiRecipe.objects.get(pk=1)
        title_length = article1._meta.get_field('title').max_length
        self.assertEqual(title_length, 200)

    ''' 
    Test Name: Test MultiRecipe model author length
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe author max length
    Written By: Anna
    '''
    def test_author_length(self):
        article1 = MultiRecipe.objects.get(pk=1)
        author_length = article1._meta.get_field('author').max_length
        self.assertEqual(author_length, 200)

    ''' 
    Test Name: Test MultiRecipe model add recipes
    Input: Create MultiRecipe
    Expected output: Correct MultiRecipe recipe titles
    Written By: Anna
    '''
    def test_add_recipes(self):
        article1 = MultiRecipe.objects.get(pk=1)
        recipe1 = Recipe.objects.get(pk=1)
        recipe2 = Recipe.objects.get(pk=2)
        recipe3 = Recipe.objects.get(pk=3)
        article1.recipes.append(recipe1.pk)
        article1.recipes.append(recipe2.pk)
        article1.recipes.append(recipe3.pk)
        self.assertEqual(Recipe.objects.get(pk=article1.recipes[0]).title, "Recipe A")
        self.assertEqual(Recipe.objects.get(pk=article1.recipes[1]).title, "Recipe B")
        self.assertEqual(Recipe.objects.get(pk=article1.recipes[2]).title, "Recipe C")

    ''' 
    Test Name: Test MultiRecipe model add descriptions
    Input: Create MultiRecipe
    Expected output: Correct descriptions
    Written By: Anna
    '''
    def test_add_descriptions(self):
        article1 = MultiRecipe.objects.get(pk=1)
        article1.descriptions.append("This article is about...")
        article1.descriptions.append("Here is recipe 1")
        article1.descriptions.append("Here is recipe 2")
        article1.descriptions.append("Here is recipe 3")
        self.assertEqual(article1.descriptions[0], "This article is about...")
        self.assertEqual(article1.descriptions[1], "Here is recipe 1")
        self.assertEqual(article1.descriptions[2], "Here is recipe 2")
        self.assertEqual(article1.descriptions[3], "Here is recipe 3")

    ''' 
    Test Name: Test MultiRecipe with no recipes saved
    Input: Create MultiRecipe
    Expected output: MultiRecipe recipes is an empty list
    Written By: Anna
    '''
    def test_recipes_empty(self):
        article1 = MultiRecipe.objects.get(pk=1)
        self.assertEqual(article1.recipes, [])
        self.assertEqual(len(article1.recipes), 0)

    ''' 
    Test Name: Test MultiRecipe with no descriptions saved
    Input: Create MultiRecipe
    Expected output: MultiRecipe descriptions is an empty list
    Written By: Anna
    '''
    def test_descriptions_empty(self):
        article1 = MultiRecipe.objects.get(pk=1)
        self.assertEqual(article1.descriptions, [])
        self.assertEqual(len(article1.descriptions), 0)

    ''' 
    Test Name: Test MultiRecipe string/print override method
    Input: Create MultiRecipe
    Expected output: MultiRecipe is printed correctly (title)
    Written By: Anna
    '''
    def test_multirecipe_print(self):
        article1 = MultiRecipe.objects.get(pk=1)
        self.assertEqual(str(article1), "Recipes for April Fools Day!")

class MultiRecipeListViewTests(TestCase):

    ''' 
    Test Name: Test WordOfMouth home page with no multirecipes and no recipes
    Input: User login
    Expected output: "No recipes are available."
    Written By: Anna
    '''
    def test_no_multirecipes_or_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('wordofmouth'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes are available.")
        self.assertQuerysetEqual(response.context['recipe_list'], [])

    ''' 
    Test Name: Test WordOfMouth home page with some multirecipes, recipes
    Input: User login
    Expected output: MultiRecipe names displayed on page
    Written By: Anna
    '''
    def test_multirecipes_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        recipe2 = Recipe.objects.create(title="Recipe B", ingredients="water", recipe="boil")

        article = MultiRecipe.objects.create(title="Recipes for April Fools!")

        response = self.client.get(reverse('wordofmouth'))
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "Recipe B")
        self.assertContains(response, "Recipes for April Fools!")
        self.assertQuerysetEqual(
            list(response.context['recipe_list']),
            [recipe1, recipe2],
        )
        self.assertQuerysetEqual(
            list(response.context['article_list']),
            [article]
        )


    ''' 
    Test Name: Test WordOfMouth home page with some multirecipes, no recipes
    Input: User login
    Expected output: MultiRecipe names displayed on page
    Written By: Anna
    '''
    def test_multirecipes_no_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article = MultiRecipe.objects.create(title="Recipes for April Fools!")

        response = self.client.get(reverse('wordofmouth'))
        self.assertContains(response, "No recipes are available.")
        self.assertContains(response, "Recipes for April Fools!")
        self.assertQuerysetEqual(
            list(response.context['recipe_list']),
            [],
        )
        self.assertQuerysetEqual(
            list(response.context['article_list']),
            [article]
        )

class ArticleSubmission(TestCase):
    ''' 
    Test Name: Test multirecipe submission page; no recipes
    Input: User login, submitted multirecipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_article_form_no_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        testcontext = {
            'article_title':'Recipes for April Fools!',
            'description_text':'Recipes about...',
        }

        response = self.client.post("/addarticle/", testcontext)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

    ''' 
    Test Name: Test multirecipe submission page; 1 recipe
    Input: User login, submitted multirecipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_article_form_one_recipe(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        testcontext = {
            'article_title':'Recipes for April Fools!',
            'description_text':'Recipes about...',
            'selectRecip1':'1',
            'description_recipe1':'recipe1',
        }

        response = self.client.post("/addarticle/", testcontext)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

    ''' 
    Test Name: Test multirecipe submission page; 2 recipes
    Input: User login, submitted multirecipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_article_form_two_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        testcontext = {
            'article_title':'Recipes for April Fools!',
            'description_text':'Recipes about...',
            'selectRecipe1':'1',
            'description_recipe1':'recipe 1',
            'selectRecipe2':'2',
            'description_recipe2':'recipe 2',
        }

        response = self.client.post("/addarticle/", testcontext)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

    ''' 
    Test Name: Test multirecipe submission page; 3 recipes
    Input: User login, submitted multirecipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_article_form_three_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        testcontext = {
            'article_title':'Recipes for April Fools!',
            'description_text':'Recipes about...',
            'selectRecipe1':'1',
            'description_recipe1':'recipe 1',
            'selectRecipe2':'2',
            'description_recipe2':'recipe 2',
            'selectRecipe3':'3',
            'description_recipe3':'recipe 3',
        }

        response = self.client.post("/addarticle/", testcontext)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

class ArticleDisplay(TestCase):

    @classmethod
    def setUpTestData(cls):
        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        recipe2 = Recipe.objects.create(title="Recipe B", ingredients="water", recipe="boil")
        recipe3 = Recipe.objects.create(title="Recipe C", ingredients="sugar", recipe="add")
        article = MultiRecipe.objects.create(title="Recipes for April Fools Day!")

    ''' 
    Test Name: Test article display page with no recipes
    Input: User login, clicked article to view
    Expected output: error free display of article title, recipes, descriptions
    Written By: Anna
    '''
    def test_article_display_no_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.descriptions.append("first description")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk}))
        self.assertContains(response, "Article A")
        self.assertContains(response, "first description")

    ''' 
    Test Name: Test article display page with one recipe
    Input: User login, clicked article to view
    Expected output: error free display of article title, recipes, descriptions
    Written By: Anna
    '''
    def test_article_display_one_recipe(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.descriptions.append("first description")
        article1.recipes.append('1')
        article1.descriptions.append("recipe 1")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk}))
        self.assertContains(response, "Article A")
        self.assertContains(response, "first description")
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "recipe 1")

    ''' 
    Test Name: Test article display page with two recipes
    Input: User login, clicked article to view
    Expected output: error free display of article title, recipes, descriptions
    Written By: Anna
    '''
    def test_article_display_two_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.descriptions.append("first description")
        article1.recipes.append('1')
        article1.descriptions.append("recipe 1")
        article1.recipes.append('2')
        article1.descriptions.append("recipe 2")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk})) 
        self.assertContains(response, "Article A")
        self.assertContains(response, "first description")
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "recipe 1")
        self.assertContains(response, "Recipe B")
        self.assertContains(response, "recipe 2")

    ''' 
    Test Name: Test article display page with three recipes
    Input: User login, clicked article to view
    Expected output: error free display of article title, recipes, descriptions
    Written By: Anna
    '''
    def test_article_display_three_recipes(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.descriptions.append("first description")
        article1.recipes.append('1')
        article1.descriptions.append("recipe 1")
        article1.recipes.append('2')
        article1.descriptions.append("recipe 2")
        article1.recipes.append('3')
        article1.descriptions.append("recipe 3")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk})) 
        self.assertContains(response, "Article A")
        self.assertContains(response, "first description")
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "recipe 1")
        self.assertContains(response, "Recipe B")
        self.assertContains(response, "recipe 2")
        self.assertContains(response, "Recipe C")
        self.assertContains(response, "recipe 3")

    ''' 
    Test Name: Test article display page author
    Input: User login, clicked article to view
    Expected output: error free display of author
    Written By: Anna
    '''
    def test_article_display_author(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A", author=self.user.username)
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk})) 
        self.assertContains(response, "Published By:")
        self.assertContains(response, "Test User")

    ''' 
    Test Name: Test article display page datetime
    Input: User login, clicked article to view
    Expected output: error free display of datetime
    Written By: Anna
    '''
    def test_article_display_datetime(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk})) 
        '''
        Title: datetime - Basic date and time types
        Author: Python Software Foundation
        Date: 2001 - 2022
        Code version: v3.9
        URL: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        Software License: Zero Clause BSD
        '''
        self.assertContains(response, timezone.localtime().strftime('%B %d, %Y, %I:%M').lstrip("0").replace(" 0", " "))
        
############################################################ Tests for Sprint # 6 #######################################################

##### Testing UI features, i.e. clicking buttons, creating input, etc: #####

# Test wordofmouth homepage functionality
    ''' 
    Test Name: Test recipe display
    Input: Select recipe
    Expected output: Display the selected recipe
    Written By: Anna
    
    By selecting "Banana Bread" displayed on the wordofmouth homepage, I was redirected to the url
    https://wordofmouth-b01.herokuapp.com/31/, where I was able to view the banana bread recipe 
    (including title, photo, list of ingredients, and instructions). The page also displayed
    a link for forking the recipe, and a text box and button to submit a comment.
    '''

    ''' 
    Test Name: Test article display
    Input: Select article
    Expected output: Display the selected article
    Written By: Anna
    
    By selecting "My Favorite Recipes" displayed on the wordofmouth homepage, I was redirected to 
    the url https://wordofmouth-b01.herokuapp.com/article/18/, where I was able to view the 
    article and the included recipes. The article page displayed the title, publisher, date published,
    description, and a list of clickable recipes and descriptions.
    '''

    ''' 
    Test Name: Test add recipe
    Input: Select add recipe button
    Expected output: Display the recipe submission form
    Written By: Anna
    
    By selecting "Add Recipe", I was redirected to the url https://wordofmouth-b01.herokuapp.com/add/
    which was a page that included text boxes for the recipe title, ingredients, and instructions.
    The page also had a button to search for and upload a photo and also had a submit button.
    '''

    ''' 
    Test Name: Test add article
    Input: Select add article button
    Expected output: Display the article submission form
    Written By: Anna
    
    By selecting "Add Article", I was redirected to the url https://wordofmouth-b01.herokuapp.com/addarticle/
    which was a page that included text boxes for the article title and descriptions.
    The page also had three dropdown buttons to allow me to select an already saved recipe. The
    three dropdown buttons included a list of all current saved recipes in the site. The page also 
    had a submit button.
    '''

# Test forking feature
    ''' 
    Test Name: Test forking display
    Input: Select "Fork this recipe!" link
    Expected output: Display a recipe submission form with each text box pre-loaded with the 
                     original recipe info
    Written By: Anna
    
    By selecting "Fork this recipe!", I was redirected to the url https://wordofmouth-b01.herokuapp.com/32/fork
    which was a page that included text boxes for the new recipe title, ingredients, and 
    instructions. The page had the heading: "Fork the [original title] recipe!", with the text boxes
    pre-filled with the original recipe's information. The pre-filled title only included the first
    word of the original title. The page also had a submit button and included the original recipe's
    photo.
    '''

    ''' 
    Test Name: Test forking submit
    Input: Select "Submit Fork" button
    Expected output: The forked recipe is linked back to the original recipe
    Written By: Anna
    
    By selecting "Submit Fork", I was redirected back to the original recipe page (https://wordofmouth-b01.herokuapp.com/32)
    which then included a link with the title of my forked recipe under "Similar Recipes:".
    '''

    ''' 
    Test Name: Test forking saved
    Input: Select forked recipe title link
    Expected output: The forked recipe (and changes) is saved
    Written By: Anna
    
    By selecting "[forked recipe title]", I was redirected to the url https://wordofmouth-b01.herokuapp.com/32/fork/19
    which was a recipe display page that included the forked recipe's title, ingredients, and 
    instructions (as edited from the original recipe). The page also had a comment box and submit
    button and NO option for forking this recipe. The page also includes a link back to the original
    recipe page.
    '''

    ''' 
    Test Name: Test forking link to original recipe
    Input: Select [original recipe title] link
    Expected output: The site redirects back to the original recipe, which is unchanged
    Written By: Anna
    
    By selecting "[original recipe title]", I was redirected to the url https://wordofmouth-b01.herokuapp.com/32
    which was a recipe display page that included the original recipe's information. This information
    was unchanged as a result of forking.
    '''

# Test comment feature
    ''' 
    Test Name: Test comment submission
    Input: Select recipe and enter comment in text box, click "Submit"
    Expected output: My comment is listed on this recipe's site
    Written By: Anna
    
    By entering a comment in the text box and clicking "Submit", the content I typed in the text box
    shows up at the bottom of the comment list with my username, the date, and the time shown. The 
    date and time of submission are correct.
    '''

# Test "Word of Mouth" navbar link
    ''' 
    Test Name: Test wordofmouth navbar link
    Input: From another page in the site, select the "Word of Mouth" navbar link
    Expected output: The site redirects back to the wordofmouth homepage
    Written By: Anna
    
    By selecting "Word of Mouth" from a recipe page, I was redirected back to the wordofmouth homepage.
    '''

# Test recipe submission
    ''' 
    Test Name: Test recipe submission
    Input: Create a recipe and select "Submit"
    Expected output: The site redirects to the homepage where my recipe is displayed at the top
                     of the recipe list
    Written By: Anna
    
    By entering a title, ingredients, and instructions into the text boxes and clicking "Submit", 
    I was redirected back to the wordofmouth homepage and the title of my submitted recipe showed
    up at the top of the displayed recipe list.
    '''

    ''' 
    Test Name: Test recipe saved
    Input: Select the recipe I just submitted
    Expected output: The site redirects to the recipe page and the information is correct
    Written By: Anna
    
    By clicking on the recipe title of the recipe I just submitted, I was redirected to the recipe
    page (https://wordofmouth-b01.herokuapp.com/32/), where the title, ingredients, and instructions
    of the recipe are the same as the ones I entered. 
    '''

# Test article submission
    ''' 
    Test Name: Test article submission
    Input: Create an article and select "Submit"
    Expected output: The site redirects to the homepage where my article is displayed at the top
                     of the article list
    Written By: Anna
    
    I entered a title and description of the article and used the dropdown to select a recipe and
    enter a description in the text box. I clicked "Submit" and was redirected back to the site's
    homepage, where my article title showed up at the top of the displayed article list.
    '''

    ''' 
    Test Name: Test article saved
    Input: Select the article I just submitted
    Expected output: The site redirects to the article page and the information is correct
    Written By: Anna
    
    By clicking on the article title of the article I just submitted, I was redirected to the article
    page (https://wordofmouth-b01.herokuapp.com/article/18/), where the title, descriptions, and
    linked recipes are the same as the ones I entered. 
    '''

# Test logout feature
    ''' 
    Test Name: Test logout feature
    Input: Click "Welcome, [username]" and select "Logout?"
    Expected output: The site redirects to the login page with the title of the site ("Word of Mouth")
                     and a button to "Login"
    Written By: Anna
    
    I clicked to logout of the site and was properly redirected to the login page of the site. If
    I have also logged out of my Google account, I am prompted to reenter my password to login, 
    otherwise, I am logged in automatically after clicking the "Login" button.
    '''
    
############################################################ Tests for Sprint # 7 #######################################################


class CommentModel(TestCase):

    # setup Recipe and Comment object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        recipeObj = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        Comment.objects.create(recipe=recipeObj, name="user", body="Comment on recipe")

    ''' 
    Test Name: Test Comment model recipe field
    Input: Create Comment
    Expected output: Correct Recipe title
    Written By: Anna
    '''
    def test_comment_recipe(self):
        comment = Comment.objects.get(pk=1)
        recipe_title = comment.recipe.title
        self.assertEqual(recipe_title, "Recipe A")

    ''' 
    Test Name: Test Comment model name length
    Input: Create Comment
    Expected output: Correct Comment name max length
    Written By: Anna
    '''
    def test_name_length(self):
        comment = Comment.objects.get(pk=1)
        name_length = comment._meta.get_field('name').max_length
        self.assertEqual(name_length, 50)

    ''' 
    Test Name: Test Comment model user
    Input: Create Comment
    Expected output: Correct Comment user
    Written By: Anna
    '''
    def test_user_field(self):
        comment = Comment.objects.get(pk=1)
        user = comment.name
        self.assertEqual(user, "user")

    ''' 
    Test Name: Test Comment model body
    Input: Create Comment
    Expected output: Correct Comment body
    Written By: Anna
    '''
    def test_body_field(self):
        comment = Comment.objects.get(pk=1)
        body = comment.body
        self.assertEqual(body, "Comment on recipe")

    ''' 
    Test Name: Test Comment string/print override method
    Input: Create Comment
    Expected output: Comment is printed correctly (Comment {body} by {name})
    Written By: Anna
    '''
    def test_comment_print(self):
        comment = Comment.objects.get(pk=1)
        self.assertEqual(str(comment), "Comment Comment on recipe by user")

class CommentViewTests(TestCase):

    # setup Recipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")

    ''' 
    Test Name: Test Recipe page with no comments
    Input: Click a recipe
    Expected output: "No recipes are available."
    Written By: Anna
    '''
    def test_no_comments(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipe', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "No comments here")

    ''' 
    Test Name: Test Recipe page with one comment
    Input: Click a recipe
    Expected output: "Comment 1"
    Written By: Anna
    '''
    def test_one_comment(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipeObj = Recipe.objects.get(pk=1)
        comment = Comment.objects.create(recipe=recipeObj, name="user", body="Comment 1")

        response = self.client.get(reverse('recipe', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "Comment 1")
        self.assertContains(response, "user")
        self.assertContains(response, timezone.localtime().strftime('%B %d, %Y, %I:%M').lstrip("0").replace(" 0", " "))

    ''' 
    Test Name: Test Recipe page with multiple comments
    Input: Click a recipe
    Expected output: "Comment 1", "Comment 2"
    Written By: Anna
    '''
    def test_multiple_comments(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipeObj = Recipe.objects.get(pk=1)
        comment1 = Comment.objects.create(recipe=recipeObj, name="user1", body="Comment 1")
        comment2 = Comment.objects.create(recipe=recipeObj, name="user2", body="Comment 2")

        response = self.client.get(reverse('recipe', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "Comment 1")
        self.assertContains(response, "user1")
        self.assertContains(response, "Comment 2")
        self.assertContains(response, "user2")

class LogoutTest(TestCase):
    ''' 
    Test Name: Test logout feature
    Input: Logout
    Expected output: "Word of Mouth" and option to "Login"
    Written By: Anna
    '''
    def test_logout(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)
        self.client.logout()

        response = self.client.get(reverse('wordofmouth'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

class RecipeModelAuthorDate(TestCase):

    # setup Recipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix", author="anna")

    ''' 
    Test Name: Test Recipe model author field
    Input: Create Recipe
    Expected output: Correct Recipe author
    Written By: Anna
    '''
    def test_author_field(self):
        recipe = Recipe.objects.get(pk=1)
        author_field = recipe.author
        self.assertEqual(author_field, "anna")

    ''' 
    Test Name: Test Recipe model default author field
    Input: Create Recipe
    Expected output: Correct Recipe author
    Written By: Anna
    '''
    def test_author_anonymous_field(self):
        recipe = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix")
        author_field = recipe.author
        self.assertEqual(author_field, "anonymous")

    ''' 
    Test Name: Test Recipe model author length
    Input: Create Recipe
    Expected output: Correct Recipe author max length
    Written By: Anna
    '''
    def test_author_length(self):
        recipe = Recipe.objects.get(pk=1)
        author_length = recipe._meta.get_field('author').max_length
        self.assertEqual(author_length, 200)

    ''' 
    Test Name: Test Recipe date field
    Input: Create Recipe
    Expected output: Correct date
    Written By: Anna
    '''
    def test_date_field(self):
        recipe = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix", author="anna")
        recipe_date = recipe.date
        self.assertEqual(recipe_date.strftime('%d-%m-%Y %H:%M:%S'), timezone.now().strftime('%d-%m-%Y %H:%M:%S'))

    ''' 
    Test Name: Test Recipe page with author
    Input: Click a recipe
    Expected output: "Published By: anna"
    Written By: Anna
    '''
    def test_recipe_author(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipeObj = Recipe.objects.get(pk=1)

        response = self.client.get(reverse('recipe', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published By: anna")

    ''' 
    Test Name: Test Recipe page with date
    Input: Click a recipe
    Expected output: "[month] [day], [time] [a.m./p.m.]"
    Written By: Anna
    '''
    def test_recipe_date(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        recipeObj = Recipe.objects.get(pk=1)

        response = self.client.get(reverse('recipe', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, timezone.localtime().strftime('%B %d, %Y, %I:%M').lstrip("0").replace(" 0", " "))


class ArticleWithRecipeAndFork(TestCase):

    # setup Recipe and Fork object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="flour", recipe="mix", author="anna")
        fork1 = Fork.objects.create(recipe=recipe1, title="fork Recipe A", ingredients="fork flour", instructions="fork mix")

    ''' 
    Test Name: Test article display with one recipe, one fork
    Input: User login, clicked article to view
    Expected output: error free display of article title, recipes, descriptions
    Written By: Anna
    '''
    def test_article_one_recipe_one_fork(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        article1 = MultiRecipe.objects.create(title="Article A")
        article1.descriptions.append("first description")
        article1.recipes.append('1') # pk for the recipe
        article1.descriptions.append("recipe 1") 
        article1.recipes.append('f1') # pk with 'f' tag for the fork
        article1.descriptions.append("fork 1")
        article1.save()
        response = self.client.get(reverse('article', kwargs={'pk':article1.pk})) 
        self.assertContains(response, "Article A")
        self.assertContains(response, "first description")
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "recipe 1")
        self.assertContains(response, "fork Recipe A")
        self.assertContains(response, "fork 1")

    ''' 
    Test Name: Test multirecipe submission page; 1 recipe, 1 fork
    Input: User login, submitted multirecipe
    Expected output: error free response
    Written By: Anna
    '''
    def test_add_article_form_one_recipe_one_fork(self):
        self.user = User.objects.create_user(
        email='abcd@gmail.com',
        password='1234',
        username='Test User'
        )
        self.client.force_login(self.user)

        testcontext = {
            'article_title':'Recipes for April Fools!',
            'description_text':'Recipes about...',
            'selectRecipe1':'1',
            'description_recipe1':'recipe 1',
            'selectRecipe2':'f2',
            'description_recipe2':'fork 1',
        }

        response = self.client.post("/addarticle/", testcontext)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

class MakeFork(TestCase):

    '''
    Test Name: Test Fork creation
    Input: Create a fork of a recipe
    Expected Output: Fork copies Recipe fields correctly
    Written by: Peter
    '''
    def test_create_fork(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients, instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk':recipe1.pk, 'rpk':fork1.pk}))
        self.assertContains(response, "Recipe A")
        self.assertContains(response, "test")
        self.assertContains(response, "steps")

    '''
    Test Name: Test if the fork is listed correctly after creation
    Input: Create a fork of a recipe
    Expected Output: Fork title and author are listed
    Written by: Peter
    '''
    def test_fork_listed(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('recipe', kwargs={'pk': recipe1.pk}))
        self.assertContains(response, fork1.title)
        self.assertContains(response, "anonymous") #default author name

    '''
    Test Name: Test if the fork has the correct header
    Input: Create a fork of a recipe
    Expected Output: You are viewing [fork.title]
    Written by: Peter
    '''
    def test_fork_made(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertContains(response, fork1.title)

    '''
    Test Name: Test if the fork links the original recipe page
    Input: Create a fork of a recipe
    Expected Output: Forked from [recipe.title]
    Written by: Peter
    '''
    def test_original_linked(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertContains(response, "Forked from")
        self.assertContains(response, recipe1.title)

    '''
    Test Name: Test if the fork has the correct header
    Input: Create a fork of a recipe
    Expected Output: No similar recipes have been posted
    Written by: Peter
    '''
    def test_no_fork(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe B", ingredients="food", recipe="mix")
        recipe1.save()

        response = self.client.get(reverse('recipe', kwargs={'pk': recipe1.pk}))
        self.assertContains(response, "No similar recipes have been posted.")

    '''
    Test Name: Test if the fork has the correct ingredients label
    Input: Create a fork of a recipe
    Expected Output: The ingredients you will need:
    Written by: Peter
    '''
    def test_instructions_label(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertContains(response, "The ingredients you will need:")

    '''
    Test Name: Test if the fork has the correct instructions label
    Input: Create a fork of a recipe
    Expected Output: The instructions:
    Written by: Peter
    '''
    def test_instructions_label(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertContains(response, "Instructions:")


class ForkCommentModel(TestCase):

    # setup Recipe and Comment object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()
        ForkComment.objects.create(recipe=fork1, name="user", body="Comment on recipe")

    ''' 
    Test Name: Test Fork Comment model recipe field
    Input: Create Comment on Forked Recipe
    Expected output: Correct Forked Recipe title
    Written By: Wamia
    '''

    def test_comment_recipe(self):
        comment = ForkComment.objects.get(pk=1)
        recipe_title = comment.recipe.title
        self.assertEqual(recipe_title, "Recipe A")

    ''' 
    Test Name: Test Forked Comment model name length
    Input: Create Forked Comment
    Expected output: Correct Forked Comment name max length
    Written By: Wamia
    '''

    def test_name_length(self):
        comment = ForkComment.objects.get(pk=1)
        name_length = comment._meta.get_field('name').max_length
        self.assertEqual(name_length, 50)

    ''' 
    Test Name: Test Forked Comment model user
    Input: Create Forked Comment
    Expected output: Correct Forked Comment user
    Written By: Wamia
    '''

    def test_user_field(self):
        comment = ForkComment.objects.get(pk=1)
        user = comment.name
        self.assertEqual(user, "user")

    ''' 
    Test Name: Test Fork Comment model body
    Input: Create Fork Comment
    Expected output: Correct Fork Comment body
    Written By: Wamia
    '''

    def test_body_field(self):
        comment = ForkComment.objects.get(pk=1)
        body = comment.body
        self.assertEqual(body, "Comment on recipe")

    ''' 
    Test Name: Test Fork Comment string/print override method
    Input: Create Fork Comment
    Expected output: Fork Comment is printed correctly (Comment {body} by {name})
    Written By: Wamia
    '''

    def test_comment_print(self):
        comment = ForkComment.objects.get(pk=1)
        self.assertEqual(str(comment), "Comment Comment on recipe by user")


class ForkCommentViewTests(TestCase):

    # setup Recipe object to be used within this class for testing
    @classmethod
    def setUpTestData(cls):
        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

    ''' 
    Test Name: Test Fork page with no comments
    Input: Click a forked recipe
    Expected output: "No comments have been posted."
    Written By: Wamia
    '''

    def test_no_comments(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "No comments have been posted")

    ''' 
    Test Name: Test Forked Recipe page with one comment
    Input: Click a forked recipe
    Expected output: "Comment 1"
    Written By: Wamia
    '''

    def test_one_comment(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        ForkComment.objects.create(recipe=fork1, name="user", body="Comment 1")

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "Comment 1")
        self.assertContains(response, "user")
        self.assertContains(response, timezone.localtime().strftime('%B %d, %Y, %I:%M').lstrip("0").replace(" 0", " "))

    ''' 
    Test Name: Test Forked Recipe page with multiple comments
    Input: Click a forked recipe
    Expected output: "Comment 1", "Comment 2"
    Written By: Wamia
    '''

    def test_multiple_comments(self):
        self.user = User.objects.create_user(
            email='abcd@gmail.com',
            password='1234',
            username='Test User'
        )
        self.client.force_login(self.user)

        recipe1 = Recipe.objects.create(title="Recipe A", ingredients="test", recipe="steps")
        recipe1.save()
        fork1 = Fork.objects.create(recipe=recipe1, title=recipe1.title, ingredients=recipe1.ingredients,
                                    instructions=recipe1.recipe)
        fork1.save()

        ForkComment.objects.create(recipe=fork1, name="user1", body="Comment 1")
        ForkComment.objects.create(recipe=fork1, name="user2", body="Comment 2")

        response = self.client.get(reverse('forkpage', kwargs={'pk': recipe1.pk, 'rpk': fork1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments:")
        self.assertContains(response, "Comment 1")
        self.assertContains(response, "user1")
        self.assertContains(response, "Comment 2")
        self.assertContains(response, "user2")

