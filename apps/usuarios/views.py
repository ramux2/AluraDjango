from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from receitas.views import receita

def cadastro(request):
    """Register an user in database"""
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
    """Log in some user in the system"""
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
    """Log out the user in the system"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """Show the user's dashboard"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def vazio(campo):
    """Check if the field is not empty"""
    return not campo.strip()

def verifica_senhas(senha, senha2):
    """Verify if both password are the same"""
    return senha != senha2
