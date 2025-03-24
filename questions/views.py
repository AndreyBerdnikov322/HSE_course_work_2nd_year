from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from .forms import QuestionForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, "questions/list.html", {'questions': questions})

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('question-list')
    else:
        form = QuestionForm()
    return render(request, 'questions/add_question.html', {'form': form})

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('question-list')
    return render(request, 'questions/confirm_delete.html', {'question': question})

@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question-list')
    else:
        form = QuestionForm(instance=question)    
    return render(request, 'questions/edit_question.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'questions/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'questions/edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('question-list')
    else:
        form = RegisterForm()
    return render(request, 'questions/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'questions/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте имя пользователя и пароль')
        return super().form_invalid(form)

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'question-list'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы успешно вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/add_question.html'
    success_url = reverse_lazy('question-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)