from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Kelas)
admin.site.register(Siswa)
admin.site.register(Pengurus)
admin.site.register(Pelanggaran)
admin.site.register(Pembayaran)