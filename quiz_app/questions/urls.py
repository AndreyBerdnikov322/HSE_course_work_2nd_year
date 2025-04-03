from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('new/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('image-form/', views.add_image_form, name='add_image_form'),
    path('<int:question_pk>/images/', views.image_list, name='image_list'),
    path('<int:question_pk>/images/add/', views.add_image, name='add_image'),
    path('images/<int:pk>/delete/', views.delete_image, name='delete_image'),
    path('answers/<int:pk>/delete/', views.delete_answer, name='delete_answer'),
]