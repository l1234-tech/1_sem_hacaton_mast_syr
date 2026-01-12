from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    NoteListView, NoteDetailView, NoteCreateView,
    NoteUpdateView, NoteDeleteView, CustomLoginView
)

urlpatterns = [
    # Аутентификация
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Заметки
    path('', NoteListView.as_view(), name='note_list'),
    path('search/', views.note_search, name='note_search'),  # ← ДОБАВЛЕНО
    path('note/new/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]