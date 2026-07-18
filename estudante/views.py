import json

from django.core.handlers.base import reset_urlconf
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from fontTools.misc.cython import returns
from weasyprint import HTML
from .models import (SistemaProfessor, Estudante, Professor, Funcionario, PEI,
                     FuncionarioEstudante, Diagnostico, HistoricoEscolar,
                     PerfilEstudante, Atividade, Planejamento, HabilidadeAcademica,
                     Checklist)
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .forms import (Pei, EquipePei, FormularioDiagnostico, FormularioHistoricoEscolar,
                    FormularioPerfilEstudante, FormularioChecklist, FormularioAtividade,
                    FormularioPlanejamento, FormularioHabilidadeAcademica)

# Create your views here.

def cadastro(request):
    return render(request, 'index.html')

def cadastro_sistema(request):
    # verifica se o metodo da requisicao e GET, se for GET renderiza a pagina sistema cadastro
    if request.method == "GET":
        return render(request, 'sistema_cadastro.html')
    #verifica se o metodo da requisicao e POST
    if request.method == "POST":
        #pega os dados da requisicao
        cpf  = request.POST.get("cpf")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        #gera o hash da senha
        senha = make_password(senha)
        #cria um objeto sistema professor passando os dados e cria a tabela no banco de dados
        SistemaProfessor.objects.create(cpf=cpf, nome=nome, email=email, senha=senha)
        #filtra sistema professor pelo cpf e pega o primeiro objeto
        professor = SistemaProfessor.objects.filter(cpf=cpf).first()
        #verifica se o sistema professor foi cadastrado
        if professor:
            #envia mensagem de usuario cadastrado e redireciona para pagina de login
            messages.success(request, "O usuario foi cadastrado")
            redirect("login")
        #se o sistema professor nao foi cadastrado, envia mensagem de usuario nao cadastro,
        #com a tag danger para ser usada pelo bootstrap e redireciona para pagina de cadastro
        messages.error(request, "O usuario não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_sistema")

def login(request):
    # verifica se o metodo da requisicao e GET, se for GET renderiza a pagina sistema cadastro
    if request.method == "GET":
        return render(request, 'login.html')
     # verifica se o metodo da requisicao e POST
    if request.method == "POST":
        #pega os dados da requisicao
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        #pega o primeiro sistema professor no banco de dados filtrando pelo email
        sistema_professor = SistemaProfessor.objects.filter(email=email).first()
        #verifica se tem sistema professor
        if sistema_professor:
            #verifica se o hash da senha é igual ao hash da senha do sistema professor
            #as senhas no banco de dados estam armazenadas em hash
            #essa funcao pega senha, transforma em hash e verifica se o hash da senha
            #e o mesmo do banco de dados
            if check_password(senha, sistema_professor.senha):
                #cria uma sessao com nome sistema_professor_cpf e armazena o cpf do professor
                #a sessao ela armazena dados em dicionario, esta criando a chave do dicionario
                #e armazenando valor, os dados da sessao sao armazenados do lado do servidor
                #o cliente recebe os coockies que representam os dados da sessao
                request.session["sistema_professor_cpf"] = sistema_professor.cpf
                request.session["sistema_professor_nome"] = sistema_professor.nome
                #redireciona para a pagina do painel do administrador
                return redirect("painel_administrador")
        #se o email nao for encontrado ou a senha for invalida, envia mensagem de error
        #login nao realizado com a tag danger para o bootstrap
        messages.error(request, "login não realizado", extra_tags="danger")
        #redireciona para pagina de login
        return redirect("login")

#apaga os dados armazenados na sessao e redireciona para a pagina de login
def sair(request):
    request.session.flush()
    return redirect("login")

def painel_administrador(request):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "painel_administrador.html")

def cadastro_estudante(request):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_estudante.html')
    if request.method == "POST":
        # pega os dados da requisicao
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
        #filtra o estudante pela matricula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se tem estudante
        if estudante:
            #se o estudante estiver cadastrado
            #envia uma mensagem de error e redireciona para pagina de cadastro
            messages.error(request, "estudante ja cadastrado", extra_tags="danger")
            return redirect("cadastro_estudante")
        #se o estudante não estiver cadastrado, cadastra o estudante
        Estudante.objects.create(cpf=cpf, matricula=matricula, nome=nome,
                                 data_de_nascimento=data_de_nascimento, curso=curso,
                                 periodo=periodo, turma=turma, ingresso=ingresso,
                                 nota=nota, telefone=telefone, email=email, pai=pai, mae=mae,
                                 telefone_responsavel=telefone_responsavel,
                                 email_responsavel=email_responsavel)
        #filtra o estudante pela matricula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #verifica se o estudante foi cadastrado
        if estudante:
            #envia mensagem de sucesso e redireciona para pagina de cadastro
            messages.success(request, "estudante cadastrado")
            return redirect("cadastro_estudante")
        #envia uma mensagem de error e redireciona para pagina de cadastro
        messages.error(request, "estudante não cadastrado", extra_tags="danger")
        return redirect("cadastro_estudante")


def cadastro_professor(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_professor.html')
    if request.method == "POST":
        # pega os dados da requisicao
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        data_de_nascimento = request.POST.get("data_de_nascimento")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        #filtra o professor pela matricula
        professor = Professor.objects.filter(matricula=matricula)
        #filtra os professores retornados pelo cpf e pega o primeiro
        professor = professor.filter(cpf=cpf).first()
        #verifica se tem professor
        if professor:
            #se ja tem professor cadastrado envia mensagem de error e redireciona para
            #pagina de cadastro
            messages.error(request, "professor ja cadastrado", extra_tags="danger")
            return redirect("cadastro_professor")
        #senao tem professor cadastrador, cadastra o professor
        Professor.objects.create(cpf=cpf, nome=nome, matricula=matricula,
                                 data_de_nascimento=data_de_nascimento, email=email,
                                 telefone=telefone)
        #filtra o professor pela matricula e pega o primeiro
        professor = Professor.objects.filter(matricula=matricula).first()
        #verifica se tem um professor
        if professor:
            #se o professor foi cadastrrado, envia mensagem de sucesso e redireciona para
            #pagina de cadastro
            messages.success(request, "professor cadastrado")
            return redirect("cadastro_professor")
        #senao tem professor cadastrado envia mensagem de error e redireciona para
        #pagina de cadastro
        messages.error(request, "professor não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_professor")

def cadastro_funcionario(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_funcionario.html')
    if request.method == "POST":
        # pega os dados da requisicao
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        funcao = request.POST.get("funcao")
        #filtra o funcionario pelo cpf e pega o primeiro
        funcionario = Funcionario.objects.filter(cpf=cpf).first()
        #verifica se tem o funcionario
        if funcionario:
            #se tem um funcionario, envia mensagem de error de funcionario ja cadastrado
            messages.error(request, "o funcionario ja cadastrado", extra_tags="danger")
            return redirect("cadastro_funcionario")
        #cria um funcionario
        Funcionario.objects.create(cpf=cpf, nome=nome, funcao=funcao)
        #filtra o funcionario pelo cpf e pega o primeiro
        funcionario = Funcionario.objects.filter(cpf=cpf).first()
        #verifica se tem funcionario
        if funcionario:
            #se o funcionario foi cadastrado envia mensagem de funcionario cadastrado
            #e redireciona para pagina de cadastro
            messages.success(request, "o funcionario foi cadastrado")
            return redirect("cadastro_funcionario")
        #se o funcionario nao foi cadastrado envia mensagem de funcionario nao cadastrado
        #e redireciona para pagina de cadastro
        messages.error(request, "o funcionario não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_funcionario")

def pei(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    #verifica se o metodo da requisicao e GET
    if request.method == "GET":
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #pega todos os professores do banco de dados
        professor = Professor.objects.all()
        #cria um dicionario com os estudantes e professores
        dicionario = {"estudantes":estudante, "professores":professor}
        #renderiza a pagina e envia o dicionario para a pagina
        return render(request, 'PEI.html', dicionario)
    if request.method == "POST":
        #pega a matricula 1 da requisicao
        matricula1 = request.POST.get("matricula1")
        #verifica se tem dado na matricula 1
        if matricula1:
            #se tiver renderiza a pagina enviando a matricula 1, para ser usada na pagina
            #como value da matricula do estudante, para ficar preenchida
            dicionario = {"matricula1":matricula1}
            return render(request, "PEI.html", dicionario)
        # pega os dados da requisicao
        matricula_estudante = request.POST.get("matricula_estudante")
        matricula_professor = request.POST.get("matricula_professor")
        validade = request.POST.get("validade")
        #filtra professor e estudante pela matricula e pega o primeiro
        estudante = Estudante.objects.filter(matricula = matricula_estudante).first()
        professor = Professor.objects.filter(matricula = matricula_professor).first()
        #verifica se tem professor e estudante
        if estudante and professor:
            #filtra o pei pelo estudante e pega o primeiro
            pei1 = PEI.objects.filter(estudante=estudante).first()
            #verifica se tem pei
            if pei1:
                #se o pei estiver cadastrado envia mensagem de error e
                #redireciona para pagina do pei
                messages.error(request, "o pei ja cadastrado", extra_tags="danger")
                return redirect("pei")
            #cria o pei com o dados da requisicao, envia mensagem de pei cadastrado e
            # redireciona para pagina do pei
            PEI.objects.create(estudante=estudante, professor=professor, tempo=validade)
            messages.success(request, "o pei foi cadastrado")
            return redirect("pei")
        #envia mensagem de error e redireciona para pagina do pei
        messages.error(request, "o pei não foi cadastrado", extra_tags="danger")
        return redirect("pei")

def cadastro_equipe(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        #pega todos os estudantes do banco de dados
        estudante = Estudante.objects.all()
        #pega quantidade da requisicao, se nao tiver dados na requisicao, retorna 0
        quantidade = request.GET.get("quantidade", 0)
        #transforma quantidade em int
        quantidade = int(quantidade)
        #cria uma lista com a quantidade
        #a lista com a quantidade e usada para redenrizar a pagina com a quantidade
        #de funcionarios informados pelo usuario, e usado o for para percorrer a lista
        #e criar os inputs
        lista = range(quantidade)
        #renderiza a pagina enviando a quantidade, a lista e os estudantes
        dicionario = {"quantidade":quantidade, "lista":lista, "estudantes":estudante}
        return render(request, 'cadastro_equipe.html', dicionario)
    if request.method == "POST":
        #pega a quantidade da requisicao, senao tiver quantidade retorna 0
        quantidade = request.POST.get("quantidade", 0)
        #trabsforma quantidade em inteiro
        quantidade = int(quantidade)
        quantidade1 = 0
        #pega matricula da requisicao
        matricula = request.POST.get("matricula")
        #filtra o estudante por matricula e pega o primeiro estudante
        estudante = Estudante.objects.filter(matricula=matricula).first()
        #cadastra os funcionarios e estudante em funcionario estudante
        for i in range(quantidade):
            # pega os cpf da requisicao de cada funcionario
            cpf = request.POST.get(f"cpf_{i}")
            #filtra o funcionario pelo cpf e pega o primeiro funcionario
            funcionario = Funcionario.objects.filter(cpf=cpf).first()
            #filtra funcionario estudante por estudante
            funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante)
            #filtra funcionario estudante retornado pelo funcionario e pega o primeiro
            funcionario_estudante = funcionario_estudante.filter(funcionario=funcionario).first()
            #verifica se tem funcionario estudante
            if funcionario_estudante:
                #se o estudante e o funcionario estiver cadastrado
                # envia mensagem de error e redireciona para pagina de cadastro
                messages.error(request, "equipe pei ja cadastrado", extra_tags="danger")
                return redirect("cadastro_equipe")
            #verifica se tem funcionario e estudante
            if estudante and funcionario:
                #cadastra o funcionario e o estudante
                FuncionarioEstudante.objects.create(estudante=estudante, funcionario=funcionario)
                #soma mais um a quantidade de funcionario estudante cadastrado
                quantidade1 += 1
        #verifica se a quantidade de funcionarios e
        #a mesma de funcionarios estudantes cadastrado
        if quantidade == quantidade1:
            #se todos os funcionarios foram cadastrados envia mensagem de sucesso
            # e redireciona para pagina de cadastro
            messages.success(request, "funcionario cadastrado")
            return redirect("cadastro_equipe")
        #se todos os funcionarios nao foram cadastrados envia mensagem de error e redireciona para pagina de login
        messages.error(request, f'{quantidade1} funcionario cadastrado', extra_tags="danger")
        return redirect("cadastro_equipe")

def diagnostico(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'diagnostico.html', dicionario)
    if request.method == "POST":
        # se tiver renderiza a pagina enviando a matricula 1, para ser usada na pagina
        # como value da matricula do estudante, para ficar preenchida
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1":matricula1}
            return render(request, "diagnostico.html", dicionario)
        # pega os dados da requisicao
        estudante = request.POST.get("estudante")
        laudo = request.POST.get("laudo")
        texto_diagnostico = request.POST.get("texto_diagnostico")
        ano = request.POST.get("ano")
        ano = int(ano)
        atendimento = request.POST.get("atendimento")
        texto_atendimento = request.POST.get("texto_atendimento", " ")
        estudante = Estudante.objects.filter(matricula=estudante).first()
        if estudante:
            diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
            if diagnostico1:
                messages.error(request, "diagnostico ja cadastrado", extra_tags="danger")
                return redirect("diagnostico")
            Diagnostico.objects.create(estudante=estudante, laudo=laudo,
                                       texto=texto_diagnostico, ano_diagnostico=ano,
                                       atendimento_fora_da_escola = atendimento,
                                       texto_atendimento=texto_atendimento)
            messages.success(request, "diagnostico cadastrado")
            return redirect("diagnostico")
        messages.error(request, "diagnostico nao cadastrado", extra_tags="danger")
        return redirect("diagnostico")

def historico_escolar(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'historico_escolar.html', dicionario)
    if request.method == "POST":
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1":matricula1}
            return render(request, "diagnostico.html", dicionario)
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        texto = request.POST.get("texto")
        texto2 = request.POST.get("texto2")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
            if historico_escolar1:
                messages.error(request, "historico escolar ja cadastrado", extra_tags="danger")
                return redirect("historico_escolar")
            HistoricoEscolar.objects.create(texto=texto, texto2=texto2, estudante=estudante)
            messages.success(request, "historico escolar cadastrado")
            return redirect("historico_escolar")
        messages.error(request, "historico escolar não cadastrado", extra_tags="danger")
        return redirect("historico_escolar")

def perfil_estudante(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'perfil_estudante.html', dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        interesse = request.POST.get("interesse")
        habilidade = request.POST.get("habilidade")
        nao_gosta = request.POST.get("nao_gosta")
        desafio = request.POST.get("desafio")
        informacao = request.POST.get("informacao")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
            if perfil_estudante1:
                messages.error(request, "perfil estudnate ja cadastrado", extra_tags="danger")
                return redirect("perfil_estudante")
            PerfilEstudante.objects.create(estudante=estudante,
                                           interesse=interesse, habilidade = habilidade,
                                           nao_gosta=nao_gosta, dificuldade=desafio,
                                           informacao=informacao)
            messages.success(request, "perfil estudante cadastrado")
            return redirect("perfil_estudante")
        messages.error(request, "perfil estudante não cadastrado", extra_tags="danger")
        return redirect("perfil_estudante")

def atividade(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "atividade.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        atividade1 = request.POST.get("atividade")
        descricao = request.POST.get("descricao")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            atividade2 = Atividade.objects.filter(estudante=estudante).first()
            if atividade2:
                messages.error(request, "atividade ja cadastrado", extra_tags="danger")
                return redirect("atividade")
            Atividade.objects.create(estudante=estudante, atividade=atividade1,
                                     descricao=descricao)
            messages.success(request, "atividade cadastrada")
            return redirect("atividade")
        messages.error(request, "atividade não cadastrada", extra_tags="danger")
        return redirect("atividade")

def planejamento(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "planejamento.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        habilidade = request.POST.get("habilidade")
        metas_curto_prazo = request.POST.get("meta_curto_prazo")
        metas_medio_prazo = request.POST.get("meta_medio_prazo")
        metas_longo_prazo = request.POST.get("meta_longo_prazo")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
            if planejamento1:
                messages.error(request, "planejamento ja cadastrado", extra_tags="danger")
                return redirect("planejamento")
            Planejamento.objects.create(estudante=estudante, habilidade=habilidade,
                                        metas_curto_prazo=metas_curto_prazo,
                                        metas_medio_prazo = metas_medio_prazo,
                                        metas_longo_prazo = metas_longo_prazo)
            messages.success(request, "planejamento cadastrado")
            return redirect("planejamento")
        messages.error(request, "planejamento não cadastrado", extra_tags="danger")
        return redirect("planejamento")

def habilidade_academica(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, 'habilidade_academica.html', dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        componente = request.POST.get("componente")
        adaptacao = request.POST.getlist("adaptacao")
        adaptacao = ", ".join(adaptacao)
        habilidade = request.POST.get("habilidade")
        facilidade_dificuldade = request.POST.get("facilidade_dificuldade")
        meta_turma = request.POST.get("meta_turma")
        meta_especifica = request.POST.get("meta_especifica")
        procedimento = request.POST.get("procedimento")
        avaliacao = request.POST.get("avaliacao")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
            if habilidade_academica1:
                messages.error(request, "habilidade academica ja cadastrado", extra_tags="danger")
                return redirect("habilidade_academica")
            HabilidadeAcademica.objects.create(estudante=estudante,
                                               componente_curricular=componente,
                                               adaptacao_curricular = adaptacao,
                                               habilidade = habilidade,
                                               facilidade_dificuldade = facilidade_dificuldade,
                                               metas_turma = meta_turma, metas_especifica = meta_especifica,
                                               procedimento_metodologico = procedimento,
                                               avaliacao = avaliacao)
            messages.success(request, "habilidade_academica cadastrado")
            return redirect("habilidade_academica")
        messages.error(request, "habilidade_academica não cadastrado", extra_tags="danger")
        return redirect("habilidade_academica")

def checklist2(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        checklist = []
        lista = []
        estudante = Estudante.objects.all()
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
        dicionario = {"lista":lista, "estudantes":estudante}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = request.POST.get("tipo")
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, f"{tipo} cadastrado")
            return redirect("checklist2")
        messages.error(request, f"{tipo} não cadastrado", extra_tags="danger")
        return redirect("checklist2")

def gerar_pdf(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "gerar_pdf_matricula.html", dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        pei1 = PEI.objects.filter(estudante=estudante).first()
        if pei1:
            professor = pei1.professor
        else:
            professor = None
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
        html = render_to_string("gerar_pdf.html", dicionario)
        pdf = HTML(string=html).write_pdf()
        return HttpResponse(pdf, content_type="application/pdf")

def estudante_cadastrado(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudantes = Estudante.objects.all()
    dicionario = {"estudantes":estudantes}
    return render(request, "estudantes_cadastrados.html", dicionario)

def remover_estudante(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudantes = Estudante.objects.all()
        dicionario = {"estudantes":estudantes}
        return render(request, "remover_estudante.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("estudante")
        if matricula.isdigit():
            matricula = int(matricula)
            estudante = Estudante.objects.filter(matricula=matricula).first()
            if estudante:
                estudante.delete()
                messages.success(request, "estudante removido")
                return redirect("remover_estudante")
            messages.error(request, "estudante não removido", extra_tags="danger")
            return redirect("remover_estudante")

def remover_professor(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        professor = Professor.objects.all()
        dicionario = {"professores":professor}
        return render(request, "remover_professor.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        matricula = request.POST.get("matricula")
        if matricula.isdigit():
            matricula = int(matricula)
            professor = Professor.objects.filter(matricula=matricula).first()
            if professor:
                professor.delete()
                messages.success(request, "profesoor removido")
                return redirect("remover_profesoor")
            messages.error(request, "profesoor não removido", extra_tags="danger")
            return redirect("remover_profesoor")

def remover_funcionario(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        funcionario = Funcionario.objects.all()
        dicionario = {"funcionarios":funcionario}
        return render(request, "remover_funcionario.html", dicionario)
    if request.method == "POST":
        # pega os dados da requisicao
        cpf = request.POST.get("cpf")
        if cpf.isdigit():
            cpf = int(cpf)
            funcionario = Funcionario.objects.filter(cpf=cpf).first()
            if funcionario:
                funcionario.delete()
                messages.success(request, "funcionario removido")
                return redirect("remover_funcionario")
            messages.error(request, "efuncionario não removido", extra_tags="danger")
            return redirect("remover_funcionario")

def professor_cadastrado(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    professor = Professor.objects.all()
    dicionario = {"professores":professor}
    return render(request, "professores_cadastrados.html", dicionario)

def funcionario_cadastrado(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    funcionario = Funcionario.objects.all()
    dicionario = {"funcionarios":funcionario}
    return render(request, "funcionarios_cadastrados.html", dicionario)

def gerenciar_professor(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_professor.html")

def gerenciar_estudante(request):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_estudante.html")

def gerenciar_funcionario(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_funcionario.html")

def cadastrar_pei(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "cadastrar_pei.html")

def remover_pei(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        pei1 = PEI.objects.filter(estudante=estudante).first()
        if pei1:
            pei1.delete()
            messages.success(request, "pei removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "pei não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_diagnostico(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
        if diagnostico1:
            diagnostico1.delete()
            messages.success(request, "diagnostico removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "diagnostico não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)


def remover_historico_escolar(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
        if historico_escolar1:
            historico_escolar1.delete()
            messages.success(request, "historico escolar removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "historico escolar não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_perfil_estudante(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
        if perfil_estudante1:
            perfil_estudante1.delete()
            messages.success(request, "perfil estudante removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "perfil estudante não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_checklist(request, matricula, id1):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        checklist1 = Checklist.objects.filter(id=id1).first()
        if checklist1:
            checklist1.delete()
            messages.success(request, "checklist removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "checklist não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_atividade(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        atividade1 = Atividade.objects.filter(estudante=estudante).first()
        if atividade1:
            atividade1.delete()
            messages.success(request, "atividade removida")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "atividade não encontrada", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_planejamento(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()

    if estudante:
        planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
        if planejamento1:
            planejamento1.delete()
            messages.success(request, "planejamento removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "planejamento não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_equipe_pei(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante)
        if funcionario_estudante:
            funcionario_estudante.delete()
            messages.success(request, "equipe pei removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "equipe pei não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def remover_habilidade_academica(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudante = Estudante.objects.filter(matricula=matricula).first()
    if estudante:
        habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante)
        if habilidade_academica1:
            habilidade_academica1.delete()
            messages.success(request, "habilidade academica removido")
            return redirect("dados_pei", matricula=matricula)
        else:
            messages.error(request, "habilidade academica não encontrado", extra_tags="danger")
            return redirect("dados_pei", matricula=matricula)
    else:
        messages.error(request, "estudante não encontrado", extra_tags="danger")
        return redirect("dados_pei", matricula=matricula)

def verificar_formulario(formulario, modelo):
    if modelo:
        formulario1 = formulario(instance=modelo)
    else:
        formulario1 = None
    return formulario1

def dados_pei(request, matricula):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    lista = []
    numero = 0
    estudante = Estudante.objects.filter(matricula=matricula).first()
    pei1 = PEI.objects.filter(estudante=estudante).first()
    formulario_pei = verificar_formulario(Pei, pei1)
    if formulario_pei:
        for formulario in formulario_pei.fields.keys():
            if formulario == "professor":
                formulario_pei.fields[formulario].widget.attrs["class"] = "form-select"
            if formulario == "tempo":
                formulario_pei.fields[formulario].widget.attrs["class"] = "form-control"
    funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante).first()
    equipe_pei = verificar_formulario(EquipePei, funcionario_estudante)
    if equipe_pei:
        for formulario in equipe_pei.fields.keys():
            if formulario == "funcionario":
                equipe_pei.fields[formulario].widget.attrs["class"] = "form-select"
    diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
    formulario_diagnostico1 = verificar_formulario(FormularioDiagnostico, diagnostico1)
    if formulario_diagnostico1:
        for formulario in formulario_diagnostico1.fields.keys():
            formulario_diagnostico1.fields[formulario].widget.attrs["class"] = "form-control"
    historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
    formulario_historico_escolar = verificar_formulario(FormularioHistoricoEscolar,
                                                        historico_escolar1)
    if formulario_historico_escolar:
        for formulario in formulario_historico_escolar.fields.keys():
            formulario_historico_escolar.fields[formulario].widget.attrs["class"] = "form-control"
            formulario_historico_escolar.fields["texto"].widget.attrs["id"] = "id_texto1"
    perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
    formulario_perfil_estudante = verificar_formulario(FormularioPerfilEstudante,
                                                       perfil_estudante1)
    if formulario_perfil_estudante:
        for formulario in formulario_perfil_estudante.fields.keys():
            formulario_perfil_estudante.fields[formulario].widget.attrs["class"] = "form-control"
    checklist1 = Checklist.objects.filter(estudante=estudante)
    for checklist in checklist1:
        formulario_checklist = verificar_formulario(FormularioChecklist, checklist)
        if formulario_checklist:
            for formulario in formulario_checklist.fields.keys():
                formulario_checklist.fields[formulario].widget.attrs["class"] = "form-control"
            lista.append(formulario_checklist)
    for checklist3 in lista:
        numero += 1
        for formulario in checklist3.fields.keys():
            checklist3.fields[formulario].widget.attrs["id"] = f"{formulario}{numero}"
    atividade1 = Atividade.objects.filter(estudante=estudante).first()
    formulario_atividade = verificar_formulario(FormularioAtividade, atividade1)
    if formulario_atividade:
        for formulario in formulario_atividade.fields.keys():
            formulario_atividade.fields[formulario].widget.attrs["class"] = "form-control"
    planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
    formulario_planejamento = verificar_formulario(FormularioPlanejamento, planejamento1)
    if formulario_planejamento:
        formulario_planejamento.fields["habilidade"].widget.attrs["id"] = "habilidade1"
        for formulario in formulario_planejamento.fields.keys():
            formulario_planejamento.fields[formulario].widget.attrs["class"] = "form-control"
    habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
    formulario_habilidade_academica = verificar_formulario(FormularioHabilidadeAcademica, habilidade_academica1)
    if formulario_habilidade_academica:
        formulario_habilidade_academica.fields["habilidade"].widget.attrs["id"] = "habilidade2"
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

def editar_pei(request, matricula):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        pei1 = PEI.objects.filter(estudante=estudante).first()
        formulario = Pei(request.POST, instance=pei1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "pei editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "pei não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_equipe_pei(request, matricula):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        funcionario_estudante = FuncionarioEstudante.objects.filter(estudante=estudante).first()
        formulario = EquipePei(request.POST, instance=funcionario_estudante)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "equipe pei editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "funcionario não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_diagnostico(request, matricula):
    #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        diagnostico1 = Diagnostico.objects.filter(estudante=estudante).first()
        formulario = FormularioDiagnostico(request.POST, instance=diagnostico1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "diagnostico editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "diagnostico não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_historico_escolar(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        historico_escolar1 = HistoricoEscolar.objects.filter(estudante=estudante).first()
        formulario = FormularioHistoricoEscolar(request.POST, instance=historico_escolar1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "historico escolar editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "historico escolar não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_perfil_estudante(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        perfil_estudante1 = PerfilEstudante.objects.filter(estudante=estudante).first()
        formulario = FormularioPerfilEstudante(request.POST, instance=perfil_estudante1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "perfil estudante editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "perfil estudante não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_checklist(request, matricula, id1):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        checklist1 = Checklist.objects.filter(id=id1).first()
        formulario = FormularioChecklist(request.POST, instance=checklist1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "checklist editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "checklist não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_atividade(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        atividade1 = Atividade.objects.filter(estudante=estudante).first()
        formulario = FormularioAtividade(request.POST, instance=atividade1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "atividade editada com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "atividade não editada", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_planejamento(request, matricula):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        planejamento1 = Planejamento.objects.filter(estudante=estudante).first()
        formulario = FormularioPlanejamento(request.POST, instance=planejamento1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "planejamento editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "planejamento não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def editar_habilidade_academica(request, matricula):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return redirect("dados_pei", matricula=matricula)
    if request.method == "POST":
        estudante = Estudante.objects.filter(matricula=matricula).first()
        habilidade_academica1 = HabilidadeAcademica.objects.filter(estudante=estudante).first()
        formulario = FormularioHabilidadeAcademica(request.POST, instance=habilidade_academica1)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "habilidade academica editado com sucesso")
            return redirect("dados_pei", matricula)
        else:
            messages.error(request, "habilidade academica não editado", extra_tags="danger")
            return redirect("dados_pei", matricula)

def gerenciar_pei(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return render(request, "gerenciar_pei.html")

def gerenciar_pei_matricula(request):
     #verifica se tem uma chave chamada sistema_professor_cpf na sessao
    #se nao tiver envia a mensagem de faça o login e redireciona para pagina de login
    #se tiver renderiza a pagina do painel do administrador
    #a chave sistema_professor_cpf da sessao e criada no login, se nao tem a chave, e porque
    #o login nao foi feito
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        estudante = Estudante.objects.all()
        dicionario = {"estudantes":estudante}
        return render(request, "gerenciar_pei_matricula.html", dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        return redirect("dados_pei", matricula=matricula)