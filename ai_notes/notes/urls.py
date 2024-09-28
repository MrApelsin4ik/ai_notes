from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [
    path('register_and_login/', views.register_and_login, name='register_and_login'),
    path('', views.main, name='main'),
    path('save-note/', views.save_note_view, name='save_note_view'),
    path('get-notes/', views.get_notes_view, name='get_notes_view'),
    path('get-note/<int:note_id>/', views.get_note_by_id_view, name='get_note_by_id_view'),
    path('delete-note/<int:note_id>/', views.delete_note_view, name='delete-note'),
    path('get-file/<int:file_id>/', views.get_file_view, name='get_file_view'),
    path('generate/', views.generate_view, name='generate'),
    path('update_summary_data/', views.update_summary_data, name='update_summary_data'),
    path('get_summary_data/', views.get_summary_data, name='get_summary_data'),
    path('get-generated-summary/<int:note_id>/', views.get_generated_summary_by_note_id_view, name='get_generated_summary_by_note_id_view'),
    path('get-generated-summary-file/<int:file_id>/', views.get_generated_summary_file_view, name='get_generated_summary_file_view'),
    path('save-file/', views.save_file_view, name='save_file'),
    path('logout', views.logout_view, name='logout')

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
