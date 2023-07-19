from django import forms
from django.forms import ModelForm, DateTimeInput
from .models import *


class KelasForm(ModelForm):
    class Meta:
        model = Kelas
        fields= '__all__'
    
        widgets = {
            'nama_kelas': forms.TextInput(attrs={'class': 'form-select'}),
            'status_kelas': forms.TextInput(attrs={'class': 'form-select'}),
        }
        labels = {
            'nama_kelas' : 'Nama Kelas',
            'status_kelas': 'Status Kelas',
        }

class SiswaForm(ModelForm):
    class Meta:
        model = Siswa
        fields= '__all__'
    
        widgets = {
            'kelas': forms.Select(attrs={'class': 'form-select'}),
            'nama': forms.TextInput(attrs={'class': 'form-select'}),
            'nisn': forms.TextInput(attrs={'class': 'form-select'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'ttl': forms.DateInput(format = '%m-%d-%Y',attrs={'type': 'date'}),
            'tahun_akademik': forms.TextInput(attrs={'class': 'form-select'}),
        }
        labels = {
            'kelas': 'Kelas',
            'nama' : 'Nama Lengkap',
            'nisn': 'NISN',
            'alamat' : 'Alamat',
            'ttl': 'Tanggal lahir',
            'tahun_akademik' : 'Tahun Akademik',
        }

class PengurusForm(ModelForm):

    class Meta:
        model = Pengurus
        fields = '__all__'
        exclude = ['user']
        labels = {
            'nama_pengurus' : 'Nama Pengurus',
            'staff' : 'Bagian',
            'no_telpon' : 'Nomer telepon',
        }