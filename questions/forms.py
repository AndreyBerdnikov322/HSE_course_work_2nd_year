# questions/forms.py
from django import forms
from .models import Question, QuestionType, Image
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_type'].queryset = QuestionType.objects.all()
        self.fields['question_type'].empty_label = "Выберите тип вопроса"
        self.fields['question_type'].widget.attrs.update({
            'class': 'form-select',
            'required': 'required'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текст вопроса'
        })

    class Meta:
        model = Question
        fields = ['text', 'question_type']
        labels = {
            'text': 'Текст вопроса',
            'question_type': 'Тип вопроса'
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Необязательная подпись'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логин',
        }
        help_texts = {
            'username': '',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})