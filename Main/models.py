from django.db import models
import datetime

lessonTypes = (
    ("starts", "Основы"),
    ("radio", "Радо Элементы"),
    ("deleted", "Удалённые")
)


class user(models.Model):
    Nickname_us = models.CharField("Ник", max_length=70, unique=True)
    email_us = models.EmailField("Почта", unique=True)
    password_us = models.CharField("Пароль", max_length=100)
    root_us = models.BooleanField("Админ", default=False)
    banned = models.IntegerField("Уровень бана", default=0)

    def __str__(self):
        return '{} {}'.format(self.id, self.Nickname_us)


class Article(models.Model):
    author_art = models.CharField("автор", max_length=70)
    name_art = models.CharField("название", max_length=100)
    text_art = models.TextField()
    sellf = models.CharField("curs", max_length=3)
    pub_date_art = models.DateTimeField(default=datetime.datetime.now())
    tags = models.ManyToManyField('Tag', blank=True, related_name="posts")

    def __str__(self):
        return '{} {} {}'.format(self.id, self.name_art, self.sellf)


class Commet(models.Model):
    article_com = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_com = models.CharField("автор", max_length=70)
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


class exLesson(models.Model):
    num = models.IntegerField("Номер урока в своей группе")
    Title = models.CharField("Название", max_length=100)
    link = models.CharField("название html файла", max_length=30)
    Type = models.CharField("тип урока", max_length=30, choices=lessonTypes, default="starts")
    Tag = models.ManyToManyField("Tag", "тэги", blank=True)

    def __str__(self):
        return '{} {}'.format(self.Title, self.Type)

    def __eq__(self, other):
        return self.num == other.num

    def __lt__(self, other):
        return self.num < other.num


class Tag(models.Model):
    name = models.CharField("название", max_length=30)
    create_date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return "{} {}".format(self.id, self.name)
