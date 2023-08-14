from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Kelas(models.Model):

    STATUS_CHOICES = (
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif'),
    )

    nama_kelas = models.CharField(max_length=10)
    status_kelas = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Aktif')
    
    def __str__(self):
        return self.nama_kelas

    class Meta:
        verbose_name_plural ="Kelas" 


class Anak(models.Model):

    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    INDIKATOR = (
        ('Iya', 'Iya'),
        ('Tidak', 'Tidak'),
    )

    STATUS = (
        ('Teratasi', 'Teratasi'),
        ('Sedang Diatasi', 'Sedang Diatasi'),
    )
    
    nama = models.CharField(max_length=200, blank=False, null=False)
    ttl = models.DateField(auto_now=False, auto_now_add=False)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, default='L')
    berat_badan = models.CharField(max_length=10, unique = False, null=False)
    tinggi_badan = models.CharField(max_length=10, unique = False, null=False)
    tanggal_operasi = models.DateField(auto_now=False, auto_now_add=False)
    indikator = models.CharField(max_length=20, choices=INDIKATOR, default='Iya')
    status = models.CharField(max_length=20, choices=STATUS, default='Teratasi')
    posyandu = models.ForeignKey(Kelas, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Anak"


class Petugas(models.Model):

    STATUS_CHOICES = (
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif'),
    )

    user = models.OneToOneField(User, blank =True, null=True, on_delete = models.CASCADE)
    nama_petugas = models.CharField(max_length=200, blank=True, null=False)
    email = models.CharField(max_length=100,blank=True, unique = True, null=False)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Aktif')
    no_telpon = models.CharField(max_length=200, blank=True,  unique = True, null=False)

    def __str__(self):
        return self.nama_petugas
    class Meta:
        verbose_name_plural = "Petugas"

