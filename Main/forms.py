from django import forms
from .models import *


class ArticleForm(forms.Form):
    Title = forms.CharField(max_length=70)
    Text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=255)
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
        new_user = user.objects.create(Nickname_us=self.cleaned_data['UserNick'],
                                       email_us=self.cleaned_data['Email'],
                                       password_us=self.cleaned_data['Password'])
        return new_user


class AutoForm(forms.Form):
    UserNick = forms.CharField(max_length=20)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=20)

    def AutoFormCH(self):
        for i in user.objects.all():
            if i.Nickname_us == self.cleaned_data['UserNick']:
                if i.password_us == self.cleaned_data['Password']:
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
        a = []
        a.append(Auther)
        a.append(self.cleaned_data['Problem'])
        a.append(self.cleaned_data['Text'])
        return a
