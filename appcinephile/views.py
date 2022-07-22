from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse,JsonResponse
#from django.forms import inlineformser_factory
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from .models import *
from .forms import CreateUserForm

import requests
import json

#import pandas as pd
#import numpy as np
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
#from ast import literal_eval
# Create your views here.


def index(request):
    return render(request,'index.html')


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for' + user)
            return redirect('login')
    context = {'form' : form}
    return render(request,'register.html',context)



def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return render(request,'search.html')
        else:
            messages.info(request,'Username or Password is incorrect')
            return render(request,'login.html')

    return render(request,'login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login.html')
def profile(request,id):
    try:  
        obj = Profile.objects.get(user_id=id)
        rev_obj = Review.objects.filter(pen_id=obj.id)
        print(rev_obj)
        dict ={
            "alldetail" : Profile.objects.get(user_id=id),
            "allreview" : Review.objects.filter(pen_id=obj.id),
            "all_list" : Watched_list.objects.filter(pen_id=obj.id)
        }
        return render(request,'profile.html',context=dict)
    except ObjectDoesNotExist:
        return render(request,'new_profile.html')
    #return HttpResponse(alldetail.values)

@login_required(login_url='login.html')
def del_rev_pro(request,id,rev_id):

    try:

        obje = Review.objects.get(id=rev_id)
        obje.delete()

        obj = Profile.objects.get(user_id=id)
        rev_obj = Review.objects.filter(pen_id=obj.id)
        print(rev_obj)
        dict ={
            "alldetail" : Profile.objects.get(user_id=id),
            "allreview" : Review.objects.filter(pen_id=obj.id),
            "all_list" : Watched_list.objects.filter(pen_id=obj.id)
        }
        return render(request,'profile.html',context=dict)
    except ObjectDoesNotExist:
        return render(request,'new_profile.html')

@login_required(login_url='login')
def search(request):
    return render(request,'search.html')


def createprof(request,id):
    obj = Profile()
    obje = User.objects.get(id=id)
    obj.first_name = request.POST['f_name']
    obj.last_name = request.POST['l_name']
    obj.bio = request.POST['bio']
    obj.user_id = obje.id
    obj.save()
    return render(request,'search.html')
    #return redirect('login')

def details(request,movie_id):
    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

    querystring = {"i":movie_id,"r":"json","plot":"short"}

    headers = {
        'x-rapidapi-key': "855323c238msh7709c704bff719cp1dafd0jsn53afaa21d39b",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }




    response = requests.request("GET", url, headers=headers, params=querystring)
    temp = response.json()
    try:
        mydict = {
            "title":temp['Title'],
            "Year":temp['Year'],
            "rated":temp['Rated'] ,
            "released":temp['Released'] ,
            "runtime": temp['Runtime'],
            "genre":temp['Genre'],
            "director":temp['Director'],
            "writer":temp['Writer'],
            "actors":temp['Actors'],
            "plot":temp['Plot'],
            "language":temp['Language'],
            "country":temp['Country'],
            "awards":temp['Awards'],
            "poster":temp['Poster'],
            "movie_id":temp['imdbID'],
            "user_review":Review.objects.filter(movie_id=movie_id)
        }
        print(mydict["user_review"])
    except ObjectDoesNotExist:
        mydict = {
            "title":temp['Title'],
            "Year":temp['Year'],
            "rated":temp['Rated'] ,
            "released":temp['Released'] ,
            "runtime": temp['Runtime'],
            "genre":temp['Genre'],
            "director":temp['Director'],
            "writer":temp['Writer'],
            "actors":temp['Actors'],
            "plot":temp['Plot'],
            "language":temp['Language'],
            "country":temp['Country'],
            "awards":temp['Awards'],
            "poster":temp['Poster'],
            "movie_id":temp['imdbID'],
            "test":'yes test'
        }

    return render(request,'details.html',context=mydict)
    #return JsonResponse(temp)

def searchquery(request):
    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
    title = request.GET['s_name']
    querystring = {"s": title,"r":"json"}
    

    headers = {
        'x-rapidapi-key': "855323c238msh7709c704bff719cp1dafd0jsn53afaa21d39b",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    temp =response.json()

    #return JsonResponse(temp)
    return render(request,'index.html',context=temp)

def addreview(request,movie_id,id):

    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

    querystring = {"i":movie_id,"r":"json","plot":"short"}

    headers = {
        'x-rapidapi-key': "855323c238msh7709c704bff719cp1dafd0jsn53afaa21d39b",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    temp = response.json()

    obje = Profile.objects.get(user_id=id)
    obj = Review()
    obj.movie_id = movie_id
    obj.movie_name = temp['Title']
    obj.poster = temp['Poster']
    obj.content = request.POST['content']
    obj.pen_id_id = obje.id
    obj.save()
    #return reverse('details-name')
    return redirect('review')
    #return render(request,'details.html')
    #return HttpResponse(Hello)
    

@login_required(login_url='login')
def review(request):
    obj = Review.objects.all()
    mydict = {
        "allreview": obj
    }
    return render(request,'reviews.html',context=mydict)
    #return HttpResponse('Hello user')





@login_required(login_url='login')
def recommend(request,movie_id,id):
    

    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

    querystring = {"i":movie_id,"r":"json","plot":"short"}

    headers = {
        'x-rapidapi-key': "855323c238msh7709c704bff719cp1dafd0jsn53afaa21d39b",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    recent = response.json()

    obje = Profile.objects.get(user_id=id)
    obj = Watched_list()
    obj.movie_id = movie_id
    obj.pen_id_id = obje.id
    obj.movie_name = recent['Title']
    obj.poster = recent['Poster']
    obj.save()

    url = "https://movies-tvshows-data-imdb.p.rapidapi.com/"

    querystring = {"type":"get-similar-movies","imdb":movie_id,"page":"1"}

    headers = {
        'x-rapidapi-key': "536a80352fmsh9fe1db0bb92793cp1b822bjsnea8bd7e9ba57",
        'x-rapidapi-host': "movies-tvshows-data-imdb.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    temp=response.json()

    #return JsonResponse(temp)
    return render(request,'recommend.html',context=temp)

    #return render(request,'recommend.html',context=mydict)

@login_required(login_url='login')
def recomend(request,id):
    try:
        obj = Profile.objects.get(user_id=id)

        mov=Watched_list.objects.filter(pen_id_id=obj.id).last()
    #print(mov.movie_name)


        url = "https://movies-tvshows-data-imdb.p.rapidapi.com/"

        querystring = {"type":"get-similar-movies","imdb":mov.movie_id,"page":"1"}

        headers = {
            'x-rapidapi-key': "536a80352fmsh9fe1db0bb92793cp1b822bjsnea8bd7e9ba57",
            'x-rapidapi-host': "movies-tvshows-data-imdb.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        temp=response.json()
        return render(request,'recommend.html',context=temp)
    
    except :
        return render(request,'recommend.html',context = {"text":"Please add movies to your watch list to get recommendations."})

    #return JsonResponse(temp)
        

'''
@login_required(login_url='login')
def recommend(request):
    metadata = pd.read_csv("C:\datasets\movies_metadata.csv")
    creditss = pd.read_csv("C:\datasets\credits.csv")
    keywords = pd.read_csv("C:\datasets\keywords.csv")

    metadata = metadata.drop([19730,29503,35587])

    keywords['id'] = keywords['id'].astype('int')
    creditss['id'] = keywords['id'].astype('int')
    metadata['id'] = metadata['id'].astype('int')

    metadata = metadata.merge(creditss, on='id')
    metadata - metadata.merge(keywords, on='id')

    features=['cast','crew','keywords','genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(literal_eval)

    def get_director(x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan
    
    def get_list(x):
        if isinstance(x,list):
            names = [i['name'] for i in x]
            if len(names) > 3:
                names = names[:3]
            return names
        
        return []

    metadata['director'] = metadata['crew'].apply(get_director)

    features=['cast','keywords','genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(get_list)

    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            #Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        metadata[feature] = metadata[feature].apply(clean_data)

    def create_soup(x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

    metadata['soup'] = metadata.apply(create_soup, axis=1)

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(metadata['soup'])

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    metadata = metadata.reset_index()
    indices = pd.Series(metadata.index, index=metadata['title'])
    

    def get_recommendations(title, cosine_sim2=cosine_sim2):
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return metadata['title'].iloc[movie_indices]

    get_recommendations('The Twilight saga: New Moon', cosine_sim2)


    return HttpResponse("Hello working")
    #return render(request,'recommend.html')'''
    