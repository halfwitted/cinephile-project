from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('search',views.search,name='search'),
    path('searchquery',views.searchquery,name='searchquery'),
    path('/details/<movie_id>',views.details,name='details'),
    path('/writereview/<movie_id>/<int:id>',views.addreview,name='addreview'),
    path('login',views.login_page,name='login'),
    path('/recommend/<movie_id>/<int:id>',views.recommend,name='recommend'),
    path('/recomend/<int:id>',views.recomend,name='recomend'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register,name='register'),
    path('/createprof/<int:id>',views.createprof,name='createprof'),
    path('review',views.review,name='review'),
    path('/profile/<int:id>',views.profile,name='profile'),
    path('/profile/<int:id>/<int:rev_id>',views.del_rev_pro,name='del_rev')
    #path('recommend',views.recommend,name='recommend')
]