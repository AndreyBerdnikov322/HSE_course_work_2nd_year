from django.shortcuts import render
from .models import Question

# Create your views here.
def question_list(request):
    questions = Question.objects.all()
    return render(request, "questions/list.html", {'questions': questions})