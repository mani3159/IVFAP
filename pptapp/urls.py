from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_presentation, name='create_presentation'),
    path('ajax/get_constituencies/', views.get_constituencies, name='get_constituencies'),
    path('history/', views.track_history, name='track_history'),
    path('export_excel/', views.export_excel, name='export_excel'),
    #path('download/<int:id>/', views.download_presentation, name='download_presentation'),
    path('history/download_ppt/<int:pk>/', views.history_download_ppt, name='history_download_ppt'),  # <-- Add this line
    path('accounts/logout/', views.user_logout, name='logout'),
    path('history/edit/<int:pk>/', views.history_edit, name='history_edit'),
    path('history/delete/<int:pk>/', views.history_delete, name='history_delete'),
]
