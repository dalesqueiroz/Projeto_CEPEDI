from django import forms
from .models import (PEI, FuncionarioEstudante, Diagnostico, HistoricoEscolar, PerfilEstudante,
                     Checklist, Atividade, Planejamento, HabilidadeAcademica)

class Pei(forms.ModelForm):
    class Meta:
        model = PEI
        exclude = ["estudante"]

class EquipePei(forms.ModelForm):
    class Meta:
        model = FuncionarioEstudante
        exclude = ["estudante"]

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