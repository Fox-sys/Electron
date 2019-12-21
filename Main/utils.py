from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic import View
import os


def news():
    return reversed(News.objects.all())

def CheckCOOKIE(request):
    if "UserNick" in request.COOKIES:
        if request.COOKIES["UserNick"] != "":
            h = request.COOKIES["UserNick"]
        else:
            h = ""
    else:
        h = ""
    return h

class TipRender:
    temp = None
    def get(self, request, **kwargs):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        if 'num' in kwargs:
            self.temp += kwargs['num']
            self.temp += '.html'
            return render(request, self.temp, context={'Nick': h, "ROOT": g, "news": news()})
        elif "Nic" in kwargs:
            n = get_object_or_404(user, Nickname_us=kwargs['Nic'])
            arts = Article.objects.filter(author_art__iexact=n.Nickname_us)
            self.temp += '.html'
            return render(request, self.temp, context={'Nick': h, "ROOT": g, "articles": arts, 'User': n, "news": news()})
        else:
            self.temp += '.html'
            return render(request, self.temp, context={'Nick': h, "ROOT": g, "news": news(), "News": news()})
