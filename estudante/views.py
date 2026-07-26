import json

from django.core.handlers.base import reset_urlconf
from django.db.models import Model
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from fontTools.misc.cython import returns
from weasyprint import HTML
from .models import (SistemaProfessor, Estudante, Professor, Funcionario, PEI,
                     FuncionarioEstudante, Diagnostico, HistoricoEscolar,
                     PerfilEstudante, Atividade, Planejamento, HabilidadeAcademica,
                     Checklist, Usuario)
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import (Pei, EquipePei, FormularioDiagnostico, FormularioHistoricoEscolar,
                    FormularioPerfilEstudante, FormularioChecklist, FormularioAtividade,
                    FormularioPlanejamento, FormularioHabilidadeAcademica, FormularioPlanejamento, FormularioHabilidadeAcademica,
                    FormularioProfessor, FormularioFuncionario, FormularioEstudante,
                    EquipePei1)

from django.core.paginator import Paginator
                    

# Create your views here.

def cadastro(request):
    return render(request, 'index.html')

def cadastro_sistema(request):
    # verifica se o método da requisição é GET,
    # se for GET renderiza a pagina sistema cadastro
    if request.method == "GET":
        return render(request, 'sistema_cadastro.html')
    #verifica se o método da requisição é POST
    if request.method == "POST":
        #pega os dados da requisicao
        cpf  = request.POST.get("cpf")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        email = email.lower()
        senha = request.POST.get("senha")
        #verifica se ja tem um usuario com cpf
        if Usuario.objects.filter(cpf=cpf).exists():
            #envia mensagem de error e redireciona para pagina de cadastro sistema
            messages.error(request, "cpf ja cadastrado", extra_tags="danger")
            return redirect("cadastro_sistema")
        if Usuario.objects.filter(email=email).exists():
            # envia mensagem de error e redireciona para pagina de cadastro sistema
            messages.error(request, "email ja cadastrado", extra_tags="danger")
            return redirect("cadastro_sistema")
        usuario = Usuario.objects.create_superuser(username=email, email=email, first_name=nome , cpf=cpf, password=senha)
        professor = SistemaProfessor.objects.create(usuario=usuario)
        if professor:
            #envia mensagem de usuário cadastrado e redireciona para página de login
            messages.success(request, "O usuario foi cadastrado")
            return redirect("login1")
        #se o sistema professor não foi cadastrado, envia mensagem de usuário não cadastrado,
        #com a tag danger para ser usada pelo bootstrap e redireciona para página de cadastro
        messages.error(request, "O usuario não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_sistema")

def login1(request):
    #verifica se o usuario esta autenticado e redireciona para o painel do admnistrador
    if request.user.is_authenticated:
        return redirect("painel_administrador")
    # verifica se o método da requisição é GET,
    # se for GET renderiza a pagina sistema cadastro
    if request.method == "GET":
        return render(request, 'login.html')
     # verifica se o método da requisição é POST
    if request.method == "POST":
        #pega os dados da requisicao
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        email = email.lower()
        #verifica se o email e a senha estam corretos
        usuario = auth.authenticate(request, username=email, password=senha)
        #verifica se o usuario foi autenticado
        if usuario:
            #faz o login
            auth.login(request, usuario)
            #redireciona para pagina painel administrador
            return redirect("painel_administrador")
        #envia mensagem de error e retornar para pagina de login
        messages.error(request, "login não realizado", extra_tags="danger")
        return redirect("login1")

#apaga os dados armazenados na sessão e redireciona para a página de login
@login_required(login_url="login1")
def sair(request):
    auth.logout(request)
    return redirect("login1")

@login_required(login_url="login1")
def painel_administrador(request):
    if request.method == "GET":
        estudantes = Estudante.objects.all().order_by("nome")
        paginas = Paginator(estudantes,
                            9)  # isso aqui faz a divisão da quantidade de estudantes em tabelas de 9 em 9, ou menos
        pagina = request.GET.get(
            "page")  # isso aqui é para saber qual paginas entre, as divisões feitas, foi pedida pelo user

        estudantes = paginas.get_page(pagina)  # coloca os estudantes divididos na variavel estudante

        return render(request, "painel_administrador.html", {
            'nome': request.user.first_name,
            "total_estudantes": Estudante.objects.count(),
            "total_peis": PEI.objects.count(),
            "estudantes": estudantes})

#verifica se o usuario esta logado
@login_required(login_url="login1")
def cadastro_estudante(request):
    if request.method == "GET":
        return render(request, 'cadastro_estudante.html')
    if request.method == "POST":
        # pega os dados da requisição
        cpf = request.POST.get("cpf")
        matricula = request.POST.get("matricula")
        nome = request.POST.get("nome")
        data_de_nascimento = request.POST.get("data_de_nascimento")
        curso = request.POST.get("curso")
        periodo = request.POST.get("periodo")
        turma = request.POST.get("turma")
        ingresso = request.POST.get("ingresso")
        nota = request.POST.get("nota")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")
        pai = request.POST.get("pai")
        mae = request.POST.get("mae")
        telefone_responsavel = request.POST.get("telefone_responsavel")
        email_responsavel = request.POST.get("email_responsavel")
        email = email.lower()
        #verifica se o email ja esta cadastrado
        if Estudante.objects.filter(matricula=matricula).exists():
            #envia mensagem de error e redireciona para pagina de cadastro
            messages.error(request, "matricula ja cadastrado", extra_tags="danger")
            return redirect("cadastro_estudante")
        #verifica se o cpf ja esta cadastrado
        if Estudante.objects.filter(cpf=cpf).exists():
            #envia mensagem de error e redireciona para pagina de cadastro
            messages.error(request, "cpf ja cadastrado", extra_tags="danger")
            return redirect("cadastro_estudante")
        #verifica se o email ja esta cadastrado
        if Estudante.objects.filter(email=email).exists():
            #envia mensagem de error e redireciona para pagina de cadastro
            messages.error(request, "email ja cadastrado", extra_tags="danger")
            return redirect("cadastro_estudante")
        #cadastra o estudante
        estudante = Estudante.objects.create(cpf=cpf, matricula=matricula, nome=nome,
                                 data_de_nascimento=data_de_nascimento, curso=curso,
                                 periodo=periodo, turma=turma, ingresso=ingresso,
                                 nota=nota, telefone=telefone, email=email, pai=pai, mae=mae,
                                 telefone_responsavel=telefone_responsavel,
                                 email_responsavel=email_responsavel)
        #verifica se o estudante foi cadastrado
        if estudante:
            #envia mensagem de sucesso e redireciona para página de cadastro
            messages.success(request, "estudante cadastrado")
            return redirect("cadastro_estudante")
        #envia uma mensagem de error e redireciona para página de cadastro
        messages.error(request, "estudante não cadastrado", extra_tags="danger")
        return redirect("cadastro_estudante")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def cadastro_professor(request):
    if request.method == "GET":
        return render(request, 'cadastro_professor.html')
    if request.method == "POST":
        # pega os dados da requisição
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        data_de_nascimento = request.POST.get("data_de_nascimento")
        email = request.POST.get("email")
        email = email.lower()
        telefone = request.POST.get("telefone")
        #verifica se a matricula ja esta cadastrado
        if Professor.objects.filter(matricula=matricula).exists():
            #envia mensagem de error e redireciona para pagina de cadastro professor
            messages.error(request, "matricula ja cadastrada", extra_tags="danger")
            return redirect("cadastro_professor")
        # verifica se a cpf ja esta cadastrado
        if Professor.objects.filter(cpf=cpf).exists():
            # envia mensagem de error e redireciona para pagina de cadastro professor
            messages.error(request, "cpf ja cadastrado", extra_tags="danger")
            return redirect("cadastro_professor")
        # verifica se a email ja esta cadastrado
        if Professor.objects.filter(email=email).exists():
            # envia mensagem de error e redireciona para pagina de cadastro professor
            messages.error(request, "email ja cadastrado", extra_tags="danger")
            return redirect("cadastro_professor")
        # senao tem professor cadastrado, cadastra o professor
        professor = Professor.objects.create(cpf=cpf, nome=nome, matricula=matricula,
                                            data_de_nascimento=data_de_nascimento, email=email,
                                            telefone=telefone)
        # verifica se tem um professor
        if professor:
            # se o professor foi cadastrado, envia mensagem de sucesso e redireciona para
            # página de cadastro
            messages.success(request, "professor cadastrado")
            return redirect("cadastro_professor")
        # senão tem professor cadastrado envia mensagem de error e redireciona para
        # página de cadastro
        messages.error(request, "professor não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_professor")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def cadastro_funcionario(request):
    if request.method == "GET":
        return render(request, 'cadastro_funcionario.html')
    if request.method == "POST":
        # pega os dados da requisição
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        funcao = request.POST.get("funcao")
        if Funcionario.objects.filter(cpf=cpf).exists():
            #se tem um funcionario, envia mensagem de error de funcionario ja cadastrado
            messages.error(request, "o funcionario ja cadastrado", extra_tags="danger")
            return redirect("cadastro_funcionario")
        #cria um funcionario
        funcionario = Funcionario.objects.create(cpf=cpf, nome=nome, funcao=funcao)
        #verifica se o funcionario foi cadastrado
        if funcionario:
            #se o funcionario foi cadastrado envia mensagem de funcionario cadastrado
            #e redireciona para página de cadastro
            messages.success(request, "o funcionario foi cadastrado")
            return redirect("cadastro_funcionario")
        #se o funcionario não foi cadastrado envia mensagem de funcionario não cadastrado
        #e redireciona para página de cadastro
        messages.error(request, "o funcionario não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_funcionario")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def pei(request):
    #verifica se o método da requisição é GET
    if request.method == "GET":
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #pega todos os professores do banco de dados
        professor = Professor.objects.all()
        #cria um dicionário com os estudantes e professores
        dicionario = {"estudantes":estudante, "professores":professor}
        #renderiza a pagina e envia o dicionario para a pagina
        return render(request, 'PEI.html', dicionario)
    if request.method == "POST":
        #pega a matrícula 1 da requisição
        matricula1 = request.POST.get("matricula1")
        #verifica se tem dado na matrícula 1
        if matricula1:
            #se tiver renderiza a pagina enviando a matrícula 1, para ser usada na pagina
            #como value da matrícula do estudante, para ficar preenchida
            dicionario = {"matricula1":matricula1}
            return render(request, "PEI.html", dicionario)
        # pega os dados da requisição
        matricula_estudante = request.POST.get("matricula_estudante")
        matricula_professor = request.POST.get("matricula_professor")
        validade = request.POST.get("validade")
        #filtra professor e estudante pela matrícula e pega o primeiro
        estudante = Estudante.objects.filter(matricula = matricula_estudante).first()
        professor = Professor.objects.filter(matricula = matricula_professor).first()
        #verifica se tem professor e estudante
        if estudante and professor:
            #verifica se tem pei
            if PEI.objects.filter(estudante=estudante).exists():
                #se o pei estiver cadastrado envia mensagem de error e
                #redireciona para página do pei
                messages.error(request, "o pei ja cadastrado", extra_tags="danger")
                return redirect("pei")
            #cria o pei com os dados da requisição, envia mensagem de pei cadastrado e
            # redireciona para página do pei
            PEI.objects.create(estudante=estudante, professor=professor, tempo=validade)
            messages.success(request, "o pei foi cadastrado")
            return redirect("pei")
        #envia mensagem de error e redireciona para página do pei
        messages.error(request, "o pei não foi cadastrado", extra_tags="danger")
        return redirect("pei")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def cadastro_equipe(request):
    if request.method == "GET":
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #pega todos os funcionarios do banco de dados
        funcionario = Funcionario.objects.all()
        dicionario = {"estudantes":estudante, "funcionarios":funcionario}
        return render(request, 'cadastro_equipe.html', dicionario)
    #verifica se o método da requisição é post
    if request.method == "POST":
        quantidade = 0
        #pega os dados da requisição
        matricula = request.POST.get("matricula")
        lista = request.POST.getlist("cpf")
        #verifica se não tem matricula ou se nao tem lista, senao tiver
        #envia mensagem de error e redireciona para pagina de cadastro equipe
        if not matricula or not lista:
            messages.error(request,  "funcionario cadastrado nao cadastrado",
                           extra_tags="danger")
            return redirect("cadastro_equipe")
        #filtra o estudante por matrícula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #percorre a lista de cpf
        for cpf in lista:
            #filtra funcionario por cpf e pega o primeiro
            funcionario = Funcionario.objects.filter(cpf=cpf).first()
            #verifica se tem funcionario e estudante
            if funcionario and estudante:
                #filtra funcionario estudante pelo estudante
                funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante)
                #filtra funcionario estudante pelo funcionario e pega o primeiro
                funcionario_estudante = funcionario_estudante.filter(funcionario=funcionario).first()
                #verifica se tem funcionario estudante
                if not funcionario_estudante:
                    #cadastra o estudante e o funcionario
                    FuncionarioEstudante.objects.create(estudante=estudante, funcionario=funcionario)
                    quantidade += 1
        #verifica se todos os funcionarios foram cadastrados, envia mensagem de sucesso
        #e redireciona para pagina de cadastro equipe
        if quantidade == len(lista):
            messages.success(request, "funcionario cadastrado")
            return redirect("cadastro_equipe")
        #se todos os funcionários não foram cadastrados envia mensagem de error
        # e redireciona para página de login
        messages.error(request, f'{quantidade} funcionario cadastrado', extra_tags="danger")
        return redirect("cadastro_equipe")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def diagnostico(request):
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'diagnostico.html', dicionario)
    if request.method == "POST":
        # se tiver renderiza a pagina enviando a matrícula 1, para ser usada na página
        # como value da matrícula do estudante, para ficar preenchida
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1":matricula1}
            return render(request, "diagnostico.html", dicionario)
        # pega os dados da requisição
        estudante = request.POST.get("estudante")
        laudo = request.POST.get("laudo")
        texto_diagnostico = request.POST.get("texto_diagnostico")
        ano = request.POST.get("ano")
        ano = int(ano)
        atendimento = request.POST.get("atendimento")
        texto_atendimento = request.POST.get("texto_atendimento", " ")
        #filtra o estudante pela matrícula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=estudante).first()
        #verifica se tem estudante
        if estudante:
            #verifica se o diagnostico esta cadastrado
            if Diagnostico.objects.filter(estudante=estudante).exists():
                #se tiver diagnostico envia mensagem de error de diagnóstico já cadastrado
                #e redireciona para página de diagnóstico
                messages.error(request, "diagnostico ja cadastrado", extra_tags="danger")
                return redirect("diagnostico")
            #cadastra o diagnostico
            Diagnostico.objects.create(estudante=estudante, laudo=laudo,
                                       texto=texto_diagnostico, ano_diagnostico=ano,
                                       atendimento_fora_da_escola = atendimento,
                                       texto_atendimento=texto_atendimento)
            #envia mensagem de sucesso e redireciona para diagnostico
            messages.success(request, "diagnostico cadastrado")
            return redirect("diagnostico")
        #envia mensagem de erro e redireciona para diagnóstico
        messages.error(request, "diagnostico nao cadastrado", extra_tags="danger")
        return redirect("diagnostico")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def historico_escolar(request):
    #verifica se o método da requisição é get
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'historico_escolar.html', dicionario)
    #verifica se o metodo da requisição é post
    if request.method == "POST":
        #pega os dados da requisição da matrícula 1
        matricula1 = request.POST.get("matricula1")
        #verifica se tem matricula 1
        if matricula1:
            #envia a matricula 1 para o template que sera usado como value
            dicionario = {"matricula1":matricula1}
            return render(request, "diagnostico.html", dicionario)
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        texto = request.POST.get("texto")
        texto2 = request.POST.get("texto2")
        #filtra o estudante pela matrícula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #verifica se o perfil estudante esta cadastrado
            if HistoricoEscolar.objects.filter(estudante=estudante).exists():
                #se tiver historico escolar envia mensagem de error historico escolar ja
                #cadastrado e redireciona para pagina de historico escolar
                messages.error(request, "historico escolar ja cadastrado", extra_tags="danger")
                return redirect("historico_escolar")
            #cadastra o historico escolar
            HistoricoEscolar.objects.create(texto=texto, texto2=texto2, estudante=estudante)
            #envia mensagem de sucesso e redireciona para historico escolar
            messages.success(request, "historico escolar cadastrado")
            return redirect("historico_escolar")
        #envia mensagem de error e redireciona para historico escolar
        messages.error(request, "historico escolar não cadastrado", extra_tags="danger")
        return redirect("historico_escolar")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def perfil_estudante(request):
    #verifica se o método da requisição é igual a get
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'perfil_estudante.html', dicionario)
    #verifica se o método da requisição é igual a post
    if request.method == "POST":
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        interesse = request.POST.get("interesse")
        habilidade = request.POST.get("habilidade")
        nao_gosta = request.POST.get("nao_gosta")
        desafio = request.POST.get("desafio")
        informacao = request.POST.get("informacao")
        #filtra os estudantes pela matrícula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #verifica se o perfil do estudante ja esta cadastrado
            if PerfilEstudante.objects.filter(estudante=estudante).exists():
                #se tiver perfil estudante envia mensagem de error de
                # perfil estudante ja cadastrado e redireciona para perfil estudante
                messages.error(request, "perfil estudante ja cadastrado", extra_tags="danger")
                return redirect("perfil_estudante")
            #cadastra o perfil estudante
            PerfilEstudante.objects.create(estudante=estudante,
                                           interesse=interesse, habilidade = habilidade,
                                           nao_gosta=nao_gosta, dificuldade=desafio,
                                           informacao=informacao)
            #envia mensagem de sucesso e redireciona para perfil estudante
            messages.success(request, "perfil estudante cadastrado")
            return redirect("perfil_estudante")
        #envia mensagem de error e redireciona para perfil estudante
        messages.error(request, "perfil estudante não cadastrado", extra_tags="danger")
        return redirect("perfil_estudante")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def atividade(request):
    #verifica se o metodo da requisição e get
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "atividade.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        atividade1 = request.POST.get("atividade")
        descricao = request.POST.get("descricao")
        #filtra os estudantes pela matrícula e pega o primeiro
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #verifica se a atividade ja esta cadastrada
            if Atividade.objects.filter(estudante=estudante).exists():
                # se tiver atividade envia mensagem de error
                # atividade já cadastrado e redireciona para atividade
                messages.error(request, "atividade ja cadastrado", extra_tags="danger")
                return redirect("atividade")
            # cadastra a atividade, envia mensagem de sucesso e redireciona para a
            # página atividade
            Atividade.objects.create(estudante=estudante, atividade=atividade1,
                                     descricao=descricao)
            messages.success(request, "atividade cadastrada")
            return redirect("atividade")
        messages.error(request, "atividade não cadastrada", extra_tags="danger")
        return redirect("atividade")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def planejamento(request):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "planejamento.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        habilidade = request.POST.get("habilidade")
        metas_curto_prazo = request.POST.get("meta_curto_prazo")
        metas_medio_prazo = request.POST.get("meta_medio_prazo")
        metas_longo_prazo = request.POST.get("meta_longo_prazo")
        #filtra os estudantes pela matrícula e pega o primeiro
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #verifica se o planejamento ja esta cadastrado
            if Planejamento.objects.filter(estudante=estudante).first():
                #se tiver planejamento enviar menasagem de error de planejamento
                #ja cadastrado e redireciona para pagina de planjamento
                messages.error(request, "planejamento ja cadastrado", extra_tags="danger")
                return redirect("planejamento")
            #cadastra o planejamento no banco de dados
            Planejamento.objects.create(estudante=estudante, habilidade=habilidade,
                                        metas_curto_prazo=metas_curto_prazo,
                                        metas_medio_prazo = metas_medio_prazo,
                                        metas_longo_prazo = metas_longo_prazo)
            #envia mensagem de sucesso de planejamento encontrado e redireciona para pagina
            #de planejamento
            messages.success(request, "planejamento cadastrado")
            return redirect("planejamento")
        #envia mensagem de error e redireciona para pagina de planejamento
        messages.error(request, "planejamento não cadastrado", extra_tags="danger")
        return redirect("planejamento")
#verifica se o usuario esta logado
@login_required(login_url="login1")
def habilidade_academica(request):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'habilidade_academica.html', dicionario)
    if request.method == "POST":
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        componente = request.POST.get("componente")
        adaptacao = request.POST.getlist("adaptacao")
        #separa as adaptação por vírgula
        adaptacao = ", ".join(adaptacao)
        habilidade = request.POST.get("habilidade")
        facilidade_dificuldade = request.POST.get("facilidade_dificuldade")
        meta_turma = request.POST.get("meta_turma")
        meta_especifica = request.POST.get("meta_especifica")
        procedimento = request.POST.get("procedimento")
        avaliacao = request.POST.get("avaliacao")
        #filtra os estudantes por matrícula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            if HabilidadeAcademica.objects.filter(estudante=estudante).exists():
                #se tiver habilidade academica envia mensagem de error e redireciona para
                #pagina de habilidade academica
                messages.error(request, "habilidade academica ja cadastrado", extra_tags="danger")
                return redirect("habilidade_academica")
            #cadastra habilidade academica no banco de dados
            HabilidadeAcademica.objects.create(estudante=estudante,
                                               componente_curricular=componente,
                                               adaptacao_curricular = adaptacao,
                                               habilidade = habilidade,
                                               facilidade_dificuldade = facilidade_dificuldade,
                                               metas_turma = meta_turma, metas_especifica = meta_especifica,
                                               procedimento_metodologico = procedimento,
                                               avaliacao = avaliacao)
            #envia mensagem de sucesso e redireciona para página de habilidade academica
            messages.success(request, "habilidade academica cadastrado")
            return redirect("habilidade_academica")
        #envia mensagem de error e redireciona para página de habilidade academica
        messages.error(request, "habilidade academica não cadastrado", extra_tags="danger")
        return redirect("habilidade_academica")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def checklist2(request):
    if request.method == "GET":
        #cria lista
        checklist = []
        lista = []
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #adiciona o tipo da checklist e a checklist na lista
        tipo = "adaptacao de acesso ao curriculo"
        checklist = ["Organização dos agrupamentos de estudantes",
                     "Organização do Espaço Físico e Condições Ambientais",
                     "Organização dos Recursos Didáticos",
                     "Organização Didática da Aula"]
        lista.append({"tipo":tipo, "checklist":checklist})
        tipo = "adaptacao de objetivo"
        checklist = ["Priorização de habilidades básicas de atenção, participação e adaptabilidade",
                     "Adequação de objetivos, de acordo com a especificidade do(a) estudante",
                     "Retirada de objetivos propostos no currículo escolar",
                     "Introdução de objetivos específicos, complementares e/ou alternativos"]
        lista.append({"tipo": tipo, "checklist": checklist})
        tipo = "adaptacao de conteudo"

        checklist = ["Priorização de conteúdos",
                     "Reformulação da sequência dos conteúdos",
                     "Retomada de determinados conteúdos, garantindo seu domínio e consolidação",
                     "Eliminação de conteúdos secundários, para dar enfoque mais intensivo e prolongado a conteúdos mais básicos e essenciais no currículo",
                     "Introdução de conteúdos específicos, complementares ou alternativos"]
        lista.append({"tipo": tipo, "checklist": checklist})
        tipo = "adaptacao do metodo de ensino e da organizacao didatica"
        checklist = ["Modificação de procedimentos / estratégias de ensino",
                     "Adoção de métodos, procedimentos e atividades alternativas e/ou complementares às previstas",
                     "Organização diferenciada da sala de aula",
                     "Adaptação de materiais",
                     "Utilização de recursos específicos de acesso ao currículo"]
        lista.append({"tipo": tipo, "checklist": checklist})
        tipo = "adaptacao sistema"
        checklist = ["Adaptação e/ou modificação de técnicas, instrumentos, procedimentos e critérios.",
                         "Introdução de critérios específicos de avaliação.",
                         "Necessidade de Avaliação em espaço diferente dos colegas.",
                         "Eliminação de critérios gerais de avaliação.",
                         "Modificação dos critérios de promoção"]
        lista.append({"tipo": tipo, "checklist": checklist})
        tipo = "adaptacao de temporalidade"
        checklist = ["Aumento do Tempo para atividades e avaliações",
                     "Aumento do tempo para trabalhar determinados objetivos/conteúdos",
                     "Diminuição do tempo para trabalhar determinados objetivos/conteúdos",
                     "Aumento do tempo do estudante em uma série",
                     "Aceleração do estudante para série posterior"]
        lista.append({"tipo": tipo, "checklist": checklist})
        #envia estudante e a lista com tipo e checklist para o template,
        #no template vai percorrer a lista pegando o tipo e percorrer a checklist
        #para criar as opções
        dicionario = {"lista":lista, "estudantes":estudante}
        return render(request, 'checklist.html', dicionario)
    #verifica se o metodo da requisição é POST
    if request.method == "POST":
        #pega os dados da requisição
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = request.POST.get("tipo")
        #transforma lista em string separando os itens por linha
        checklist = "\n".join(checklist)
        #filtra os estudanes por matricula e pega o primeiro
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            checklist3 = Checklist.objects.filter(estudante=estudante)
            checklist3 = checklist3.filter(checklist=tipo).first()
            if checklist3:
                messages.error(request, f"{tipo} ja cadastrado", extra_tags="danger")
                return redirect("checklist2")
            #se tem estudante cadastra a checklist
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            #envia mensagem de sucesso e redireciona para pagina da checklist
            messages.success(request, f"{tipo} cadastrado")
            return redirect("checklist2")
        #envia mensagem de error e redireciona para pagina da checklist
        messages.error(request, f"{tipo} não cadastrado", extra_tags="danger")
        return redirect("checklist2")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerar_pdf(request):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "gerar_pdf_matricula.html", dicionario)
    #verifica se o metodo da requisição é POST
    if request.method == "POST":
        #pega a matrícula da requisição
        matricula = request.POST.get("matricula")
        #filtra o estudante pela matrícula e pega o primeiro
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if not estudante:
            messages.error(request, "estudante não encontrado", extra_tags="danger")
            return redirect("gerar_pdf")
        #filtra o pei pelo estudante e pega o primeiro
        pei1 = PEI.objects.filter(estudante=estudante).first()
        #verifica se tem pei
        if pei1:
            #pega o professor do pei
            professor = pei1.professor
        else:
            professor = None
        #pega os dados do banco de dados
        funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante)
        diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
        historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
        perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
        checklist = Checklist.objects.filter(estudante=estudante)
        atividade1 = Atividade.objects.filter(estudante=estudante).first()
        planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
        habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
        dicionario = {"estudante":estudante, "pei":pei1, "professor":professor,
                      "funcionarioEstudante":funcionario_estudante, "diagnostico":diagnostico1,
                      "historico_escolar":historico_escolar1, "perfil_estudante":perfil_estudante1,
                      "checklist":checklist, "atividade":atividade1, "planejamento":planejamento1,
                      "habilidadeAcademica":habilidade_academica1}
        #redenriza o template com os dados e converte em string
        html = render_to_string("gerar_pdf.html", dicionario)
        #transforma o codigo html em pdf
        pdf = HTML(string=html).write_pdf()
        #carrega o pdf
        return HttpResponse(pdf, content_type="application/pdf")

#verifica se o usuario esta logado senão estiver redireciona para pagina de login
@login_required(login_url="login1")
def estudante_cadastrado(request):
    #pega todos os estudantes do banco de dados e envia para o template
    #no template exibe os dados dos estudantes
    estudantes = Estudante.objects.all().order_by("nome")
    matricula = request.GET.get("estudante")
    paginas = Paginator(estudantes,9)  # isso aqui faz a divisão da quantidade de estudantes em tabelas de 9 em 9, ou menos
    pagina = request.GET.get("page")  # isso aqui é para saber qual paginas entre, as divisões feitas, foi pedida pelo user

    estudantes = paginas.get_page(pagina)  # coloca os estudantes divididos na variavel estudante
    estudante_selecionado = None

    if matricula:
        estudante_selecionado = Estudante.objects.get(matricula=matricula)
    dicionario = {"estudantes": estudantes, 'nome': request.user.first_name,"estudante_selecionado": estudante_selecionado}
    return render(request, "estudantes_cadastrados.html", dicionario)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_estudante(request):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #pega todos os estudantes do banco de dados e envia para o template
        estudantes = Estudante.objects.all()
        dicionario = {"estudantes":estudantes}
        return render(request, "remover_estudante.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        #filtra os estudantes pela matricula
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #exclui o estudante
            estudante.delete()
            #envia mensagem de sucesso e redireciona para página de remover estudante
            messages.success(request, "estudante removido")
            return redirect("remover_estudante")
        #envia mensagem de error e redireciona para pagina de remover estudante
        messages.error(request, "estudante não removido", extra_tags="danger")
        return redirect("remover_estudante")
#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_professor(request):
    if request.method == "GET":
        professor = Professor.objects.all()
        dicionario = {"professores":professor}
        return render(request, "remover_professor.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisição
        matricula = request.POST.get("matricula")
        #filtra os professores por matrícula e pega o primeiro
        professor = Professor.objects.filter(matricula=matricula).first()
        #verifica se tem professor
        if professor:
            #remove o professor
            professor.delete()
            #envia mensagem de sucesso e redireciona para pagina de remover professor
            messages.success(request, "professor removido")
            return redirect("remover_professor")
        #envia mensagem de error e redireciona para pagina de remover professor
        messages.error(request, "professor não removido", extra_tags="danger")
        return redirect("remover_professor")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_funcionario(request):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #pega todos os funcionários do banco de dados e envia para o template
        funcionario = Funcionario.objects.all()
        dicionario = {"funcionarios":funcionario}
        return render(request, "remover_funcionario.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisição
        cpf = request.POST.get("cpf")
        #filtra funcionario pelo cpf e pega o primeiro
        funcionario = Funcionario.objects.filter(cpf=cpf).first()
        #verifica se tem funcionario
        if funcionario:
            #remove o funcionario
            funcionario.delete()
            #envia mensagem de sucesso e redireciona para página de remover funcionario
            messages.success(request, "funcionario removido")
            return redirect("remover_funcionario")
        #envia mensagem de error e redireciona para pagina de remover funcionario
        messages.error(request, "efuncionario não removido", extra_tags="danger")
        return redirect("remover_funcionario")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def professor_cadastrado(request):
    # pega todos os professores do banco de dados e envia para o template
    # no template exibe os dados dos professores
    professor = Professor.objects.all()
    dicionario = {"professores":professor}
    return render(request, "professores_cadastrados.html", dicionario)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def funcionario_cadastrado(request):
    # pega todos os funcionarios do banco de dados e envia para o template
    # no template exibe os dados dos funcionarios
    funcionario = Funcionario.objects.all()
    dicionario = {"funcionarios":funcionario}
    return render(request, "funcionarios_cadastrados.html", dicionario)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_professor(request, matricula):
    #verifica se o metodo da requisição é GET
    if request.method  == "GET":
        #filtra o professor pela matricula senão tiver professor retornar error 404
        professor = get_object_or_404(Professor, matricula=matricula)
        #cria um formulario com os dados do professor
        formulario = FormularioProfessor(instance=professor)
        #percorre as chaves do dicionario de fields do formulario e adiciona
        # a class form-control aos itens do formulario
        for formulario1 in formulario.fields.keys():
            formulario.fields[formulario1].widget.attrs["class"] = "form-control"
        #envia o formulario para o template
        dicionario = {"formulario":formulario, "matricula":matricula}
        return render(request, "editar_professor.html", dicionario)
    #verifica se o metodo da requisição é POST
    if request.method == "POST":
        #filtra o professor pela matricula, senão tiver professor retorna error 404
        professor = get_object_or_404(Professor, matricula=matricula)
        #cria um formulario com os dados do professor e envia os dados da requisição
        #para o formulario
        formulario = FormularioProfessor(request.POST, instance=professor)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #envia os dados do formulario para o banco de dados
            formulario.save()
            #envia mensagem de sucesso e redireciona para página de editar professor
            messages.success(request, "professor editado com sucesso")
            return redirect("editar_professor", matricula=matricula)
        messages.error(request, "professor não editado", extra_tags="danger")
        return redirect("editar_professor", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_funcionario(request, cpf):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #filtra o funcionario pelo cpf, senão encontrar retorna error 404
        funcionario = get_object_or_404(Funcionario, cpf=cpf)
        #cria um formulario com as informações do funcionario
        formulario = FormularioFuncionario(instance=funcionario)
        # percorre as chaves do dicionario de fields do formulario e adiciona
        # a class form-control aos itens do formulario
        for formulario1 in formulario.fields.keys():
            formulario.fields[formulario1].widget.attrs["class"] = "form-control"
        # envia o formulario para o template
        #envia o formulario para o template
        dicionario = {"formulario":formulario, "cpf":cpf}
        return render(request, "editar_funcionario.html", dicionario)
    #verifica se o metodo da requisição é POST
    if request.method == "POST":
        #filtra o funcionario pelo cpf, senao tiver retorna error 404
        funcionario = get_object_or_404(Funcionario, cpf=cpf)
        #cria um formulario com os dados de funcionários e envia os dados da requisição
        formulario = FormularioFuncionario(request.POST, instance=funcionario)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso
            messages.success(request, "funcionario editado com sucesso")
            return redirect("editar_funcionario", cpf=cpf)
        messages.error(request, "funcioanrio não editado", extra_tags="danger")
        return redirect("editar_funcionario", cpf=cpf)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_estudante(request, matricula):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        #filtra estudante pela matricula senao tiver estudante, retornar error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #cria um formulario com os dados do estudante e envia para o template
        formulario = FormularioEstudante(instance=estudante)
        # percorre as chaves do dicionario de fields do formulario e adiciona
        # a class form-control aos itens do formulario
        for formulario1 in formulario.fields.keys():
            formulario.fields[formulario1].widget.attrs["class"] = "form-control"
        # envia o formulario para o template
        dicionario = {"formulario":formulario, "matricula":matricula}
        return render(request, "editar_estudante.html", dicionario)
    #verifica se o metodo é POST
    if request.method == "POST":
        # filtra estudante pela matricula senao tiver estudante, retornar error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #cria um formulario com os dados do estudante e envia os dados da requisição
        #para o formulario
        formulario = FormularioEstudante(request.POST, instance=estudante)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para página de editar estudante
            messages.success(request, "estudante editado com sucesso")
            return redirect(editar_estudante, matricula=matricula)
        #envia mensagem de error e redireciona para pagina de editar estudante
        messages.error(request, "estudante não editado", extra_tags="danger")
        return redirect(editar_estudante, matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_professor_matricula(request):
    #verifica se o metodo da requisição é get
    if request.method == "GET":
        professor = Professor.objects.all()
        dicionario = {"professores":professor}
        return render(request, "editar_professor_matricula.html", dicionario)
    #verifica se o metodo da requisição é post
    if request.method == "POST":
        #pega a matricula da requisição
        matricula = request.POST.get("matricula")
        #redireciona para pagina de editar professor
        return redirect("editar_professor", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_funcionario_cpf(request):
    #verifica se o metodo da requisição é get
    if request.method == "GET":
        funcionario = Funcionario.objects.all()
        dicionario = {"funcionarios":funcionario}
        return render(request, "editar_funcionario_cpf.html", dicionario)
    #verifica se o metodo da requisição é post
    if request.method == "POST":
        #pega a matricula da requisição
        cpf = request.POST.get("cpf")
        #redireciona para pagina de editar professor
        return redirect("editar_funcionario", cpf=cpf)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_estudante_matricula(request):
    #verifica se o metodo da requisição é get
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "editar_estudante_matricula.html", dicionario)
    #verifica se o metodo da requisição é post
    if request.method == "POST":
        #pega a matricula da requisição
        matricula = request.POST.get("matricula")
        #redireciona para pagina de editar professor
        return redirect("editar_estudante", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerenciar_professor(request):
    return render(request, "gerenciar_professor.html")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerenciar_estudante(request):
    return render(request, "gerenciar_estudante.html")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerenciar_funcionario(request):
    return render(request, "gerenciar_funcionario.html")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def cadastrar_pei(request):
    return render(request, "cadastrar_pei.html")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_pei(request, matricula):
    #filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra o pei pelo estudante e pega o primeiro
    pei1 = PEI.objects.filter(estudante=estudante).first()
    #verifica se tem pei
    if pei1:
        #remove o pei
        pei1.delete()
        #envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "pei removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "pei não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_diagnostico(request, matricula):
    #filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra diagnostico pelo estudante e pega o primeiro
    diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
    #verifica se tem diagnostico
    if diagnostico1:
        #remove o diagnostico
        diagnostico1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "diagnostico removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "diagnostico não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_historico_escolar(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra o historico escolar pelo estudante e pega o primeiro
    historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
    #verifica se tem historico escolar
    if historico_escolar1:
        #remove o historico escolar
        historico_escolar1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "historico escolar removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "historico escolar não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_perfil_estudante(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra o perfil estudante pelo estudante e pega o primeiro
    perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
    #verifica se tem perfil estudante
    if perfil_estudante1:
        #remove o perfil do estudante
        perfil_estudante1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "perfil estudante removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "perfil estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_checklist(request, matricula, id1):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra a checklist pelo id e pega a primeira
    checklist1 = Checklist.objects.filter(id=id1).first()
    #verifica se tem a checklist
    if checklist1:
        #remove a checklist
        checklist1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "checklist removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "checklist não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_atividade(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra a atividade pelo estudante e pega a primeira
    atividade1 = Atividade.objects.filter(estudante=estudante).first()
    #verifica se tem a atividade
    if atividade1:
        #remove a atividade
        atividade1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "atividade removida")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para página de dados pei
        messages.error(request, "atividade não encontrada", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_planejamento(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra o planejamento pelo estudante e pega o primeiro
    planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
    #verifica se tem planejamento
    if planejamento1:
        #remove o planejamento
        planejamento1.delete()
        # envia mensagem de sucesso e redireciona para página de dados pei
        messages.success(request, "planejamento removido")
        return redirect("dados_pei", matricula=matricula)
    # envia mensagem de error e redireciona para página de dados pei
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "planejamento não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_equipe_pei(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra funcionario estudante pelos estudantes
    funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante)
    #verifica se tem funcionario estudante
    if funcionario_estudante:
        #remove funcionario estudante
        funcionario_estudante.delete()
        # envia mensagem de sucesso e redireciona para página de dados pei
        messages.success(request, "equipe pei removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para página de dados pei
        messages.error(request, "equipe pei não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def remover_habilidade_academica(request, matricula):
    # filtra estudante pela matricula, se não tiver estudante retorna error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    # filtra estudante pela habilidade academica
    habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
    # verifica se tem habilidade academica
    if habilidade_academica1:
        # remove habilidade academica
        habilidade_academica1.delete()
        # envia mensagem de sucesso e redireciona para pagina de dados pei
        messages.success(request, "habilidade academica removido")
        return redirect("dados_pei", matricula=matricula)
    else:
        # envia mensagem de error e redireciona para pagina de dados pei
        messages.error(request, "habilidade academica não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

#verifica se tem dados no banco de dados, se tiver retorna
#um formulario com os dados preenchidos senão tiver retorna None
def verificar_formulario(formulario, modelo):
    if modelo:
        formulario1 = formulario(instance=modelo)
    else:
        formulario1 = None
    return formulario1

#verifica se o usuario esta logado
@login_required(login_url="login1")
def dados_pei(request, matricula):
    #cria uma lista
    lista = []
    numero = 0
    #verifica se tem estudante se não tiver retornar error 404
    estudante = get_object_or_404(Estudante, matricula=matricula)
    #filtra o pei pelo estudante e pega o primeiro
    pei1 = PEI.objects.filter(estudante=estudante).first()
    #verifica se tem pei, se tiver retorna um formulario com os dados do pei preenchido,
    #senão tiver retorna None
    formulario_pei = verificar_formulario(Pei, pei1)
    #verifica se tem formulario
    if formulario_pei:
        #percorre os dados do formulario
        for formulario in formulario_pei.fields.keys():
            #se formulario for professor, cria classe com form-select do bootstrap
            if formulario == "professor":
                formulario_pei.fields[formulario].widget.attrs["class"] = "form-select"
            #se o formulario for tempo, cria classe com form-control do bootstrap
            if formulario == "tempo":
                formulario_pei.fields[formulario].widget.attrs["class"] = "form-control"
    #filtra os dados do funcionario estudante pelo estudante, retorna uma lista com os ids
    #dos funcionarios
    funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante).values_list("funcionario_id", flat=True)
    #verifica se tem funcionario estudante
    if funcionario_estudante:
        #cria um formulario com os dados dos funcionarios
        equipe_pei = EquipePei1(initial={"funcionarios": funcionario_estudante})
    else:
        equipe_pei = None
    # filtra o diagnostico pelo estudante e pega o primeiro
    diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
    #verifica se tem diagnostico1, se tiver preenche com os dados do banco de dados,
    #senão tiver retorna None
    formulario_diagnostico1 = verificar_formulario(FormularioDiagnostico, diagnostico1)
    # verifica se tem formulario, percorre o formulario,
    # adiciona a classe do bootstrap no formulario
    if formulario_diagnostico1:
        for formulario in formulario_diagnostico1.fields.keys():
            formulario_diagnostico1.fields[formulario].widget.attrs["class"] = "form-control"
    # filtra o historico escolar pelo estudante e pega o primeiro
    historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
    # verifica se tem historico_escolar1, se tiver preenche com os dados do banco de dados,
    # senão tiver retorna None
    formulario_historico_escolar = verificar_formulario(FormularioHistoricoEscolar,
                                                       historico_escolar1)
    # verifica se tem formulario, percorre o formulario,
    # adiciona a classe do bootstrap no formulario
    if formulario_historico_escolar:
        for formulario in formulario_historico_escolar.fields.keys():
            formulario_historico_escolar.fields[formulario].widget.attrs["class"] = "form-control"
            formulario_historico_escolar.fields["texto"].widget.attrs["id"] = "id_texto1"
    # filtra o perfil estudante pelo estudante e pega o primeiro
    perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
    # verifica se tem perfil estudante 1, se tiver preenche com os dados do banco de dados,
    # senão tiver retorna None
    formulario_perfil_estudante = verificar_formulario(FormularioPerfilEstudante,
                                                       perfil_estudante1)
    # verifica se tem formulario, percorre o formulario,
    # adiciona a classe do bootstrap no formulario
    if formulario_perfil_estudante:
        for formulario in formulario_perfil_estudante.fields.keys():
            formulario_perfil_estudante.fields[formulario].widget.attrs["class"] = "form-control"
    # filtra a checklist pelo estudante
    checklist1 = Checklist.objects.filter(estudante=estudante)
    for checklist in checklist1:
        # verifica se tem checklist, se tiver preenche com os dados do banco de dados,
        # senão tiver retorna None
        formulario_checklist = verificar_formulario(FormularioChecklist, checklist)
        # verifica se tem formulario, percorre o formulario,
        # adiciona a classe do bootstrap no formulario
        if formulario_checklist:
            for formulario in formulario_checklist.fields.keys():
                formulario_checklist.fields[formulario].widget.attrs["class"] = "form-control"
            #adiciona o formulario na lista
            lista.append(formulario_checklist)
    #percorre a lista de formularios
    for checklist3 in lista:
        #soma mais 1 ao numero
        numero += 1
        #altera o id do formulario para o nome do formulario mais o numero
        for formulario in checklist3.fields.keys():
            checklist3.fields[formulario].widget.attrs["id"] = f"{formulario}{numero}"
    # filtra o atividade pelo estudante e pega o primeiro
    atividade1 = Atividade.objects.filter(estudante=estudante).first()
    # verifica se tem atividade, se tiver preenche com os dados do banco de dados,
    # senão tiver retorna None
    formulario_atividade = verificar_formulario(FormularioAtividade, atividade1)
    if formulario_atividade:
        for formulario in formulario_atividade.fields.keys():
            formulario_atividade.fields[formulario].widget.attrs["class"] = "form-control"
    # filtra o planejamento pelo estudante e pega o primeiro
    planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
    # verifica se tem planejamento, se tiver preenche com os dados do banco de dados,
    # senão tiver retorna None
    formulario_planejamento = verificar_formulario(FormularioPlanejamento, planejamento1)
    if formulario_planejamento:
        formulario_planejamento.fields["habilidade"].widget.attrs["id"] = "habilidade1"
        for formulario in formulario_planejamento.fields.keys():
            formulario_planejamento.fields[formulario].widget.attrs["class"] = "form-control"
    # filtra o habilidade academica pelo estudante e pega o primeiro
    habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
    # verifica se tem habilidade academica 1, se tiver preenche com os dados do banco de dados,
    # senão tiver retorna None
    formulario_habilidade_academica = verificar_formulario(FormularioHabilidadeAcademica, habilidade_academica1)
    # verifica se tem formulario
    if formulario_habilidade_academica:
        #altera o id do formulario para habilidade academica2
        formulario_habilidade_academica.fields["habilidade"].widget.attrs["id"] = "habilidade2"
        #percorre o formulario e adiciona a classe do bootstrap
        for formulario in formulario_habilidade_academica.fields.keys():
            formulario_habilidade_academica.fields[formulario].widget.attrs["class"] = "form-control"
    dicionario = {"pei":formulario_pei, "equipe_pei":equipe_pei,
                  "diagnostico":formulario_diagnostico1,
                  "historico_escolar":formulario_historico_escolar,
                  "perfil_estudante":formulario_perfil_estudante,
                  "checklist":lista, "atividade":formulario_atividade,
                  "planejamento":formulario_planejamento,
                  "habilidade_academica":formulario_habilidade_academica,
                  "matricula":matricula, "estudante":estudante}
    return render(request, "dados_pei.html", dicionario)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_pei(request, matricula):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    #verifica se o metodo da requisição é POST
    if request.method == "POST":
        #filtra o estudante pela matricula,
        #se nao tiver estudante cadastrado retornar error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra o pei pelo estudante e pega o primeiro
        pei1 = PEI.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados do pei e com os dados da requisição
        formulario = Pei(request.POST, instance=pei1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para dados pei
            messages.success(request, "pei editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            # envia mensagem de error e redireciona para dados pei
            messages.error(request, "pei não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_equipe_pei(request, matricula):
    #verifica se o metodo da requisição é GET
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    # verifica se o metodo da requisição é POST
    if request.method == "POST":
        # filtra o estudante pela matricula
        # se o estudante não estiver cadastrado retorna error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #cria um formulario com os dados da requisição
        formulario = EquipePei1(request.POST)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #filtra os funcionarios estudantes pelo estudante e remove
            FuncionarioEstudante.objects.filter(estudante=estudante).delete()
            #pega os funcionarios do formulario
            funcionarios = formulario.cleaned_data["funcionarios"]
            #percorre a lista de funcionarios
            for funcionario in funcionarios:
                #adiciona o estudante e o funcionario ao funcionario estudante
                FuncionarioEstudante.objects.create(estudante=estudante, funcionario=funcionario)
        #envia mensagem de sucesso e redireciona para pagina dados pei
        messages.success(request, "a equipe pei foi editada com sucesso")
        return redirect("dados_pei", matricula=matricula)
    #envia mensagem de error e redireciona para pagina de dados pei
    messages.error(request, "a equipe pei não foi editada")
    return redirect("dados_pei", matricula=matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_diagnostico(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    # verifica se o metodo da requisição é POST
    if request.method == "POST":
        # filtra o estudante pela matricula
        # se o estudante não estiver cadastrado retorna error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra os dados do formulario pelo estudante e pega o primeiro
        diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados do banco de dados e da requisição
        formulario = FormularioDiagnostico(request.POST, instance=diagnostico1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina dados pei
            messages.success(request, "diagnostico editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "diagnostico não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_historico_escolar(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    # verifica se o metodo da requisição é POST
    if request.method == "POST":
        # filtra o estudante pela matricula
        # se o estudante não estiver cadastrado retorna error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra o historico escolar pelo estudante e pega o primeiro
        historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados do banco de dados e os dados da requisição
        formulario = FormularioHistoricoEscolar(request.POST, instance=historico_escolar1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de sucesso
            messages.success(request, "historico escolar editado com sucesso")
            return redirect("dados_pei", matricula)
        #envia mensagem de error e redireciona para pagina de error
        else:
            messages.error(request, "historico escolar não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_perfil_estudante(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    # verifica se o metodo da requisição é POST
    if request.method == "POST":
        # filtra o estudante pela matricula
        # se o estudante não estiver cadastrado retorna error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra pelo estudante e pega o primeiro
        perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados da requisição e os dados do banco de dados
        formulario = FormularioPerfilEstudante(request.POST, instance=perfil_estudante1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de dados pei
            messages.success(request, "perfil estudante editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "perfil estudante não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_checklist(request, matricula, id1):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    # verifica se o metodo da requisição é POST
    if request.method == "POST":
        # filtra o estudante pela matricula
        # se o estudante não estiver cadastrado retorna error 404
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra pelo estudante e pega o primeiro
        checklist1 = Checklist.objects.filter(id=id1).first()
        #cria um formulario com os dados da requisição e os dados do banco de dados
        formulario = FormularioChecklist(request.POST, instance=checklist1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de dados pei
            messages.success(request, "checklist editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "checklist não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_atividade(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra pelo estudante e pega o primeiro
        atividade1 = Atividade.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados da requisição e os dados do banco de dados
        formulario = FormularioAtividade(request.POST, instance=atividade1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de dados pei
            messages.success(request, "atividade editada com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "atividade não editada", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_planejamento(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra pelo estudante e pega o primeiro
        planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados da requisição e os dados do banco de dados
        formulario = FormularioPlanejamento(request.POST, instance=planejamento1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de dados pei
            messages.success(request, "planejamento editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "planejamento não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def editar_habilidade_academica(request, matricula):
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = get_object_or_404(Estudante, matricula=matricula)
        #filtra pelo estudante e pega o primeiro
        habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
        #cria um formulario com os dados da requisição e os dados do banco de dados
        formulario = FormularioHabilidadeAcademica(request.POST, instance=habilidade_academica1)
        #verifica se o formulario é valido
        if formulario.is_valid():
            #salva o formulario
            formulario.save()
            #envia mensagem de sucesso e redireciona para pagina de dados pei
            messages.success(request, "habilidade academica editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            #envia mensagem de error e redireciona para pagina de dados pei
            messages.error(request, "habilidade academica não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerenciar_pei(request):
    if request.method == "GET":
        return render(request, "gerenciar_pei.html")

#verifica se o usuario esta logado
@login_required(login_url="login1")
def gerenciar_pei_matricula(request):
    if request.method == "GET":
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #envia os estudantes para o template
        dicionario = {"estudantes":estudante}
        return render(request, "gerenciar_pei_matricula.html", dicionario)
    if request.method == "POST":
        #pega a matricula da requisição e redireciona para dados pei
        matricula = request.POST.get("matricula")
        return redirect("dados_pei", matricula=matricula)