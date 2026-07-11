import json

from django.core.handlers.base import reset_urlconf
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import (SistemaProfessor, Estudante, Professor, Funcionario, PEI,
                     FuncionarioEstudante, Diagnostico, HistoricoEscolar,
                     PerfilEstudante, Atividade, Planejamento, HabilidadeAcademica,
                     Checklist)
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

# Create your views here.

def cadastro(request):
    return render(request, 'index.html')

def cadastro_sistema(request):
    if request.method == "GET":
        return render(request, 'sistema_cadastro.html')
    if request.method == "POST":
        cpf  = request.POST.get("cpf")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha = make_password(senha)
        SistemaProfessor.objects.create(cpf=cpf, nome=nome, email=email, senha=senha)
        professor = SistemaProfessor.objects.filter(cpf=cpf).first()
        if professor:
            messages.success(request, "O usuario foi cadastrado")
            redirect("login")
        messages.error(request, "O usuario não foi cadastrado", extra_tags="danger")

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        sistema_professor = SistemaProfessor.objects.filter(email=email).first()
        if sistema_professor:
            if check_password(senha, sistema_professor.senha):
                request.session["sistema_professor_cpf"] = sistema_professor.cpf
                request.session["sistema_professor_nome"] = sistema_professor.nome
                return redirect("painel_administrador")
        messages.error(request, "login não realizado", extra_tags="danger")
        return redirect("login")

def sair(request):
    request.session.flush()
    return redirect("login")

def painel_administrador(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "painel_administrador.html")

def cadastro_estudante(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_estudante.html')
    if request.method == "POST":
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
        Estudante.objects.create(cpf=cpf, matricula=matricula, nome=nome,
                                 data_de_nascimento=data_de_nascimento, curso=curso,
                                 periodo=periodo, turma=turma, ingresso = ingresso,
                                 nota=nota, telefone=telefone, email=email, pai=pai, mae=mae,
                                 telefone_responsavel=telefone_responsavel,
                                 email_responsavel=email_responsavel)
        estudante = Estudante.objects.filter(cpf=cpf).first()
        if estudante:
            messages.success(request, "estudante cadastrado")
            return redirect("cadastro_estudante")
        messages.error(request, "estudante não cadastrado", extra_tags="danger")
        return redirect("cadastro_estudante")

def cadastro_professor(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_professor.html')
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        data_de_nascimento = request.POST.get("data_de_nascimento")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        Professor.objects.create(cpf=cpf, nome=nome, matricula=matricula,
                                 data_de_nascimento=data_de_nascimento, email=email,
                                 telefone=telefone)
        professor = Professor.objects.filter(cpf=cpf).first()
        if professor:
            messages.success(request, "professor foi cadastrado")
            return redirect("cadastro_professor")
        messages.error(request, "professor não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_professor")

def cadastro_funcionario(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'cadastro_funcionario.html')
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        funcao = request.POST.get("funcao")
        Funcionario.objects.create(cpf=cpf, nome=nome, funcao=funcao)
        funcionario = Funcionario.objects.filter(cpf=cpf).first()
        if funcionario:
            messages.success(request, "o funcionario foi cadastrado")
            return redirect("cadastro_funcionario")
        messages.warning(request, "o funcionario não foi cadastrado", extra_tags="danger")
        return redirect("cadastro_funcionario")

def pei(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'PEI.html')
    if request.method == "POST":
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1":matricula1}
            return render(request, "PEI.html", dicionario)
        matricula_estudante = request.POST.get("matricula_estudante")
        matricula_professor = request.POST.get("matricula_professor")
        validade = request.POST.get("validade")
        estudante = Estudante.objects.filter(matricula = matricula_estudante).first()
        professor = Professor.objects.filter(matricula = matricula_professor).first()
        if estudante and professor:
            PEI.objects.create(estudante=estudante, professor=professor, tempo=validade)
            messages.success(request, "o pei foi cadastrado")
            return redirect("PEI")
        messages.error(request, "o pei não foi cadastrado", extra_tags="danger")
        return redirect("PEI")

def cadastro_equipe(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        quantidade = request.GET.get("quantidade", 0)
        quantidade = int(quantidade)
        lista = range(quantidade)
        dicionario = {"quantidade":quantidade, "lista":lista}
        return render(request, 'cadastro_equipe.html', dicionario)
    if request.method == "POST":
        quantidade = request.POST.get("quantidade", 0)
        quantidade = int(quantidade)
        quantidade1 = 0
        matricula = request.POST.get("matricula")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        for i in range(quantidade):
            cpf = request.POST.get(f"cpf_{i}")
            funcionario = Funcionario.objects.filter(cpf=cpf).first()
            if estudante and funcionario:
                FuncionarioEstudante.objects.create(estudante=estudante, funcionario=funcionario)
                quantidade1 += 1
        if quantidade == quantidade1:
            messages.success(request, "funcionario cadastrado")
            return redirect("cadastro_equipe")
        messages.error(request, f'{quantidade1} funcionario cadastrado', extra_tags="danger")

def diagnostico(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'diagnostico.html')
    if request.method == "POST":
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1":matricula1}
            return render(request, "diagnostico.html", dicionario)
        estudante = request.POST.get("estudante")
        laudo = request.POST.get("laudo")
        texto_diagnostico = request.POST.get("texto_diagnostico")
        ano = request.POST.get("ano")
        ano = int(ano)
        atendimento = request.POST.get("atendimento")
        texto_atendimento = request.POST.get("texto_atendimento", " ")
        estudante = Estudante.objects.filter(matricula=estudante).first()
        if estudante:
            Diagnostico.objects.create(estudante=estudante, laudo=laudo,
                                       texto=texto_diagnostico, ano_diagnostico=ano,
                                       atendimento_fora_da_escola = atendimento,
                                       texto_atendimento=texto_atendimento)
            messages.success(request, "diagnostico cadastrado")
            return redirect("diagnostico")
        messages.error(request, "diagnostico nao cadastrado", extra_tags="danger")
        return redirect("diagnostico")

def historico_escolar(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'historico_escolar.html')
    if request.method == "POST":
        matricula1 = request.POST.get("matricula1")
        if matricula1:
            dicionario = {"matricula1": matricula1}
            return render(request, "diagnostico.html", dicionario)
        matricula = request.POST.get("matricula")
        texto = request.POST.get("texto")
        texto2 = request.POST.get("texto2")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            HistoricoEscolar.objects.create(texto=texto, texto2=texto2, estudante=estudante)
            messages.success(request, "historico escolar cadastrado")
            return redirect("historico_escolar")
        messages.error(request, "historico escolar não cadastrado", extra_tags="danger")
        return redirect("historico_escolar")

def perfil_estudante(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'perfil_estudante.html')
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        interesse = request.POST.get("interesse")
        habilidade = request.POST.get("habilidade")
        nao_gosta = request.POST.get("nao_gosta")
        desafio = request.POST.get("desafio")
        informacao = request.POST.get("informacao")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            PerfilEstudante.objects.create(estudante=estudante,
                                           interesse=interesse, habilidade = habilidade,
                                           nao_gosta=nao_gosta, dificuldade=desafio,
                                           informacao=informacao)
            messages.success(request, "perfil estudante cadastrado")
            return redirect("perfil_estudante")
        messages.error(request, "perfil estudante não cadastrado", extra_tags="danger")
        return redirect("perfil_estudante")

def atividade(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, "atividade.html")
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        atividade1 = request.POST.get("atividade")
        descricao = request.POST.get("descricao")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Atividade.objects.create(estudante=estudante, atividade=atividade1,
                                     descricao=descricao)
            messages.success(request, "atividade cadastrada")
            return redirect("atividade")
        messages.error(request, "atividade não cadastrada", extra_tags="danger")
        return redirect("atividade")

def planejamento(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, "planejamento.html")
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        habilidade = request.POST.get("habilidade")
        metas_curto_prazo = request.POST.get("meta_curto_prazo")
        metas_medio_prazo = request.POST.get("meta_medio_prazo")
        metas_longo_prazo = request.POST.get("meta_longo_prazo")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Planejamento.objects.create(estudante=estudante, habilidade=habilidade,
                                        metas_curto_prazo=metas_curto_prazo,
                                        metas_medio_prazo = metas_medio_prazo,
                                        metas_longo_prazo = metas_longo_prazo)
            messages.success(request, "planejamento cadastrado")
            return redirect("planejamento")
        messages.error(request, "planejamento não cadastrado", extra_tags="danger")
        return redirect("planejamento")

def habilidade_academica(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, 'habilidade_academica.html')
    if request.method == "POST":
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

def adaptacao_curriculo(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao de acesso ao curriculo"
        checklist = ["Organização dos agrupamentos de estudantes",
                     "Organização do Espaço Físico e Condições Ambientais",
                     "Organização dos Recursos Didáticos",
                     "Organização Didática da Aula"]
        nome = "adaptacao_curriculo"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}

        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao de acesso ao curriculo"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao curriculo cadastrado")
            return redirect("adaptacao_curriculo")
        messages.error(request, "adaptacao curriculo não cadastrado", extra_tags="danger")
        return redirect("adaptacao_curriculo")

def adaptacao_objetivo(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao de objetivo"
        checklist = ["Priorização de habilidades básicas de atenção, participação e adaptabilidade",
                    "Adequação de objetivos, de acordo com a especificidade do(a) estudante",
                    "Retirada de objetivos propostos no currículo escolar",
                    "Introdução de objetivos específicos, complementares e/ou alternativos",]
        nome = "adaptacao_objetivo"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao de objetivo"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao objetivo cadastrado")
            return redirect("adaptacao_objetivo")
        messages.error(request, "adaptacao objetivo não cadastrado", extra_tags="danger")
        return redirect("adaptacao_objetivo")

def adaptacao_conteudo(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao de conteudo"
        checklist = ["Priorização de conteúdos",
                    "Reformulação da sequência dos conteúdos",
                    "Retomada de determinados conteúdos, garantindo seu domínio e consolidação",
                    "Eliminação de conteúdos secundários, para dar enfoque mais intensivo e prolongado a conteúdos mais básicos e essenciais no currículo",
                    "Introdução de conteúdos específicos, complementares ou alternativos" ]
        nome = "adaptacao_conteudo"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao de conteudo"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao conteudo cadastrado")
            return redirect("adaptacao_conteudo")
        messages.error(request, "adaptacao conteudo não cadastrado", extra_tags="danger")
        return redirect("adaptacao_conteudo")

def adaptacao_metodo(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao do metodo de ensino e da organizacao didatica"
        checklist = ["Modificação de procedimentos / estratégias de ensino",
                    "Adoção de métodos, procedimentos e atividades alternativas e/ou complementares às previstas",
                    "Organização diferenciada da sala de aula",
                    "Adaptação de materiais",
                    "Utilização de recursos específicos de acesso ao currículo"]
        nome = "adaptacao_metodo"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao do metodo de ensino e da organizacao didatica"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao metodo cadastrado")
            return redirect("adaptacao_metodo")
        messages.error(request, "adaptacao metodo não cadastrado", extra_tags="danger")
        return redirect("adaptacao_metodo")

def adaptacao_sistema(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao do sistema de avaliacao"
        checklist = ["Adaptação e/ou modificação de técnicas, instrumentos, procedimentos e critérios",
                    "Introdução de critérios específicos de avaliação",
                    "Necessidade de Avaliação em espaço diferente dos colegas",
                    "Eliminação de critérios gerais de avaliação",
                    "Modificação dos critérios de promoção"]
        nome = "adaptacao_sistema"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao do sistema de avaliacao"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao sistema cadastrado")
            return redirect("adaptacao_sistema")
        messages.error(request, "adaptacao sistema não cadastrado", extra_tags="danger")
        return redirect("adaptacao_sistema")

def adaptacao_temporalidade(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        tipo = "adaptacao de temporalidade"
        checklist = ["Aumento do Tempo para atividades e avaliações",
                    "Aumento do tempo para trabalhar determinados objetivos/conteúdos",
                    "Diminuição do tempo para trabalhar determinados objetivos/conteúdos",
                    "Aumento do tempo do estudante em uma série",
                    "Aceleração do estudante para série posterior"]
        nome = "adaptacao_temporalidade"
        dicionario = {"tipo":tipo, "checklist":checklist, "nome":nome}
        return render(request, 'checklist.html', dicionario)
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        checklist = request.POST.getlist("checklist")
        texto = request.POST.get("texto")
        tipo = "adaptacao de temporalidade"
        checklist = "\n".join(checklist)
        estudante = Estudante.objects.filter(matricula=matricula).first()
        if estudante:
            Checklist.objects.create(estudante=estudante, checklist=tipo,
                                     pergunta=checklist, texto=texto)
            messages.success(request, "adaptacao temporalidade cadastrado")
            return redirect("adaptacao_temporalidade")
        messages.error(request, "adaptacao temporalidade não cadastrado", extra_tags="danger")
        return redirect("adaptacao_temporalidade")

def gerar_pdf(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        return render(request, "gerar_pdf_matricula.html")
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        estudante = Estudante.objects.filter(matricula=matricula).first()
        pei1 = PEI.objects.filter(estudante=estudante).first()
        professor = pei1.professor
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
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    estudantes = Estudante.objects.all()
    dicionario = {"estudantes":estudantes}
    return render(request, "estudantes_cadastrados.html", dicionario)

def remover_estudante(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        estudantes = Estudante.objects.all()
        dicionario = {"estudantes":estudantes}
        return render(request, "remover_estudante.html", dicionario)
    if request.method == "POST":
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
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        professor = Professor.objects.all()
        dicionario = {"professores":professor}
        return render(request, "remover_professor.html", dicionario)
    if request.method == "POST":
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
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    if request.method == "GET":
        funcionario = Funcionario.objects.all()
        dicionario = {"funcionarios":funcionario}
        return render(request, "remover_funcionario.html", dicionario)
    if request.method == "POST":
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
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    professor = Professor.objects.all()
    dicionario = {"professores":professor}
    return render(request, "professores_cadastrados.html", dicionario)

def funcionario_cadastrado(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    funcionario = Funcionario.objects.all()
    dicionario = {"funcionarios":funcionario}
    return render(request, "funcionarios_cadastrados.html", dicionario)

def gerenciar_professor(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_professor.html")

def gerenciar_estudante(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_estudante.html")

def gerenciar_funcionario(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "gerenciar_funcionario.html")

def cadastrar_pei(request):
    if not request.session.get("sistema_professor_cpf"):
        messages.warning(request, "faça o  login")
        return redirect("login")
    return render(request, "cadastrar_pei.html")