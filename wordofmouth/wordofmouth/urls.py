from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'wordofmouth'
urlpatterns = [
    #path('<new_title>', views.wordofmouthListView.as_view(), name='wordofmouth'),
    path('', views.wordofmouthListView.as_view(), name='wordofmouth'),
    path('browserecipes/', views.recipeListView.as_view(), name='browserecipes'),
    path('browsearticles/', views.articleListView.as_view(), name='browsearticles'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('add/', views.addrecipe, name='addrecipe'),
    path('addarticle/', views.addarticle, name='addarticle'),
    #path('add/success/<new_title>', views.success, name='success'), # placeholder page for development (streamline later!)
    path('success', views.submit, name='submit'),
    path('successarticle', views.submitarticle, name='submitarticle'),
    path('<int:pk>/', views.recipe, name='recipe'),
    path('<int:pk>/fork', views.fork, name='fork'),
    path('<int:pk>/fork/<int:rpk>', views.forkpage, name='forkpage'),
    #path('<int:pk>/', views.comment, name='comment'),
    path('article/<int:pk>/', views.article, name='article'),
    path('logout', LogoutView.as_view()),


    #path('', include('main.urls')),
]