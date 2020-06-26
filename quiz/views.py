from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone

from account.models import User

from .forms import QuizCreateForm
from .models import Quiz, Category, Tag, Answer



# ! FunctionBaseViewによる記述(ココカラ) !
# ! コードはあえて冗長に書いています。注意 ！

# TODO お気に入り
# TODO Userモデルへフィールド追加（メールとお気に入り）


def index(request):
    """
    * ホーム画面(最新問題を5件表示)
    """
    latest_quiz_list = Quiz.objects.order_by('-created_at')[:5]
    context = {'latest_quiz_list': latest_quiz_list}
    return render(request, 'quiz/index.html', context)


class QuizListView(ListView):
    """
    * リスト表示 作成日降順 ページネーション10件ごと
    * 検索窓（タイトル又は問題文による絞り込み）の設定
    """
    model = Quiz
    context_object_name = 'quiz_list'
    template_name = 'quiz/list.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        queryset = Quiz.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword') # inputタグのname="keyword"が対応
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)|Q(text__icontains=keyword)
            )
        return queryset


class QuizCategoryView(ListView):
    """
    * カテゴリによる絞り込み表示
    """
    model = Quiz
    template_name = 'quiz/list.html'
    paginate_by = 5

    def get_queryset(self):
        # category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        # queryset = Quiz.objects.order_by('-created_at').filter(category=category)
        category_pk = self.kwargs['category_pk']
        queryset = Quiz.objects.order_by('-created_at').filter(category__pk=category_pk)
        return queryset


class QuizTagView(ListView):
    """
    * タグによる絞り込み表示
    """
    model = Quiz
    template_name = 'quiz/list.html'
    paginate_by = 5

    def get_queryset(self):
        # tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        # queryset = Quiz.objects.order_by('-created_at').filter(tag=tag)
        tag_pk = self.kwargs['tag_pk']
        queryset = Quiz.objects.order_by('-created_at').filter(tag__pk=tag_pk)
        return queryset


@login_required
def detail(request, quiz_pk):
    """
    * 問題の詳細表示(回答フォーム)
    """
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    context = {'quiz': quiz}
    return render(request, 'quiz/detail.html', context)


@login_required
def answer(request, quiz_pk):
    """
    * 回答ボタンを押した際の処理
    * 問題の正答と選択された選択肢を比較し正誤判定
    * Answerテーブルへの保存
    """

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    answerer = request.user

    try:
        selected_value = request.POST['selected']

        if selected_value == quiz.correct_answer:
            is_correct = True
        else:
            is_correct = False

        answer = Answer.objects.create(
            quiz=quiz,
            answerer=answerer,
            selected_value=selected_value,
            is_correct=is_correct
        )
        answer.save()

        context = {
            'quiz': quiz,
        'is_correct': is_correct
        }
        return render(request, 'quiz/result.html', context)

    except KeyError:
        context = {
            'quiz': quiz,
            'error_message': 'いづれかを選択してください。'
        }
        return render(request, 'quiz/detail.html', context)

def result(request, quiz_pk):
    """
    * 正誤判定を表示
    """
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    context = {'quiz': quiz}
    return render(request, 'quiz/result.html', context)


@login_required
def create(request):
    """
    * Quizの新規作成
    """
    if request.method == "POST":
        form = QuizCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            quiz = form.instance
            return redirect('quiz:detail', quiz_pk=quiz.pk)
    else:
        form = QuizCreateForm()

    context = {
            'word': '作成',
            'form': form,
        }
    return render(request, 'quiz/quizform.html', context)


@login_required
def edit(request, quiz_pk):
    """
    * Quizの編集
    """
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    request_user = request.user
    quiz_author = quiz.author

    if request.method == 'POST':
        form = QuizCreateForm(request.POST, instance=quiz)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.created_at = timezone.now()
            form.save()
            return redirect('quiz:detail', quiz_pk=quiz.pk)
    else:
        form = QuizCreateForm(instance=quiz)

    context = {
                'word': '編集',
                'form': form,
                'request_user': request_user,
                'quiz_author': quiz_author,
            }
    return render(request, 'quiz/quizform.html', context)



@login_required
def delete(request, quiz_pk):
    """
    * Quizの消去
    """
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    request_user = request.user
    quiz_author = quiz.author


    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz:list')

    context = {
        'quiz': quiz,
        'request_user': request_user,
        'quiz_author': quiz_author,
    }
    return render(request, 'quiz/confirm_delete.html', context)


@login_required
def mypage(request):
    user = request.user

    created_quiz_list = Quiz.objects.filter(author=user).order_by('-created_at')
    answer_history = Answer.objects.filter(answerer=user).order_by('-answered_at')


    if request.method == 'POST':
        if 'favorite' in request.POST:
            context = {}
        elif 'created' in request.POST:
            context = {'created_quiz_list': created_quiz_list,}
        elif 'answered' in request.POST:
            context = {'answer_history': answer_history,}

    else:
        context = {
            'created_quiz_list': created_quiz_list,
            'answer_history': answer_history,
        }
    return render(request, 'quiz/mypage.html', context)



# ! FunctionBaseViewによる記述(ココマデ) !



# 参考
# ! ClassBaseViewでの記述(ココカラ) !
# ! ClassBaseViewでの記述(ココマデ) !


