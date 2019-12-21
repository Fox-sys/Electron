from django.urls import path, include
from .views import *
urlpatterns = [
    path("", hello.as_view(), name = 'main_url'),
    path('forum', Forum.as_view(), name = 'Forum_url'),
    path('create_thread/<str:type>', CreateArticle.as_view(), name = 'New_Art_url'),
    path('forum/<str:id>', article_detail.as_view(), name = "art_url"),
    path('register', reg.as_view(), name = 'reg_url'),
    path('exit', exit_, name = 'exit_url'),
    path('login', Auto.as_view(), name = 'auto_url'),
    path('delete/thread/<str:id>', delete_art, name = 'del_art_url'),
    path("delete/comment/<str:id>", delete_com, name = 'del_com_url'),
    path("support", Support.as_view(), name = 'Support_url'),
    path("tools", tools.as_view(), name = 'tools_url'),
    path("subforum/<str:args>", subforum, name = 'subforum_url'),
    path("tool/<str:j>", tool, name = 'tool_url'),
    path('article', article_list, name= "art_list_url"),
    path('article/<str:q>', article_l_det, name= "art_det_url"),
    path('New/<str:id>', New_detail, name= "new_detail_url"),
]




