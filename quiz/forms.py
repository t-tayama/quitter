from django import forms
from .models import Quiz


class QuizCreateForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = (
            'title', 'text', 'image', 'category', 'tag',
            'choice_a', 'choice_b', 'choice_c', 'choice_d',
            'correct_answer', 'explanation'
            )


