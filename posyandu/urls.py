from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from .views import SiswaAutocomplete

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('accounts/login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    # path('register/', views.registerPage, name='register'),

    # posyandu
    path('posyandu', views.kelas, name='kelas'),
    path('create_posyandu/', views.create_kelas, name='create_kelas'),
    path('update_posyandu/<int:pk>/', views.update_kelas, name='update_kelas'),
    path('delete_posyandu/<int:pk>/', views.delete_kelas, name='delete_kelas'),

    # siswa
    path('anak', views.siswa, name='siswa'),
    path('create_anak/', views.create_siswa, name='create_siswa'),
    path('update_anak/<int:pk>/', views.update_siswa, name='update_siswa'),
    path('delete_anak/<int:pk>/', views.delete_siswa, name='delete_siswa'),

    # petugas
    path('admin', views.petugas, name='petugas'),
    path('create_admin', views.create_petugas, name='create_petugas'),
    path('delete_admin/<str:pk>', views.delete_petugas, name='delete_petugas'),

    path('laporan/', views.laporan, name='laporan'),
    path('getfoto/', views.getfoto, name='getfoto'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)