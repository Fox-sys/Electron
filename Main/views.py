from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic import View
from .utils import *
from django.template import RequestContext
from django.core.mail import send_mail
import os

messages = [
    "успешная регистрация",
    "аккаунт уже существует",
    "не верный пароль",
    "аккаунта не существует",
    "ваш аккаунт имеет уровень блокировки 1 или более, вы не можите оставлять коментарии",
    "ваш аккаунт имеет уровень блокировки 2 или более, вы не можите писать трэды",
    "ваш аккаунт имеет уровень блокировки 3, вы не можите писать в тэхническую поддержку",
    "успешный вход",
    "не все поля заполнены",
    "вы не автарезированны",
    "успешный выход",
    "у вас нет доступа",
    "вы уже авторизированны"
]


class tools(TipRender, View):
    temp = "First/tools"


class hello(TipRender, View):
    temp = 'First/index'


class NSProfile(TipRender, View):
    temp = "First/NSProfile"


class Post_detail(View):
    temp = "First/thread"

    def get(self, request, **kwargs):
        null = False
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        if 'id' in kwargs:
            art = get_object_or_404(Post, id__iexact=kwargs['id'])
            comment = Commet.objects.all()
            self.temp += '.html'
            if art.tags.all()[0].name == "" and len(art.tags.all()) == 1:
                null = True
            imagesNoneCheck = [art.img1, art.img2, art.img3, art.img4, art.img5, art.img6, art.img7, art.img8, art.img9,
                      art.img10]
            images = []
            for i in range(len(imagesNoneCheck)):
                if imagesNoneCheck[i] == "":
                    pass
                else:
                    images.append("/media/" + str(imagesNoneCheck[i]))
            return render(request, self.temp,
                          context={'Nick': h, "ROOT": g, "Post": art, 'comment': reversed(comment), "news": news(),
                                   "null": null, "images": images})

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
            art = Post.objects.get(id__iexact=kwargs["id"])
            bound_form = CommentForm(request.POST)
            if bound_form.is_valid():
                new_com = bound_form.save(h, art)
            else:
                return render(request, "redirect.html",
                              context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})
        elif l.banned >= 1:
            return render(request, "redirect.html",
                          context={"url": "", "message": messages[4], 'Nick': h, "ROOT": g})
        return redirect("../forum/" + kwargs["id"])


class Forum(View):
    @staticmethod
    def get(request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        All_Posts = Post.objects.all()
        form = SearchForm()
        return render(request, 'First/Forum.html',
                      context={'Art_list': reversed(All_Posts), 'Nick': h, "ROOT": g, 'form': form, "news": news()})

    @staticmethod
    def post(request):
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
            All_Posts = Post.objects.all()
            for i in All_Posts:
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
        else:
            return render(request, "redirect.html", context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})


class CreatePost(View):
    @staticmethod
    def get(request, type):
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
            form = PostForm()
            return render(request, 'First/create_Post.html',
                          context={'Form': form, 'Nick': h, "ROOT": g, "news": news(), 'type': type})
        elif l.banned >= 2:
            return render(request, "redirect.html",
                          context={"url": "../", "message": messages[5], 'Nick': h, "ROOT": g})
        else:
            return render(request, "redirect.html",
                          context={"url": "../", "message": messages[9], 'Nick': h, "ROOT": g})

    @staticmethod
    def post(request, type):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            n = Post.objects.all()
            for i in n:
                if i.name_art == request.POST['Title']:
                    art = Post.objects.get(name_art__iexact=request.POST['Title'])
                    return render(request, 'First/AlReadyExists.html',
                                  context={'art': request.POST['Title'], 'Nick': h, "ROOT": g, "news": news()})
                else:
                    continue
            r = request.POST["tags"].split(" ")
            new_art = bound_form.save(h, r)
            art = Post.objects.get(name_art__iexact=request.POST['Title'])
            for i in r:
                p = Tag.objects.filter(name__iexact=i)
                if len(p) == 0:
                    g = Tag.objects.create(name=i)
                    art.tags.add(g)
                else:
                    art.tags.add(p[0])
            return redirect('../forum/' + str(art.id))
        else:
            return render(request, "redirect.html", context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})


class reg(View):
    @staticmethod
    def get(request):
        h = CheckCOOKIE(request)
        form = UserForm()
        return render(request, 'First/CreateUser.html', context={'Form': form, 'Nick': h, "news": news()})

    @staticmethod
    def post(request):
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
                    return render(request, "redirect.html",
                                  context={"url": "", "message": messages[1], 'Nick': h, "ROOT": g})
                else:
                    continue

            new_user = bound_form.save()
            User = user.objects.get(Nickname_us__iexact=request.POST['UserNick'])
            response = HttpResponse(
                render(request, "redirect.html", context={"url": "../", "message": messages[0], 'Nick': h, "ROOT": g})
            )
            response.set_cookie("UserNick", request.POST["UserNick"])
            response.set_cookie("ROOT", user.objects.get(Nickname_us__iexact=request.POST['UserNick']).root_us)
            return response
        else:
            return render(request, "redirect.html", context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})


def exit_(request):
    h = CheckCOOKIE(request)
    req = HttpResponse(
        render(request, "redirect.html", context={"url": "../", "message": messages[10], 'Nick': h})
    )
    req.set_cookie("UserNick", "")
    req.set_cookie("ROOT", False)
    return req


class Auto(View):
    @staticmethod
    def get(request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        form = AutoForm()
        return render(request, 'First/AutoUser.html', context={'Form': form, 'Nick': h, "ROOT": g, "news": news()})

    @staticmethod
    def post(request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        if h == "":
            bound_form = AutoForm(request.POST)
            if bound_form.is_valid() and bound_form.AutoFormCH() == True:
                req = HttpResponse(
                    render(request, "redirect.html", context={"url": "../", "message": messages[7], 'Nick': h, "ROOT": g})
                )
                req.set_cookie("UserNick", request.POST["UserNick"])
                req.set_cookie("ROOT", user.objects.get(Nickname_us__iexact=request.POST['UserNick']).root_us)
            elif not bound_form.is_valid():
                req = HttpResponse(
                    render(request, "redirect.html",
                           context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})
                )
            else:
                req = HttpResponse(
                    render(request, "redirect.html", context={"url": "", "message": messages[2], 'Nick': h, "ROOT": g})
                )
            return req
        else:
            return render(request, "redirect.html", context={"url": "../", "message": messages[12], 'Nick': h, "ROOT": g})


def delete_art(request, id):
    h = CheckCOOKIE(request)
    n = Post.objects.get(id=id)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    if n.author_art == h or g == 'True':
        Post.objects.filter(id=id).delete()
        return redirect("../../forum/")
    else:
        return render(request, "redirect.html", context={"url": "../../forum/", "message": messages[11], 'Nick': h, "ROOT": g})


def delete_com(request, id):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    n = Commet.objects.get(id__iexact=id)
    j = n.Post_com.id
    if n.author_com == h or g == 'True':
        Commet.objects.filter(id=id).delete()
        return redirect("../../forum/" + str(j))
    else:
        return render(request, "redirect.html", context={"url": "../../forum/" + str(j), "message": messages[11],
                                                         'Nick': h, "ROOT": g})


class Support(View):
    @staticmethod
    def get(request):
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
            return render(request, 'First/support.html',
                          context={'Form': form, 'Nick': h, "ROOT": g, "us": p, "news": news()})
        else:
            return render(request, "redirect.html", context={"url": "../", "message": messages[6], 'Nick': h, "ROOT": g})

    @staticmethod
    def post(request):
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
    arts = Post.objects.filter(sellf__iexact=args)
    return render(request, "First/fubforum.html",
                  context={"Nick": h, "ROOT": g, "ar": reversed(arts), "news": news(), "arg": args})


def tool(request, j):
    h = CheckCOOKIE(request)
    if 'ROOT' in request.COOKIES:
        g = request.COOKIES['ROOT']
    else:
        g = 'False'
    return render(request, "First/tools/" + j + ".html", context={"Nick": h, "ROOT": g, "news": news()})


class Post_list(View):
    @staticmethod
    def get(request):
        typeList = ["starts", "radio"]
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

    @staticmethod
    def post(request):
        h = CheckCOOKIE(request)
        if 'ROOT' in request.COOKIES:
            g = request.COOKIES['ROOT']
        else:
            g = 'False'
        bound_form = SearchLesson(request.POST)
        if bound_form.is_valid():
            tags = bound_form.result()
            prom = []
            lessons = exLesson.objects.all()
            for i in lessons:
                if i.Type != "deleted":
                    res = []
                    a = ""
                    for j in i.Title.lower():
                        if j == " ":
                            res.append(a)
                            a = ""
                        else:
                            a += j
                    res.append(a)
                    for j in res:
                        for k in tags:
                            if j == k.lower():
                                prom.append(i)
                                res = []
                                break
                    gg = i.Tag.all()
                    for j in gg:
                        for k in tags:
                            if j.name.lower() == k.lower():
                                if len(prom) != 0:
                                    for q in prom:
                                        print(k)
                                        if q.Title == i.Title:
                                            gg = []
                                            break
                                        else:
                                            prom.append(i)
                                            gg = []
                                            break
                                else:
                                    prom.append(i)
                                    gg = []
                                    break
                res = {}
                res["sorted"] = sorted(prom)
                return render(request, "First/lessons.html", context={"Nick": h, "ROOT": g, "news": news(), "lessons": res})
            else:
                return render(request, "redirect.html", context={"url": "", "message": messages[8], 'Nick': h, "ROOT": g})


def Post_l_det(request, q):
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
