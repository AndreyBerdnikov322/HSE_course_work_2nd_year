# questions/forms.py
from django import forms
from .models import Question, QuestionType, Image

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Принудительно обновляем queryset
        self.fields['question_type'].queryset = QuestionType.objects.all()
        self.fields['question_type'].empty_label = "Выберите тип вопроса"
    
    class Meta:
        model = Question
        fields = ['text', 'question_type']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Необязательная подпись'}),
        }