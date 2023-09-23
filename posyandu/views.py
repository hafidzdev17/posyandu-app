import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.http import HttpResponse
from .filters import KelasFilter, SiswaFilter, PembayaranFilter
from .resource import PembayaranResource
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .decorators import tolakhalaman_ini
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.contrib.auth.models import User
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime  # Import modul datetime
from django.utils.dateformat import DateFormat
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def is_admin(user):
    return user.petugas.roles == 'Admin' if user.petugas else False

def is_bidan(user):
    return user.petugas.roles == 'Bidan' if user.petugas else False

@login_required
@user_passes_test(is_bidan, login_url='login')
def generate_pdf(request):
    # Mengambil data pengguna yang sedang masuk
    current_user = request.user

    try:
        petugas = Petugas.objects.get(user=current_user)
        print(f"Nama Petugas: {petugas.nama_petugas}")
        print(f"Email: {petugas.email}")
        print(f"Status: {petugas.status}")
        print(f"No Telpon: {petugas.no_telpon}")
    except Petugas.DoesNotExist:
        print("Data Petugas tidak ditemukan.")

    # Mendapatkan tanggal saat ini dan mengonversinya ke format yang diinginkan
    current_date = datetime.now()
    formatted_date = DateFormat(current_date).format("j F Y")

    # Mengambil data petugas yang terkait dengan pengguna yang sedang login
    try:
        petugas = Petugas.objects.get(user=current_user)
    except Petugas.DoesNotExist:
        petugas = None

    # Mengambil data siswa atau data lain yang ingin dicetak
    siswa = User.objects.filter(id=current_user.id)

    # Mengambil template HTML
    template = get_template('data/pdf_report.html')

    tglmulai = request.GET.get('tglmulai', '')
    tglakhir = request.GET.get('tglakhir', '')

    # Lakukan validasi dan konversi tanggal
    if not tglmulai or not tglakhir:
        # Jika salah satu atau kedua tanggal tidak ada maka dapat menentukan nilai default
        # atau mengambil seluruh data, sesuai dengan kebutuhan
        tglmulai = '1900-01-01'  # Tanggal default awal
        tglakhir = '2100-12-31'  # Tanggal default akhir
    
    # ...

    # Mendapatkan nilai filter indikator dari permintaan GET
    indikator = request.GET.get('indikator', '')

    # Setelah validasi berhasil maka dapat melanjutkan dengan menggunakan tanggal dan indikator dalam filter
    anak = Anak.objects.filter(tanggal_operasi__range=(tglmulai, tglakhir)).order_by('-id')

    # Jika indikator tidak kosong, tambahkan filter indikator ke query
    if indikator and indikator != 'Semua':
        anak = anak.filter(indikator=indikator)

        # Mengatur nilai filter berdasarkan filter indikator
    if indikator == 'Iya':
        filter_value = 'Stunting'
    elif indikator == 'Tidak':
        filter_value = 'Tidak Stunting'
    else:
        filter_value = 'Stunting Dan Tidak Stunting'  # Nilai default jika tidak ada filter indikator

    # Mengisi konteks template dengan data dan tanggal
    context = {
        'siswa': anak,
        'current_date': formatted_date,
        'petugas': petugas,
        'indikator': filter_value
    }

    html = template.render(context)

    # Menginisialisasi objek PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_report.pdf"'

    # Menentukan ukuran halaman Letter (8.5 x 11 inch)
    pdf = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        response,
        encoding='utf-8',
        link_callback=lambda uri, _: fetch_resources(uri) if uri.startswith('/') else uri
    )
    pdf.use_full_page = True

    if not pdf.err:
        return response

    return HttpResponse('Terjadi kesalahan saat membuat PDF')


# views halaman depan
def index(request):
    context = {
        'menu' : 'index',
        'page' : 'Sistem Informasi Stunting Kelurahan Candigati Jember',
    }
    return render(request, 'frontend/index.html', context)

def about(request):
    context = {
        'menu' : 'about',
        'page' : 'Posyandu Kelurahan Candigati Jember | Tentang',
    }
    return render(request, 'frontend/about.html', context)

def posyandu(request):
    context = {
        'menu' : 'posyandu',
        'page' : 'Posyandu Kelurahan Candigati Jember | Posyandu',
    }
    return render(request, 'frontend/posyandu.html', context)

def contact(request):
    context = {
        'menu' : 'contact',
        'page' : 'Posyandu Kelurahan Candigati Jember | Contact',
    }
    return render(request, 'frontend/contact.html', context)

@login_required
def beranda(request):
    
    anak = Anak.objects.all()
    total_kms =  anak.filter(indikator='Iya').count()
    total_lks = anak.filter(indikator='Tidak').count()
    total_komputer = anak.filter(status='Teratasi').count()
    total_komputers = anak.filter(status='Sedang Diatasi').count()
    total_siswa = Anak.objects.count()
    total_kelas = Kelas.objects.count()
    total_petugas = Petugas.objects.count()
  
    context = {
        'menu' : 'Beranda',
        'page' : 'Selamat Datang Di Beranda',
        'kms': total_kms,
        'lks': total_lks,
        'komputer': total_komputer,
        'komputers': total_komputers,
        'siswa' : total_siswa,
        'kelas' : total_kelas,
        'petugas' : total_petugas,
    }
    return render(request, 'data/beranda.html', context)


@tolakhalaman_ini
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda')
        else:
            messages.error(request, f"username/password salah")
            return redirect('login')
        
    context = {
        'menu': 'login',
        'page': 'Halaman Login',
        
    }
    return render(request, 'data/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


# views kelas
@login_required
def posyandus(request):
    kelas_data = Kelas.objects.all()
    context = {
        'menu' : 'Form Posyandu',
        'page' : 'Halaman Posyandu',
        'kelas' : kelas_data,
        'filter_kelas' : KelasFilter
    }
    return render(request, 'data/posyandu.html', context)

@login_required
def create_posyandu(request):
    form = KelasForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Posyandu berhasil ditambahkan.')
        return redirect('kelas')
    context = {
        'menu' : 'Tambah Posyandu',
        'page' : 'Halaman Tambah Posyandu',
        'form': form
    }
    return render(request, 'data/posyandu_form.html', context)

@login_required
def update_posyandu(request, pk):
    kelas = Kelas.objects.get(id=pk)
    form = KelasForm(request.POST or None, request.FILES or None, instance=kelas)
    if form.is_valid():
        form.save()
        messages.success(request, 'Posyandu berhasil diupdate.')
        return redirect('kelas')
    context = {
        'menu' : 'Edit Posyandu',
        'page' : 'Halaman Edit Posyandu',
        'form': form
    }
    return render(request, 'data/posyandu_form.html', context)

@login_required
def delete_posyandu(request, pk):
    kelas = Kelas.objects.get(id=pk)
    if request.method == 'POST':
        kelas.delete()
        messages.success(request, 'Posyandu berhasil dihapus.')
        return redirect('kelas')
    context = {
        'menu':'Menu Delete Kelas',
        'page':'Halaman Delete Kelas',
        'kelas': kelas
    }
    return render(request, 'data/posyandu_delete.html', context)


# views siswa
@login_required
def anak(request):
    siswa_data = Anak.objects.order_by('-id')
    context = {
        'menu' : 'Form Anak',
        'page' : 'Halaman Anak',
        'siswa' : siswa_data,
        'filter_siswa' : SiswaFilter
    }
    return render(request, 'data/anak.html', context)

@login_required
def create_anak(request):
    form = AnakForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Anak Berhasil Ditambahkan.')
        return redirect('anak')
    context = {
        'menu' : 'Tambah Anak',
        'page' : 'Halaman Tambah Anak',
        'form': form
    }
    return render(request, 'data/anak_form.html', context)


@login_required
def update_anak(request, pk):
    anak = Anak.objects.get(id=pk)
    form = AnakForm(request.POST or None, request.FILES or None, instance=anak)
    if form.is_valid():
        form.save()
        messages.success(request, 'Anak berhasil diupdate.')
        return redirect('anak')
    context = {
        'menu' : 'Edit Anak',
        'page' : 'Halaman Edit Anak',
        'form': form
    }
    return render(request, 'data/anak_form.html', context)

@login_required
def delete_anak(request, pk):
    anak = Anak.objects.get(id=pk)
    if request.method == 'POST':
        anak.delete()
        messages.success(request, 'Anak berhasil dihapus.')
        return redirect('anak')
    context = {
        'menu':'Menu Delete Anak',
        'page':'Halaman Delete Anak',
        'siswa': anak
    }
    return render(request, 'data/anak_delete.html', context)

# petugas

@login_required
@user_passes_test(is_admin, login_url='login')
def petugas(request):
    data = Petugas.objects.order_by('-id')
    context ={
        "menu" : 'Admin',
        "page" : 'Halaman Admin',
        'petugas' : data
    }
    return render(request, 'data/petugas.html', context)

@login_required
@user_passes_test(is_admin, login_url='login')
def create_petugas(request):
    form = PetugasForm()
    petugas = PetugasForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).first():
            messages.success(request, 'Username sudah ada.')
            return redirect('create_petugas')

        if password1 != password2:
            messages.success(request, 'Password Tidak sama')
            return redirect('create_petugas')

        # user
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        user.is_active = True
        user.save()

        # Petugas
        createPetugas = petugas.save(commit=False)
        createPetugas.user = user  # Mengaitkan objek Petugas dengan pengguna yang sedang login
        createPetugas.save()
        messages.success(request, 'admin berhasil ditambahkan.')

        return redirect('petugas')

    context = {
        "menu": 'Input Admin',
        "page": 'Halaman Admin',
        "form": form
    }
    return render(request, 'data/petugas_form.html', context)


@login_required
@user_passes_test(is_admin, login_url='login')
def delete_petugas(request, pk):
    delete_petugas = Petugas.objects.get(id=pk)
    if request.method == 'POST':
        delete_petugas.delete()
        messages.success(request, 'admin berhasil dihapus.')
        return redirect ('petugas')
    context = {
        'menu':'Menu Delete Admin',
        'page':'Halaman Delete Admin',
        'petugas': delete_petugas
    }
    return render(request, 'data/petugas_delete.html', context)

@login_required
@user_passes_test(is_bidan, login_url='login')
def laporan(request):
    pembayaran = Anak.objects.order_by('-id')
    filterpembayaran = PembayaranFilter(request.GET, queryset=pembayaran)
    filter_pel = filterpembayaran.qs

    # Mendapatkan nilai filter indikator dari permintaan GET
    indikator = request.GET.get('indikator', '')

    context = {
        'menu': 'laporan',
        'page': 'Halaman Laporan',
        'filter_pln': filterpembayaran,
        'siswa': filter_pel,
        'filter_indikator': indikator,
    }

    return render(request, 'data/formlaporan.html', context)



