from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic import View
from .utils import *
from django.template import RequestContext
from django.core.mail import send_mail
import os


class tools(TipRender, View):
    temp = "First/tools"


class hello(TipRender, View):
    temp = 'First/index'


class NSProfile(TipRender, View):
    temp = "First/NSProfile"


class article_detail(View):
    temp = "First/thread"

    def get(self, request, **kwargs):
        null = False
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        if 'id' in kwargs:
            art = get_object_or_404(Article, id__iexact=kwargs['id'])
            comment = Commet.objects.all()
            self.temp += '.html'
            if art.tags.all()[0].name == "":
                null = True
            return render(request, self.temp,
                          context={'Nick': h, "ROOT": g, "Article": art, 'comment': reversed(comment), "news": news(), "null": null})

    def post(self, request, **kwargs):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        p = user.objects.filter(Nickname_us__iexact=h)
        if len(p) != 0:
            l = p[0]
        else:
            l = 0
        if "text" in request.POST and l.banned < 1:
            art = Article.objects.get(id__iexact=kwargs["id"])
            bound_form = CommentForm(request.POST)
            if bound_form.is_valid():
                new_com = bound_form.save(h, art)
        return redirect("../forum/" + kwargs["id"])


class Forum(View):
    def get(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        All_Articles = Article.objects.all()
        form = SearchForm()
        return render(request, 'First/Forum.html',
                      context={'Art_list': reversed(All_Articles), 'Nick': h, "ROOT": g, 'form': form, "news": news()})

    def post(self, request):
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        h = CheckCOOKIE(request)
        bound_form = SearchForm(request.POST)
        rets = []
        t = False
        if bound_form.is_valid():
            new_search = bound_form.ret()
            All_Articles = Article.objects.all()
            for i in All_Articles:
                for j in i.tags.all():
                    for p in new_search:
                        if j.name == p:
                            rets.append(i)
                            t = True
                            break
                    if t:
                        break
            return render(request, 'First/Forum.html',
                          context={'Art_list': reversed(rets), 'Nick': h, "ROOT": g, 'form': bound_form,
                                   "news": news()})


class CreateArticle(View):
    def get(self, request, type):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        p = user.objects.filter(Nickname_us__iexact=h)
        if len(p) != 0:
            l = p[0]
        else:
            l = 0
        if h != "" and l.banned < 2:
            form = ArticleForm()
            return render(request, 'First/create_article.html',
                          context={'Form': form, 'Nick': h, "ROOT": g, "news": news(), 'type': type})
        else:
            return redirect("../")

    def post(self, request, type):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        bound_form = ArticleForm(request.POST)
        if bound_form.is_valid():
            n = Article.objects.all()
            for i in n:
                if i.name_art == request.POST['Title']:
                    art = Article.objects.get(name_art__iexact=request.POST['Title'])
                    return render(request, 'First/AlReadyExists.html',
                                  context={'art': request.POST['Title'], 'Nick': h, "ROOT": g, "news": news()})
                else:
                    continue
            r = []
            p = ""
            for i in request.POST['tags']:
                if i == " ":
                    r.append(p)
                    p = ""
                else:
                    p += i
            r.append(p)
            new_art = bound_form.save(h, r)
            art = Article.objects.get(name_art__iexact=request.POST['Title'])
            for i in r:
                p = Tag.objects.filter(name__iexact=i)
                if len(p) == 0:
                    g = Tag.objects.create(name=i)
                    art.tags.add(g)
                else:
                    art.tags.add(p[0])
            return redirect('../forum' + '/' + str(art.id))

class reg(View):
    def get(self, request):
        h = CheckCOOKIE(request)
        form = UserForm()
        return render(request, 'First/CreateUser.html', context={'Form': form, 'Nick': h, "news": news()})

    def post(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        bound_form = UserForm(request.POST)
        if bound_form.is_valid() and request.POST['Password'] == request.POST['repPassword']:
            n = user.objects.all()
            for i in n:
                if i.Nickname_us == request.POST['UserNick']:
                    User = user.objects.get(Nickname_us__iexact=request.POST['UserNick'])
                    return render(request, 'First/UserAlReadyExists.html',
                                  context={'art': request.POST['UserNick'], 'Nick': h, "ROOT": g, "news": news()})
                else:
                    continue

            new_user = bound_form.save()
            User = user.objects.get(Nickname_us__iexact=request.POST['UserNick'])
            response = HttpResponse(
                """
                       <script type="text/javascript">
                           location.replace("../");
                       </script>
                       <p>Такого аккаунта не существует</p><a href='../'>"<a href='../'>Кликните по ссылке что бы вернутся на главную</a></a>
                       """
            )
            response.set_cookie("UserNick", request.POST["UserNick"])
            response.set_cookie("ROOT", user.objects.get(Nickname_us__iexact=request.POST['UserNick']).root_us)
            return response


def exit_(request):
    h = CheckCOOKIE(request)
    req = HttpResponse(
        """
                       <script type="text/javascript">
                           location.replace("../");
                       </script>
                       <p>Такого аккаунта не существует</p><a href='../'>"<a href='../'>Кликните по ссылке что бы вернутся на главную</a></a>
                       """

    )
    req.set_cookie("UserNick", "")
    req.set_cookie("ROOT", False)
    return req


class Auto(View):
    def get(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        form = AutoForm()
        return render(request, 'First/AutoUser.html', context={'Form': form, 'Nick': h, "ROOT": g, "news": news()})

    def post(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        if h == "":
            bound_form = AutoForm(request.POST)
            if bound_form.is_valid() and bound_form.AutoFormCH() == True:
                req = HttpResponse(
                    """
                           <script type="text/javascript">
                               location.replace("../");
                           </script>
                           <p>Такого аккаунта не существует</p><a href='../'>"<a href='../'>Кликните по ссылке что бы вернутся на главную</a></a>
                           """
                )
                req.set_cookie("UserNick", request.POST["UserNick"])
                req.set_cookie("ROOT", user.objects.get(Nickname_us__iexact=request.POST['UserNick']).root_us)
            else:
                req = HttpResponse(
                    """
                    <script type="text/javascript">
                        location.replace("../login");
                    </script>
                    <p>Такого аккаунта не существует</p><a href='../login'>Кликните по ссылке что бы повторить авторизацию</a>
                    """
                )
            return req


def delete_art(request, id):
    h = CheckCOOKIE(request)
    n = Article.objects.get(id=id)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    if n.author_art == h or g == 'True':
        Article.objects.filter(id=id).delete()
        return redirect("../../../forum")
    else:
        return render(request, "First/NotYour.html", context={"Nick": h, "ROOT": g, "article": n, "news": news()})


def delete_com(request, id):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    n = Commet.objects.get(id__iexact=id)
    j = n.article_com.id
    if n.author_com == h or g == 'True':
        Commet.objects.filter(id=id).delete()
        return redirect("../../../forum/" + str(j))
    else:
        return render(request, "First/NotYour.html", context={"Nick": h, "ROOT": g, "comment": n, "news": news()})


class Support(View):
    def get(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        form = Sup()
        p = user.objects.filter(Nickname_us__iexact=h)
        if len(p) != 0:
            l = p[0]
        else:
            l = 0
        if l.banned < 3:
            return render(request, 'First/support.html', context={'Form': form, 'Nick': h, "ROOT": g, "us": p, "news": news()})
        else:
            return redirect("../")

    def post(self, request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        bound_form = Sup(request.POST)
        if bound_form.is_valid():
            if h != "":
                g = user.objects.get(Nickname_us__iexact=h)
                p = g.Nickname_us
                l = g.email_us
            else:
                p = "guest"
                l = "guest@none.ru"
            k = bound_form.save(l)
            send_mail(subject=k[1], message=p + "\n" + l + "\n" + k[2], from_email=k[0],
                      recipient_list=['berestovborisasz@gmail.com'], fail_silently=False)
        return redirect("../")


def subforum(request, args):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    arts = Article.objects.filter(sellf__iexact=args)
    return render(request, "First/fubforum.html",
                  context={"Nick": h, "ROOT": g, "ar": reversed(arts), "news": news(), "arg": args})


def tool(request, j):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    return render(request, "First/tools/" + j + ".html", context={"Nick": h, "ROOT": g, "news": news()})


def article_list(request):
    typeList = ["starts", "radio"]
    prom = []
    res = {}
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    for i in typeList:
        prom = exLesson.objects.filter(Type__iexact=i)
        res[i] = sorted(prom)
    return render(request, "First/lessons.html", context={"Nick": h, "ROOT": g, "news": news(), "lessons": res})


def article_l_det(request, q):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    return render(request, "First/Lessons/" + q + ".html", context={"Nick": h, "ROOT": g, "news": news()})


def New_detail(request, id):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    New = News.objects.get(id__iexact=id)
    return render(request, "First/New.html", context={"Nick": h, "ROOT": g, "news": news(), "new": New})
