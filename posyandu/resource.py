from import_export import resources
from .models import Anak
from import_export.fields import Field

class PembayaranResource(resources.ModelResource):
    # nama_siswa__nama = Field(attribute='nama_siswa', column_name='Nama Siswa')
    # nisn = Field(attribute='nama_siswa__nisn', column_name='NISN')
    # kelas = Field(attribute='nama_siswa__kelas__nama_kelas', column_name='Kelas')

    class Meta:
        model = Anak
        fields = ['nama', 'ttl', 'jenis_kelamin','berat_badan','tinggi_badan', 'tanggal_operasi', 'indikator','status','posyandu']

