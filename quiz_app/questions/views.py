from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Question, QuestionType, Image, Answer
from django.http import HttpResponse
from .forms import QuestionForm 

# Create your views here.

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'questions/question_detail.html', {'question': question})

class QuestionCreateView(SuccessMessageMixin, CreateView):
    model = Question
    fields = ['text', 'question_type']
    template_name = 'questions/question_form.html'
    success_message = "Вопрос успешно создан!"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})


class QuestionUpdateView(SuccessMessageMixin, UpdateView):
    model = Question
    fields = ['text', 'question_type']
    template_name = 'questions/question_form.html'
    success_message = "Вопрос успешно обновлен!"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})

def add_image_form(request):
    return render(request, 'questions/partials/image_form.html')

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Вопрос успешно удален!")
        return HttpResponse(status=204, headers={'HX-Redirect': reverse('question_list')})
    
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

def add_image(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            # Проверка размера файла (не более 5MB)
            if image_file.size > 5*1024*1024:
                messages.error(request, "Файл слишком большой (макс. 5MB)")
            else:
                Image.objects.create(
                    question=question,
                    image=image_file,
                    caption=request.POST.get('caption', '')
                )
                messages.success(request, "Изображение успешно загружено!")
        else:
            messages.error(request, "Необходимо выбрать файл")
    return redirect('question_detail', pk=question.pk)

def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        image.delete()
        return HttpResponse(status=204, headers={'HX-Trigger': 'imageListChanged'})
    return render(request, 'questions/image_confirm_delete.html', {'image': image})

def image_list(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    images = question.images.all()
    return render(request, 'questions/image_list.html', {'images': images, 'question': question})

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            
            # Обработка изображений
            for image, caption in zip(
                request.FILES.getlist('images'),
                request.POST.getlist('image_captions')
            ):
                if image:  # Проверяем, что файл был загружен
                    Image.objects.create(
                        question=question,
                        image=image,
                        caption=caption
                    )
            
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    
    question_types = QuestionType.objects.all()
    return render(request, 'questions/question_form.html', {
        'form': form,
        'question_types': question_types
    })
