from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Question, QuestionType, Image, Answer
from django.http import HttpResponse
from .forms import QuestionForm, ImageForm
from django.forms import inlineformset_factory
from django.views.generic import UpdateView
# Create your views here.

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'questions/question_detail.html', {'question': question})

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AnswerFormSet = inlineformset_factory(Question, Answer, fields=('text', 'is_correct'), extra=1)
        
        if self.request.POST:
            context['answer_formset'] = AnswerFormSet(self.request.POST)
        else:
            context['answer_formset'] = AnswerFormSet()
            
        # Добавляем пустой список изображений для создания
        context['existing_images'] = []
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        answer_formset = context['answer_formset']
        
        if answer_formset.is_valid():
            self.object = form.save()
            answer_formset.instance = self.object
            answer_formset.save()
            
            # Обработка изображений
            images = self.request.FILES.getlist('new_images')
            captions = self.request.POST.getlist('new_captions')
            
            for image, caption in zip(images, captions):
                if image:  # Проверяем, что файл был загружен
                    Image.objects.create(
                        question=self.object,
                        image=image,
                        caption=caption
                    )
            
            return redirect('question_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AnswerFormSet = inlineformset_factory(Question, Answer, fields=('text', 'is_correct'), extra=1)
        
        if self.request.POST:
            context['answer_formset'] = AnswerFormSet(self.request.POST, instance=self.object)
        else:
            context['answer_formset'] = AnswerFormSet(instance=self.object)
            
        # Добавляем существующие изображения
        context['existing_images'] = self.object.images.all()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        answer_formset = context['answer_formset']
        
        if answer_formset.is_valid():
            self.object = form.save()
            answer_formset.instance = self.object
            answer_formset.save()
            
            # Обработка новых изображений
            images = self.request.FILES.getlist('new_images')
            captions = self.request.POST.getlist('new_captions')
            
            for image, caption in zip(images, captions):
                if image:
                    Image.objects.create(
                        question=self.object,
                        image=image,
                        caption=caption
                    )
            
            # Удаление изображений, помеченных на удаление
            deleted_images = self.request.POST.getlist('delete_images')
            for image_id in deleted_images:
                try:
                    image = Image.objects.get(pk=image_id, question=self.object)
                    image.delete()
                except Image.DoesNotExist:
                    pass
            
            messages.success(self.request, "Вопрос успешно обновлен!")
            return redirect('question_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        answer.delete()
        return HttpResponse(status=204)
    return render(request, 'questions/answer_confirm_delete.html', {'answer': answer})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        if request.headers.get('HX-Request'):
            return HttpResponse(status=204)
        messages.success(request, "Вопрос успешно удален!")
        return redirect('question_list')
    
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

def add_image(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        images = request.FILES.getlist('new_images')
        captions = request.POST.getlist('new_captions')
        
        for image, caption in zip(images, captions):
            if image:
                if image.size > 5*1024*1024:
                    messages.error(request, f"Файл {image.name} слишком большой (макс. 5MB)")
                    continue
                
                Image.objects.create(
                    question=question,
                    image=image,
                    caption=caption
                )
        
        if not images:
            messages.error(request, "Необходимо выбрать хотя бы один файл")
        else:
            messages.success(request, "Изображения успешно добавлены!")
        
        return redirect('question_update', pk=question.pk)
    
    return HttpResponse(status=405)  # Method Not Allowed

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

def add_image_form(request):
    """Возвращает HTML-форму для добавления изображения"""
    return render(request, 'questions/partials/image_form.html')

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

