from django import forms
from .models import *
from hashlib import sha256


class PostForm(forms.Form):
    """Form for creating a post"""
    Title = forms.CharField(max_length=70)
    Text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=255, required=False)
    Theme = forms.CharField(max_length=3)
    img1 = forms.ImageField(required=False)
    img2 = forms.ImageField(required=False)
    img3 = forms.ImageField(required=False)
    img4 = forms.ImageField(required=False)
    img5 = forms.ImageField(required=False)
    img6 = forms.ImageField(required=False)
    img7 = forms.ImageField(required=False)
    img8 = forms.ImageField(required=False)
    img9 = forms.ImageField(required=False)
    img10 = forms.ImageField(required=False)

    def save(self, Auther, ClearTags):
        new_Post = Post.objects.create(author_art=Auther,
                                             name_art=self.cleaned_data['Title'],
                                             text_art=self.cleaned_data['Text'],
                                             sellf=self.cleaned_data['Theme'],
                                             )
        return new_Post


class UserForm(forms.Form):
    """Form for user regestation"""
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
    """Form for user authentication"""
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
        return False


class CommentForm(forms.Form):
    """Form for creating a comment for Posts"""
    text = forms.CharField(widget=forms.Textarea)

    def save(self, Auther, post):
        new_comment = Commet.objects.create(author_com=Auther,
                                            Post_com=post,
                                            text_com=self.cleaned_data['text'])
        return new_comment


class SearchForm(forms.Form):
    """Form for post searching"""
    req = forms.CharField(max_length=70)

    def ret(self):
        return self.cleaned_data['req'].split(" ")


class Sup(forms.Form):
    """Form for sending request to the support"""
    Problem = forms.CharField()
    Text = forms.CharField(widget=forms.Textarea)

    def save(self, Auther):
        a = [Auther, self.cleaned_data['Problem'], self.cleaned_data['Text']]
        return a


class SearchLesson(forms.Form):
    """Searching of lessongs"""
    SearchLesson = forms.CharField(max_length=90)

    def result(self):
        return self.cleaned_data['SearchLesson'].split(" ")
