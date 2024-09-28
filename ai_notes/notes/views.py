from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, FileResponse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Note, NoteFile, GeneratedSummary, GeneratedSummaryFile
from django.core.files.storage import default_storage
import os
from django.utils import timezone
import json
import base64

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

            print('note', note_id)
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


@login_required
def get_generated_summary_by_note_id_view(request, note_id):
    if request.method == 'GET':
        user = request.user
        try:
            summaries = GeneratedSummary.objects.prefetch_related('summary_files').get(id=note_id)
            summary_data = [
                {
                    'id': summary.id,
                    'summary_text': summary.summary_text,
                    'thesis_plan': summary.thesis_plan,
                    'test_text': summary.test_text,
                    'files': [{'id': file.id, 'name': file.upload.name} for file in GeneratedSummary.files.all()],
                } for summary in summaries
            ]
            return JsonResponse({'summaries': summary_data})
        except GeneratedSummary.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found or not accessible'}, status=404)

    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_generated_summary_file_view(request, file_id):

    try:
        summary_file = get_object_or_404(GeneratedSummaryFile, id=file_id)
        return FileResponse(summary_file.upload.open(), content_type='application/octet-stream')
    except GeneratedSummaryFile.DoesNotExist:
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


def generate_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        note_id = data.get('note_id')
        summary = data.get('summary', False)
        outline = data.get('outline', False)
        test = data.get('test', False)

        try:
            note = Note.objects.get(id=note_id)
            summary, created = GeneratedSummary.objects.update_or_create(
                note=note,
                defaults={
                    'summary': summary,
                    'outline': outline,
                    'test': test,

                }
            )

            if created:
                message = 'Данные успешно сохранены!'
            else:
                message = 'Данные успешно обновлены!'

            return JsonResponse({'success': True, 'message': message})
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Заметка не найдена!'})

    return JsonResponse({'success': False, 'message': 'Неверный метод запроса!'})


key = '@]p$}&/IaF0g7?jl?@8+AdK!dj,@9AxY:'

def get_summary_data(request):
    global key
    if request.method == 'POST':
        data = json.loads(request.body)
        api_key = data.get('key')

        # Замените 'your_predefined_key' на ваш фактический ключ
        if api_key == key:
            summary = (GeneratedSummary.objects.filter(summary=True).first() or
                       GeneratedSummary.objects.filter(outline=True).first() or
                       GeneratedSummary.objects.filter(test=True).first())

            if summary:
                note = summary.note
                files = [base64.b64encode(file.upload.read()).decode('utf-8') for file in note.files.all()]
                file_names = [file.upload.name for file in note.files.all()]

                response_data = {
                    'note_id': note.id,
                    'summary': summary.summary,
                    'outline': summary.outline,
                    'test': summary.test,
                    'note_text': note.text,
                    'files': files,
                    'file_names': file_names
                }
                return JsonResponse(response_data)

            return JsonResponse({'error': 'No valid summaries found'}, status=404)
    elif request.method == "GET":
        return render(request, 'csrf_html.html')
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_summary_data(request):
    global key
    if request.method == 'POST':
        data = json.loads(request.body)
        api_key = data.get('key')

        # Замените 'your_predefined_key' на ваш фактический ключ
        if api_key == key:
            note_id = data.get('id')
            summary_text = data.get('summary_text')
            thesis_plan = data.get('thesis_plan')
            test_text = data.get('test_text')
            files = data.get('files', [])

            try:
                note = Note.objects.get(id=note_id)
                summary, created = GeneratedSummary.objects.get_or_create(note=note)

                if summary_text is not None:
                    summary.summary_text = summary_text
                if thesis_plan is not None:
                    summary.thesis_plan = thesis_plan
                if test_text is not None:
                    summary.test_text = test_text

                summary.summary, summary.outline, summary.test = False, False, False

                # Очистка старых файлов
                GeneratedSummaryFile.objects.filter(note=note).delete()

                # Сохранение новых файлов
                for file in files:
                    GeneratedSummaryFile.objects.create(note=note, upload=file)

                summary.save()

                return JsonResponse({'message': 'Summary updated successfully'}, status=200)

            except Note.DoesNotExist:
                return JsonResponse({'error': 'Note not found'}, status=404)
    elif request.method == "GET":
        return render(request, 'csrf_html.html')
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def logout_view(request):
    logout(request)
    return redirect(register_and_login)
