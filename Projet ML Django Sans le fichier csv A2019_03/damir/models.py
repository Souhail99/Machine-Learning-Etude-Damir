from django.db import models
from plotly.offline import plot
import plotly.graph_objs as go
from io import StringIO
from .models import *
from plotly.graph_objs import Scatter
import numpy as np 
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
from urllib.request import urlopen
from django.template import loader
from plotly.offline import plot
import json
import os
import seaborn as sns
import random
from io import BytesIO
import base64
import urllib
# Create your models here.

current_path = os.path.dirname(__file__)

path = os.path.join(current_path, 'A2019_03.csv')



Liste={}
ListeColonnes=['AGE_BEN_SNDS',
'ASU_NAT', 
'ATT_NAT',
'BEN_CMU_TOP', 
'BEN_QLT_COD',
'BEN_RES_REG',
'ETE_REG_COD', 
'BEN_SEX_COD', 
'DDP_SPE_COD',
'ETE_TYP_SNDS',  
'SOI_MOI',
'SOI_ANN',
'PRS_NAT',
'PRS_PAI_MNT', 
'PRS_PPU_SEC',
'PRS_REM_TYP', 
'PSE_ACT_CAT',
'PSP_ACT_CAT' ]

ListeDef=['Tranche Age Bénéficiaire au moment des soins',
'Nature Assurance',
'Nature Accident du Travail',
'Top Bénéficiaire CMU-C',
'Qualité du Bénéficiaire',
'Région de Résidence du Bénéficiaire',
'Région Implantation Etb Exécutant',
'Sexe du Bénéficiaire',
'Discipline de Prestation Etb Exécutant',
'Type Etb Exécutant',
'Mois de Soins',
'Année de Soins',
'Nature de Prestation',
'Montant de la Dépense', 
'Code Secteur Privé/Public',
'Type de Remboursement',
'Catégorie de Exécutant',
'Catégorie du Prescripteur']


reg = {
            5:"Régions et Départements d'outre-mer" ,
            11:	"Ile-de-France",
            24:	"Centre-Val de Loire",
            27:	"Bourgogne-Franche-Comté",
            28:	"Normandie",
            32:	"Hauts-de-France - Nord-Pas-de-Calais-Picardie",
            44:	"Grand Est",
            52:	"Pays de la Loire",
            53:	"Bretagne",
            75:	"Aquitaine-Limousin-Poitou-Charentes",
            76:	"Languedoc-Roussillon-Midi-Pyrénées",
            84:	"Auvergne-Rhône-Alpes",
            93:	"Provence-Alpes-Côte d'Azur et Corse",
            99:	"Inconnu"}


for i in range(len(ListeColonnes)):
    Liste[ListeColonnes[i]]=ListeDef[i]

p=0.01
#Ici on lit on prend p% des lignes grâce à skiprows et une expression lambda
df = pd.read_csv(path,sep=';',usecols=ListeColonnes,skiprows=lambda i: i>0 and random.random() > p)

data=df.copy()

class Modele_Ben:

    def Executant_vs_Beneficiaires():
        #Affichons cela sur un graphique les deux comparaison afin d'avoir une meilleure vue d'ensembles :
     
        dtest=df.groupby(['BEN_RES_REG']).size().reset_index(name='count')
        dtest2=df.groupby(['ETE_REG_COD']).size().reset_index(name='count')
        dtest22=dtest2[dtest2['count']<=100000]


        pandasDF1 = dtest
        pandasDF2 = dtest22

        #On rename la colonne car ce sont les memes regions mais pour étudier on a besion d'un seul nom de colonne
        pandasDF2=pandasDF2.rename(columns={'ETE_REG_COD':'BEN_RES_REG'})

        pandasDF1['hue']='BEN_RES_REG'
        pandasDF2['hue']='ETE_REG_COD'



        res=pd.concat([pandasDF1,pandasDF2])
        fig=px.bar(data_frame=res,x='BEN_RES_REG',y='count',color='count',color_discrete_sequence=px.colors.sequential.Rainbow,height=700,width=800)
        fig.update_layout(
            autosize=False,
            width=800,
            height=800,
            
            paper_bgcolor="LightSteelBlue",)
        fig.update_traces(width=4)


        return plot(fig,output_type='div')


    

    def Sex_Rate_Ben():
        newdf=df.copy()
        sums = newdf.groupby(['BEN_SEX_COD']).size().reset_index(name='count')
        fig = px.pie(sums, values=sums['count'], names=sums.index, color_discrete_sequence=px.colors.sequential.RdBu,title='Ratio : Hommes (2) / Femmes (1) / Inconnu ou Personne morale sans civilité (0) ')
        fig.update_layout(
            autosize=False,
            width=750,
            height=800)
        return plot(fig,output_type='div')
    
    def Montant_Depenses():
        #1er graphe

        Modele_Ben.viz1=data[["PRS_PAI_MNT", "PRS_REM_TYP","BEN_RES_REG"]].dropna()
        vf_type = Modele_Ben.viz1.groupby(["BEN_RES_REG"]).mean().sort_values("PRS_PAI_MNT",ascending=False)
        vf_type = vf_type.sort_values("BEN_RES_REG")
 
        vf_type['region']= vf_type.index.map(reg)
        
        fig = px.bar(vf_type,x = 'region',y = vf_type["PRS_PAI_MNT"])
        
            
        fig.update_layout(
            title_text="Les moyennes des Paiements dépensés par régions " 
        )
        return plot(fig,output_type='div')

    def Montant_Rembourses():
        #2eme graphe
        Modele_Ben.viz1=data[["BEN_RES_REG","PRS_PAI_MNT", "PRS_REM_TYP"]].dropna()
        vf_type = Modele_Ben.viz1.groupby(["BEN_RES_REG"]).mean().sort_values("PRS_REM_TYP",ascending=False)
        vf_type = vf_type.sort_values("BEN_RES_REG")
        vf_type['region']= vf_type.index.map(reg)
        fig2 = px.bar(vf_type,x = 'region',y = vf_type["PRS_REM_TYP"],log_y = True)
            
        fig2.update_layout(
            title_text="Les moyennes des Paiements remboursés par régions " 
        )
        return plot(fig2,output_type='div')
             


class Modele_Reg():

    def Carte_Reg():
        viz4 = data[["AGE_BEN_SNDS", "BEN_SEX_COD","BEN_RES_REG"]].dropna()
        viz4 = viz4.groupby(["AGE_BEN_SNDS","BEN_SEX_COD"])

        viz5=viz4.apply(lambda x:x)
        viz5.to_csv("Bénéficiaires.csv")
        dfMap=pd.read_csv(r"Bénéficiaires.csv")
        #On récupère le fichier json contenant toutes les régions
        request2 = urlopen("https://france-geojson.gregoiredavid.fr/repo/regions.geojson")
        frmap = json.load(request2)

        reg_id_map={}
        for feature in frmap['features']:
            feature['id']=feature['properties']['code']
            reg_id_map[feature['properties']['nom']]=feature['id']


        #On enleve la colone index
        dfMap = dfMap.iloc[: , 1:]

        #Supprimons le 99 car c'est region inconnu
        dfMap.drop(dfMap[dfMap['BEN_RES_REG'] == 99].index, inplace = True)

        grouped_df=dfMap.groupby('BEN_RES_REG')
        mean_df = grouped_df.mean()
        dfMap=mean_df.reset_index()

        fig=px.choropleth(dfMap,locations='BEN_RES_REG', geojson=frmap, 
                        color='AGE_BEN_SNDS',title='Age moyen des bénéficiaires par région française')
        fig.update_geos(fitbounds="locations", visible=False)
        return plot(fig,output_type='div')

