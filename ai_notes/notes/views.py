from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, FileResponse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Note, NoteFile
from django.core.files.storage import default_storage
import os
from django.utils import timezone
import json


@login_required
def main(request):
    return render(request, 'main.html')

@login_required
def save_file_view(request):
    if request.method == 'POST':
        try:
            # Получаем идентификатор заметки из данных запроса
            note_id = request.POST.get('note_id')

            uploaded_file = request.FILES['file']
            if note_id:
                # Проверяем, существует ли заметка
                note = Note.objects.get(pk=note_id)

                # Сохранение файла как оригинала и привязка к заметке
                NoteFile.objects.create(note=note, upload=uploaded_file)

                return JsonResponse({'status': 'success', 'file_name': uploaded_file.name})

        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found'}, status=404)

    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_note_view(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            user = request.user
            title = data.get('title')
            text = data.get('content', '-')
            note_id = data.get('id', None)
            print(note_id)
            if title == '':
                title = 'Без названия'
            if note_id:
                # Обновляем существующую заметку
                note = Note.objects.get(pk=note_id, user=user)
                note.title = title
                note.text = text
                note.save()
            else:
                # Создаем новую заметку
                note = Note.objects.create(
                    user=user,
                    title=title,
                    text=text,
                    date_created=timezone.now()
                )


            return JsonResponse({'status': 'success', 'note_id': note.id})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found'}, status=404)

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_notes_view(request):
    if request.method == 'GET':
        user = request.user
        notes = Note.objects.filter(user=user).order_by('-date_created')
        notes_list = []

        for note in notes:
            notes_list.append({
                'id': note.id,
                'title': note.title,
                'text': note.text,
                'date_created': note.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                # Добавляем другие необходимые данные
            })

        return JsonResponse({'notes': notes_list})

    print('error')
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_note_by_id_view(request, note_id):
    if request.method == 'GET':
        user = request.user
        try:
            note = Note.objects.prefetch_related('files').get(id=note_id, user=user)
            note_data = {
                'id': note.id,
                'title': note.title,
                'text': note.text,
                'date_created': note.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'files': [{'id': file.id, 'name': file.upload.name} for file in note.files.all()],  # Получаем файлы
            }
            return JsonResponse({'note': note_data})
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found or not accessible'}, status=404)

    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_file_view(request, file_id):
    user = request.user
    try:
        file = get_object_or_404(NoteFile, id=file_id, note__user=user)  # Проверка принадлежности файла
        return FileResponse(file.upload.open(), content_type='application/octet-stream')
    except NoteFile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'File not found or not accessible'}, status=404)


# Удаление заметки
@login_required
def delete_note_view(request, note_id):
    if request.method == 'DELETE':
        note = get_object_or_404(Note, id=note_id)

        # Проверяем принадлежит ли заметка текущему пользователю
        if note.user != request.user:
            return HttpResponseForbidden('You do not have permission to delete this note.')

        # Удаляем заметку
        note.delete()
        return JsonResponse({'success': True, 'message': 'Note deleted successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def register_and_login(request):
    if request.method == 'POST':
        # Регистрация
        if 'signupEmail' in request.POST and 'signupPassword' in request.POST:
            email = request.POST['signupEmail']
            password = request.POST['signupPassword']
            try:
                user = CustomUser.objects.create_user(email=email, password=password)
                user.save()
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)

                    return JsonResponse({'redirect_url': '/'})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    print(e)
                    return JsonResponse({'error2': 'Данная почта уже используется.'})
                else:
                    print(e)
                    return JsonResponse({'error2': 'Произошла ошибка при регистрации пользователя.'})
        # Вход
        elif 'loginEmail' in request.POST and 'loginPassword' in request.POST:
            email = request.POST['loginEmail']
            password = request.POST['loginPassword']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'redirect_url': '/'})
            else:
                # Обработка ошибки входа
                return JsonResponse({'error1': 'Неверный логин или пароль.'})
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect(register_and_login)
