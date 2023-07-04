from django.contrib.auth.views import LoginView
from django.urls import path
from notatki import views
from notatki.views import MyLoginView, MyRegisterView, NotesList

app_name = 'notatki'  #przestrzen nazw aplikacji
urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path('notatki/', views.NotesList.as_view(template_name='notatki/list.html'), name='notes_list'),
    path('notatki/<int:pk>', views.NoteDetailView.as_view(template_name='notatki/details.html'), name='details'),
    path('notatki/note_form', views.NoteFormView.as_view(template_name='notatki/noteform.html'), name='note_form'),
    path('notatki/note_form/<int:pk>', views.NoteUpdateView.as_view(template_name='notatki/noteform.html'), name='note_edit'),
    path('tags', views.TagsListAndForm.as_view(template_name='notatki/tags.html'), name='tags'),
    path('login', MyLoginView.as_view(template_name='notatki/login.html'), name='login'),
    path('register', MyRegisterView.as_view(template_name='notatki/register.html'), name='register'),
    path('logout', MyRegisterView.as_view(template_name='notatki/register.html'), name='logout'),
]