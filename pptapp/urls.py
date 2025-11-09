from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_presentation, name='create_presentation'),
    path('history/', views.track_history, name='track_history'),
    path('export_excel/', views.export_excel, name='export_excel'),
    #path('download/<int:id>/', views.download_presentation, name='download_presentation'),
    path('history/download_png/<int:pk>/', views.history_download_png, name='history_download_png'),  # <-- Add this line
    path('accounts/logout/', views.user_logout, name='logout'),
]
