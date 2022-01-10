from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from .models import Modele_Ben,Modele_Reg
from plotly.offline import plot
from plotly.graph_objs import Scatter

def index(request):
    return HttpResponse(render(request,'index.html'))
    

def damir(request):
    context = {}
    context["graph1"] = Modele_Reg.Carte_Reg()
    return render(request, "damir.html", context=context)


def beneficiaires(request):

    context = {}
    context["graph1"] = Modele_Ben.Executant_vs_Beneficiaires()
    context["graph2"] = Modele_Ben.Sex_Rate_Ben()
    context["graph3"] = Modele_Ben.Montant_Depenses()
    context["graph4"] = Modele_Ben.Montant_Rembourses()

    return render(request, "beneficiaires.html", context=context)

