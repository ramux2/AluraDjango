from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from receitas.views import receita

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if vazio(nome):
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('cadastro')

        if vazio(email):
            messages.error(request, 'Email não pode ficar em branco')
            return redirect('cadastro')

        if vazio(senha):
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('cadastro')

        if verifica_senhas(senha, senha2):
            messages.error(request, 'As senhas não coincidem')
            return redirect('cadastro')

        if User.objects.filter(email = email).exists():
            messages.error(request, 'E-mail já cadastrado')
            return redirect('cadastro')

        if User.objects.filter(username = nome).exists():
            messages.error(request, 'E-mail já cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro feito com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        
        if email == '' or senha == '':
            messages.error(request, 'Os campos E-mail e Senha não podem ser vazios')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')
        
def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user,nome_receita=nome_receita,ingredientes=ingredientes,modo_preparo=modo_preparo,tempo_preparo=tempo_preparo,rendimento=rendimento,categoria=categoria,foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_editar = {
        'receita' : receita
    }
    return render(request, 'usuarios/edita_receita.html', receita_editar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')

def vazio(campo):
    return not campo.strip()

def verifica_senhas(senha, senha2):
    return senha != senha2
