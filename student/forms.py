from django import forms
from tests.models import AnswerSheet

class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = "__all__"
        exclude = ('m_sheet', 'correct_answer')

        widgets = {
            'my_answer': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }