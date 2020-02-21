from django import forms
from .models import *
from hashlib import sha256


class ArticleForm(forms.Form):
    Title = forms.CharField(max_length=70)
    Text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=255, required=False)
    Theme = forms.CharField(max_length=3)

    def save(self, Auther, ClearTags):
        new_Article = Article.objects.create(author_art=Auther,
                                             name_art=self.cleaned_data['Title'],
                                             text_art=self.cleaned_data['Text'],
                                             sellf=self.cleaned_data['Theme'],
                                             )
        return new_Article


class UserForm(forms.Form):
    UserNick = forms.CharField(max_length=20)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=20)
    repPassword = forms.CharField(widget=forms.PasswordInput, max_length=20)
    Email = forms.EmailField()

    def save(self):
        p = self.cleaned_data['Password'].encode("utf-8")
        new_user = user.objects.create(Nickname_us=self.cleaned_data['UserNick'],
                                       email_us=self.cleaned_data['Email'],
                                       password_us=sha256(p).hexdigest())
        return new_user


class AutoForm(forms.Form):
    UserNick = forms.CharField(max_length=20)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=20)

    def AutoFormCH(self):
        for i in user.objects.all():
            if i.Nickname_us == self.cleaned_data['UserNick']:
                p = self.cleaned_data['Password'].encode('utf-8')
                if i.password_us == sha256(p).hexdigest():
                    return True
                else:
                    continue
            else:
                continue
        return False


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, Auther, art):
        new_comment = Commet.objects.create(author_com=Auther,
                                            article_com=art,
                                            text_com=self.cleaned_data['text'])
        return new_comment


class SearchForm(forms.Form):
    req = forms.CharField(max_length=70)

    def ret(self):
        r = []
        a = ""
        for i in self.cleaned_data['req']:
            if i == " ":
                r.append(a)
                a = ""
            else:
                a += i
        r.append(a)
        return r


class Sup(forms.Form):
    Problem = forms.CharField()
    Text = forms.CharField(widget=forms.Textarea)

    def save(self, Auther):
        a = [Auther, self.cleaned_data['Problem'], self.cleaned_data['Text']]
        return a


class SearchLesson(forms.Form):
    SearchLesson = forms.CharField(max_length=90)

    def result(self):
        r = []
        a = ""
        for i in self.cleaned_data['SearchLesson']:
            if i == " ":
                r.append(a)
                a = ""
            else:
                a += i
        r.append(a)
        return r
