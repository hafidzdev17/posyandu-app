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
# Create your views here.

class SiswaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Siswa.objects.none()

        qs = Siswa.objects.all()

        if self.q:
            qs = qs.filter(nama__istartswith=self.q)

        return qs

def getfoto(request):
    santri = Santri.objects.get(id=request.GET.get('pk'))
    foto = santri.foto.name
    return HttpResponse(foto)

def telegram_bot(chat_id, message):
    # https://api.telegram.org/bot1837414090:AAEd-MMi0Z_NYxkHdNsQTbMNyhndwQCJycY/getUpdates
    bot_token = '1837414090:AAH5AB4hR_oX1xbDMsPs7F5N0RsimoLkFCY'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=HTML&text=' + message
    response = requests.get(send_text)
    return response.json()

# @ijinkan_pengguna(yang_diizinkan=['admin']) 
# @login_required(login_url='login')
def export_xls(request):
    pln = PembayaranResource()
    dataset = pln.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=pelangaran.xls'
    return response


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
def kelas(request):
    kelas_data = Kelas.objects.all()
    context = {
        'menu' : 'Form Posyandu',
        'page' : 'Halaman Posyandu',
        'kelas' : kelas_data,
        'filter_kelas' : KelasFilter
    }
    return render(request, 'data/kelas.html', context)

@login_required
def create_kelas(request):
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
    return render(request, 'data/kelas_form.html', context)

@login_required
def update_kelas(request, pk):
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
    return render(request, 'data/kelas_form.html', context)

@login_required
def delete_kelas(request, pk):
    kelas = Kelas.objects.get(id=pk)
    if request.method == 'POST':
        kelas.delete()
        messages.success(request, 'Kelas berhasil dihapus.')
        return redirect('kelas')
    context = {
        'menu':'Menu Delete Kelas',
        'page':'Halaman Delete Kelas',
        'kelas': kelas
    }
    return render(request, 'data/kelas_delete.html', context)


# views siswa
@login_required
def siswa(request):
    siswa_data = Anak.objects.order_by('-id')
    context = {
        'menu' : 'Form Anak',
        'page' : 'Halaman Anak',
        'siswa' : siswa_data,
        'filter_siswa' : SiswaFilter
    }
    return render(request, 'data/siswa.html', context)

@login_required
def create_siswa(request):
    form = AnakForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Anak Berhasil Ditambahkan.')
        return redirect('siswa')
    context = {
        'menu' : 'Tambah Anak',
        'page' : 'Halaman Tambah Anak',
        'form': form
    }
    return render(request, 'data/siswa_form.html', context)


@login_required
def update_siswa(request, pk):
    siswa = Anak.objects.get(id=pk)
    form = AnakForm(request.POST or None, request.FILES or None, instance=siswa)
    if form.is_valid():
        form.save()
        messages.success(request, 'Anak berhasil diupdate.')
        return redirect('siswa')
    context = {
        'menu' : 'Edit Anak',
        'page' : 'Halaman Edit Anak',
        'form': form
    }
    return render(request, 'data/siswa_form.html', context)

@login_required
def delete_siswa(request, pk):
    siswa = Anak.objects.get(id=pk)
    if request.method == 'POST':
        siswa.delete()
        messages.success(request, 'Anak berhasil dihapus.')
        return redirect('siswa')
    context = {
        'menu':'Menu Delete Anak',
        'page':'Halaman Delete Anak',
        'siswa': siswa
    }
    return render(request, 'data/siswa_delete.html', context)

@login_required
# petugas
def petugas(request):
    data = Petugas.objects.order_by('-id')
    context ={
        "menu" : 'Admin',
        "page" : 'Halaman Admin',
        'petugas' : data
    }
    return render(request, 'data/petugas.html', context)

@login_required
def create_petugas(request):
    form = PetugasForm()
    petugas = PetugasForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username = username).first():
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
        createPetugas = petugas.save()
        createPetugas.user = user
        createPetugas.save()
        messages.success(request, 'admin berhasil ditambahkan.')
        
        return redirect('petugas')

    context ={
        "menu" : 'Input Admin',
        "page" : 'Halaman Admin',
        "form" : form
        
    }
    return render(request, 'data/petugas_form.html', context)

@login_required
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


def laporan(request):
    pembayaran = Anak.objects.order_by('-id')
    filterpembayaran = PembayaranFilter(request.GET, queryset=pembayaran)
    filter_pel = filterpembayaran.qs
    context = {
        'menu' : 'laporan',
        'page' : 'Halaman Laporan',
        'filter_pln' : filterpembayaran,
        'siswa' : filter_pel,
    }
    return render(request, 'data/formlaporan.html', context)    
