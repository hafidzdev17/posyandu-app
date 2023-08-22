from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from .views import SiswaAutocomplete

urlpatterns = [
    path('account/login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    # path('register/', views.registerPage, name='register'),

    # depan
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('posyandu', views.posyandu, name='posyandu'),
    path('contact', views.contact, name='contact'),
    # admin
    path('dashboard', views.beranda, name='beranda'),
    # posyandu
    path('dashboard/posyandu', views.posyandus, name='kelas'),
    path('dashboard/create_posyandu/', views.create_posyandu, name='create_kelas'),
    path('dashboard/update_posyandu/<int:pk>/', views.update_posyandu, name='update_kelas'),
    path('dashboard/delete_posyandu/<int:pk>/', views.delete_posyandu, name='delete_kelas'),

    # siswa
    path('dashboard/anak', views.anak, name='anak'),
    path('dashboard/create_anak/', views.create_anak, name='create_anak'),
    path('dashboard/update_anak/<int:pk>/', views.update_anak, name='update_anak'),
    path('dashboard/delete_anak/<int:pk>/', views.delete_anak, name='delete_anak'),

    # petugas
    path('dashboard/admin', views.petugas, name='petugas'),
    path('dashboard/create_admin', views.create_petugas, name='create_petugas'),
    path('dashboard/delete_admin/<str:pk>', views.delete_petugas, name='delete_petugas'),

    path('dashboard/laporan/', views.laporan, name='laporan'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)