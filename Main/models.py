from django.db import models
import datetime

class user(models.Model):
    Nickname_us = models.CharField("Ник", max_length = 70, unique=True)
    email_us = models.EmailField("Почта", unique = True)
    password_us = models.CharField("Пароль", max_length = 100)
    root_us = models.BooleanField("Админ", default=False)
    banned = models.IntegerField("Уровень бана", default=0)

    def __str__(self):
        return '{} {}'.format(self.id, self.Nickname_us)

class Article(models.Model):
    author_art = models.CharField("автор", max_length = 70)
    name_art = models.CharField("название", max_length = 100)
    text_art = models.TextField()
    sellf = models.CharField("curs", max_length = 3)
    pub_date_art = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '{} {} {}'.format(self.id, self.name_art, self.sellf)

class Commet(models.Model):
    article_com = models.ForeignKey(Article, on_delete = models.CASCADE)
    author_com = models.CharField("автор", max_length = 70)
    text_com = models.TextField()
    pub_date_com = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '{} {}'.format(self.id, self.article_com.name_art)

class News(models.Model):
    Title = models.CharField("название", max_length=90)
    Subtitle = models.CharField("Под название", max_length=90)
    text = models.TextField("текст")
    pub_date_com = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '{}'.format(self.Title)