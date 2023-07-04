
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from notatki.forms import UserRegisterForm, UserLoginForm, NoteForm, NoteSearchForm
from notatki.models import UserProfile, Note, Tag

class NavBarHendler:
    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return redirect('notatki:home')
        if hasattr(super(), 'some_method'):
            return super().post(request, *args, **kwargs)
        return HttpResponse('Metoda post nie jest dostępna w klasie nadrzędnej.')


class HomeTemplateView(NavBarHendler, TemplateView):
    template_name = "notatki/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        user = UserProfile.objects.get(user=self.request.user)
        context['dane'] = (Note.objects.filter(author=user).count)
        return context


@method_decorator(login_required, name='dispatch')
class NotesList(NavBarHendler, ListView, FormView, ):
    form_class = NoteSearchForm
    success_url = reverse_lazy('notatki:notes_list')
    def get_queryset(self):
        search_title = self.request.GET.get('search_title')
        search_text = self.request.GET.get('search_text')
        encoded_tags = self.request.GET.get('search_tags')

        profile = UserProfile.objects.get(user=self.request.user)
        queryset = Note.objects.filter(author=profile)
        if search_title:
            queryset = queryset.filter(title__icontains=search_title)
        if search_text:
            queryset = queryset.filter(content__icontains=search_text)
        if encoded_tags:
            search_tags = encoded_tags.split(',')
            queryset = queryset.filter(tag__in=search_tags)
        return queryset

    def post(self, request, *args, **kwargs):
        if 'delete_selected' in request.POST:
            selected_notes = request.POST.getlist('selected_notes')
            if selected_notes:
                # Usuń zaznaczone notatki
                Note.objects.filter(id__in=selected_notes).delete()
                return redirect('notatki:notes_list')
        elif 'search' in request.POST:
            search_title = request.POST.get('search_title')
            search_text = request.POST.get('search_text')
            search_tags = request.POST.getlist('tags')
            param =''
            if search_title:
                param += f'?search_title={search_title}'
            if search_text:
                if param:
                    param += f'&search_text={search_text}'
                else:
                    param += f'?search_text={search_text}'
            if search_tags:
                encoded_tags =','.join(search_tags)
                if param:
                    param += f'&search_tags={encoded_tags}'
                else:
                    param += f'?search_tags={encoded_tags}'
            return redirect(reverse('notatki:notes_list') + param)
        return super().post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class NoteDetailView(NavBarHendler, DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = self.get_object()
        tags = Tag.objects.filter(notes=note.id)
        context['tags'] = tags
        return context
    def post(self, request, *args, **kwargs):
        if 'delete_note' in request.POST:
            self.get_object().delete()
            return redirect(reverse('notatki:notes_list'))
        return super().post(request, *args, **kwargs)

class MyLoginView(LoginView):
    form_class = UserLoginForm
    next_page = 'notatki:notes_list'
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class MyRegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('notatki:notes_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        # Tworzenie UserProfile po utworzeniu użytkownika
        UserProfile.objects.create(user=user)
        # Automatyczne logowanie użytkownika
        login(self.request, user)
        return response

@method_decorator(login_required, name='dispatch')
class NoteFormView(NavBarHendler, CreateView):

    form_class = NoteForm
    success_url = reverse_lazy('notatki:notes_list')
    def form_valid(self, form):
        instance = form.save(commit=False)
        profile = UserProfile.objects.get(user=self.request.user)
        instance.author = profile
        instance.save()
        # Pobierz wybrane tagi z formularza
        tags = form.cleaned_data['tags']

        # Dodaj notatkę do wybranych tagów
        for tag in tags:
            tag.notes.add(instance)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoteUpdateView(NavBarHendler, UpdateView):
    queryset = Note.objects.all()
    form_class = NoteForm

    def get_success_url(self):
        return reverse('notatki:details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        note = form.save(commit=False)
        note.save()

        # Pobierz wybrane tagi z formularza
        tags = form.cleaned_data['tags']

        # Dodaj notatkę do wybranych tagów
        note.tag_set.clear()
        for tag in tags:
            tag.notes.add(note)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TagsListAndForm(NavBarHendler, ListView):
    model = Tag

    def post(self, request, *args, **kwargs):
        if 'delete_selected' in request.POST:
            selected_tags = request.POST.getlist('selected_tags')
            if selected_tags:
                # Usuń zaznaczone tagi
                Tag.objects.filter(id__in=selected_tags).delete()
            return self.get(request, *args, **kwargs)
                # return reverse_lazy('notatki:tags')
        elif 'tag_name' in request.POST:
            try:
                tag_name = request.POST['tag_name']
                if tag_name:
                    Tag.objects.create(name=tag_name)
            except IntegrityError:
                # Jeśli wystąpił błąd IntegrityError, oznacza to, że tag o podanej nazwie już istnieje
                # Dodajemy komunikat do kolejki wiadomości
                messages.error(request, 'Tag o podanej nazwie już istnieje.')
            return self.get(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)