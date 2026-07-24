from django import forms
from .models import (PEI, FuncionarioEstudante, Diagnostico, HistoricoEscolar, PerfilEstudante,
                     Checklist, Atividade, Planejamento, HabilidadeAcademica,
                     Professor, Estudante, Funcionario)

class Pei(forms.ModelForm):
    class Meta:
        model = PEI
        exclude = ["estudante"]

class EquipePei(forms.ModelForm):
    class Meta:
        model = FuncionarioEstudante
        exclude = ["estudante"]

class EquipePei1(forms.Form):
    funcionarios = forms.ModelMultipleChoiceField(queryset=Funcionario.objects.all(),
                                                  widget=forms.SelectMultiple(attrs={"class":"form-select"}),
                                                  required=False)

class FormularioDiagnostico(forms.ModelForm):
    class Meta:
        model = Diagnostico
        exclude = ["estudante"]

class FormularioHistoricoEscolar(forms.ModelForm):
    class Meta:
        model = HistoricoEscolar
        exclude = ["estudante"]

class FormularioPerfilEstudante(forms.ModelForm):
    class Meta:
        model = PerfilEstudante
        exclude = ["estudante"]

class FormularioChecklist(forms.ModelForm):
    class Meta:
        model = Checklist
        exclude = ["estudante"]


class FormularioAtividade(forms.ModelForm):
    class Meta:
        model = Atividade
        exclude = ["estudante"]

class FormularioPlanejamento(forms.ModelForm):
    class Meta:
        model = Planejamento
        exclude = ["estudante"]

class FormularioHabilidadeAcademica(forms.ModelForm):
    class Meta:
        model = HabilidadeAcademica
        exclude = ["estudante"]

class FormularioProfessor(forms.ModelForm):
    class Meta:
        model = Professor
        exclude = ["matricula"]

class FormularioFuncionario(forms.ModelForm):
    class Meta:
        model = Funcionario
        exclude = ["cpf"]

class FormularioEstudante(forms.ModelForm):
    class Meta:
        model = Estudante
        exclude = ["matricula"]