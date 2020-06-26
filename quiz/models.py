from django.db import models
from django.utils import timezone
from account.models import User

class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=255)

    def __str__(self):
        return self.name


class Quiz(models.Model):

    # タプル：一つ目の要素がDBに格納する値、二つ目が表示名
    QUIZ_CHOICES = (
        ('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')
        )

    author = models.ForeignKey(User,verbose_name='作成者',on_delete=models.CASCADE)

    title = models.CharField('タイトル', max_length=255)
    text = models.TextField('問題文')
    image = models.ImageField('画像', upload_to='img', blank=True, null=True)

    category = models.ForeignKey(Category, verbose_name='カテゴリ', blank=True, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)


    choice_a = models.CharField('選択肢a', max_length=255)
    choice_b = models.CharField('選択肢b', max_length=255)
    choice_c = models.CharField('選択肢c', max_length=255)
    choice_d = models.CharField('選択肢d', max_length=255)

    correct_answer = models.CharField('正解', choices=QUIZ_CHOICES, max_length=1)

    explanation = models.TextField('解説', blank=True)
    created_at = models.DateTimeField('問題更新日', default=timezone.now)

    def __str__(self):
        return self.title


class Answer(models.Model):

    ANSWER_CHOICES = (
        ('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')
    )
    quiz = models.ForeignKey(Quiz, verbose_name='回答した問題ID', on_delete=models.CASCADE)
    answerer = models.ForeignKey(User, verbose_name='回答者',on_delete=models.CASCADE)

    selected_value = models.CharField('回答', choices=ANSWER_CHOICES, max_length=1)

    is_correct = models.BooleanField('正誤判定')
    answered_at = models.DateTimeField('回答日', default=timezone.now)

    def __str__(self):
        result = '正解' if self.is_correct else '不正解'
        message = f'{self.quiz}への{self.answerer}さんの回答は{self.selected_value}で{result}でした'
        return message