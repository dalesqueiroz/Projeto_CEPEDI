from tkinter.constants import CASCADE

from django.db import models

# Create your models here.

class Estudante(models.Model):
    cpf = models.BigIntegerField()
    matricula = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    data_de_nascimento = models.DateField()
    curso = models.CharField(max_length=255)
    periodo = models.IntegerField()
    turma = models.CharField(max_length=255)
    ingresso = models.DateField()
    nota = models.FloatField()
    telefone = models.CharField(max_length=255)
    email = models.EmailField()
    pai = models.CharField(max_length=255)
    mae = models.CharField(max_length=255)
    telefone_responsavel = models.CharField(max_length=255)
    email_responsavel = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.matricula} - {self.nome}"

class Diagnostico(models.Model):
    laudo = models.CharField(max_length=255)
    texto = models.TextField()
    ano_diagnostico = models.IntegerField()
    atendimento_fora_da_escola = models.CharField()
    texto_atendimento = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class HistoricoEscolar(models.Model):
    texto = models.TextField()
    texto2 = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class PerfilEstudante(models.Model):
    interesse = models.TextField()
    habilidade = models.TextField()
    nao_gosta = models.TextField()
    dificuldade = models.TextField()
    informacao = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete = models.CASCADE )
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class Checklist(models.Model):
    checklist = models.TextField()
    pergunta = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    texto = models.TextField()
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class Atividade(models.Model):
    atividade = models.CharField()
    descricao = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class Planejamento(models.Model):
    habilidade = models.TextField()
    metas_curto_prazo = models.TextField()
    metas_medio_prazo = models.TextField()
    metas_longo_prazo = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class AvaliacaoPedagogica(models.Model):
    texto = models.TextField()
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class HabilidadeAcademica(models.Model):
    componente_curricular = models.TextField()
    adaptacao_curricular = models.TextField()
    habilidade = models.TextField()
    facilidade_dificuldade = models.TextField()
    metas_turma = models.TextField()
    metas_especifica = models.TextField()
    procedimento_metodologico = models.TextField()
    avaliacao = models.TextField()
    estudante =  models.ForeignKey(Estudante, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class Professor(models.Model):
    cpf = models.BigIntegerField()
    nome = models.CharField(max_length=255)
    matricula = models.BigIntegerField(primary_key=True)
    data_de_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.matricula} - {self.nome}"

class Funcionario(models.Model):
    cpf = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    funcao = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.cpf} - {self.nome}"

class FuncionarioEstudante(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)

class PEI(models.Model):
    estudante =  models.ForeignKey(Estudante, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tempo = models.DateField()
    def __str__(self):
        return f"{self.estudante.matricula} - {self.estudante.nome}"

class SistemaProfessor(models.Model):
    cpf = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.cpf} - {self.nome}"

class RegistroPedagogico(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    texto = models.TextField()

