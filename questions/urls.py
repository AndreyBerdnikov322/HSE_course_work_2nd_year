from django.urls import path
from . import views
from .views import profile, edit_profile

urlpatterns = [
    path("", views.question_list, name="question-list"),
    path('add/', views.add_question, name='add-question'),
    path('delete/<int:pk>/', views.delete_question, name='delete-question'),
    path('edit/<int:pk>/', views.edit_question, name='edit-question'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/edit/', edit_profile, name='edit-profile'),
]