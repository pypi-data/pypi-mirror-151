from xml.etree.ElementInclude import include
import requests
import pandas as pd
import numpy as np
from calendar import month, monthrange
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from sympy import lowergamma
import time

from .PyTranslate import _

STATIONS_MI_RAIN="""92150015	PETIGNY Barrage
92880015	CUL-DES-SARTS
91370015	BOUSSU-EN-FAGNE
10430015	WAVRE
10810015	BOUSVAL
60480015	RACHAMPS-NOVILLE
61280015	ORTHO
61680015	SAINT-HUBERT aéro
68580015	TAILLES
70030015	SART-TILMAN
70160015	OUFFET
70180015	MEAN
70480015	EREZEE
70870015	MARCHE
10570015	LOUVAIN LA NEUVE
15790015	PERWEZ
15840015	HELECINE
18980015	UCCLE
19540015	TUBIZE
19970015	SOIGNIES
23480015	LILLOIS
23880015	SENEFFE
24590015	DERGNEAU
28920015	ENGHIEN
29930015	CHIEVRES
32770015	KAIN
34760015	MOUSCRON
35340015	WASMUEL
35720015	TRIVIERES
36280015	ROISIN
36470015	ROUVEROY
36490015	BLAREGNIES
37170015	PERUWELZ
38850015	COMINES Barrage-Ecl
52840015	GEMMENICH
55780015	WAREMME
55960015	AWANS
56490015	BATTICE
57570015	LANAYE
64970015	TERNELL
65290015	MONT-RIGI
65380015	SPA aerodrome
65500015	JALHAY
66570015	LOUVEIGNE
67120015	COO INF.
67120115	COO INF.
67180015	COO SUP.
67180115	COO SUP.
68480015	VIELSALM
69580015	ROBERTVILLE
69670015	BUTGENBACH
69670115	BUTGENBACH
71680015	LANDENNE
72280015	MODAVE
72960015	VEDRIN
73350015	MORNIMONT Bar-Ecluse
73690015	CHATELET
73950015	MONCEAU Bar-Ecluse
74850015	SOLRE S/S Bar-Ecluse
75770015	MOMIGNIES
76290015	LIGNY
76780015	GERPINNES
78650015	PLATE TAILLE
78880015	SENZEILLES
79670015	SIVRY
80630015	ANSEREMME
81280015	SAINT-GERARD
81380015	CRUPET
81570015	CINEY
81890015	FLORENNES
83480015	DAVERDISSE
83880015	LIBIN
84680015	BEAURAING
85180015	ROCHEFORT
85380015	NASSOGNE
86770015	GEDINNE
86870015	CROIX-SCAILLE
94360015	VRESSE
94690015	BOUILLON
95740015	FRATIN
95880015	MEIX-LE-TIGE
95960015	ARLON
95960115	ARLON
96170015	SUGNY
96320015	BERTRIX
96520015	STRAIMONT
96980015	NAMOUSSART
97430015	TORGNY
97810015	ATHUS
97940015	AUBANGE
97970015	SELANGE
98160015	ORVAL
99150015	STEFFESHAUSEN
99220015	SANKT-VITH
99480015	BASTOGNE
"""

STATS_HOURS_IRM=np.asarray([1,2,3,6,12,24,2*24,3*24,4*24,5*24,7*24,10*24,15*24,20*24,25*24,30*24],dtype=np.int32)
STATS_MINUTES_IRM=np.asarray(STATS_HOURS_IRM)*60

class SPW_MI_pluvioraphs():
    '''
    Gestion des données pluviographiques du SPW-MI au travers de l'ancien site web "voies-hydrauliques.be"
    http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/
    '''

    def __init__(self) -> None:
        #Création de 2 dictionnaires de recherche sur base de la chaîne
        self.code2name={}
        self.name2code={}
        
        for mypluvio in STATIONS_MI_RAIN.splitlines():
            mycode,myname=mypluvio.split("\t")
            self.code2name[mycode]=myname
            self.name2code[myname.lower()]=mycode
            
    def get_names(self):
        return list(self.name2code.keys())
    def get_codes(self):
        return list(self.code2name.keys())

    def get_rain_fromweb(self,fromyear,toyear,code='',name='',filterna=True):
        rain=[]
        for curyear in range(fromyear,toyear+1):
            rain.append(self.get_yearrain_fromweb(curyear,code,name,filterna))       
            print(curyear)     
        return pd.concat(rain)

    def get_yearrain_fromweb(self,year=2021,code='',name='',filterna=True):
        rain=[]
        for curmonth in range(1,13):
            rain.append(self.get_monthrain_fromweb(curmonth,year,code,name))
        
        rain = pd.concat(rain)

        if filterna:
            rain[rain.isna()]=0.            
        
        return rain

    def get_monthrain_fromweb(self,month=7,year=2021,code='',name='',mysleep=.2):
        '''Récupération des données au pas horaire depuis le site SPW-MI VH
        
        On lit les informations pour l'ensemble du mois
        
        http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/
        '''

        station=code
        if name!="":
            station=self.name2code[name.lower()]

        #calcul du nombre de jours dans le mois souhaité
        nbdays = monthrange(year, month)[1] 

        url="http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/annuaires/stathorairetab.do?code="+station+"&mois="+str(month)+"&annee="+str(year)

        res=requests.get(url)
        html_tables = pd.read_html(res.content, match='.+')
        
        startdate = dt.date(year,month,1)
        enddate = startdate+pd.DateOffset(months=1)
        try:
            #analyse du tableau HTML qui contient les données de pluie
            rain = html_tables[12].to_numpy()[0:24,1:nbdays+1].astype('float').reshape(24*nbdays,order='F')
            rain = pd.Series(rain,index=pd.date_range(startdate,enddate,inclusive='left',freq='1H'))
            
        except:
            rain=np.zeros(nbdays*24)
            rain = pd.Series(rain,index=pd.date_range(startdate,enddate,inclusive='left',freq='1H'))
            pass
        
        time.sleep(mysleep)
        
        return rain

    def compute_stats_Q(self,rain,listhours):
        '''
        Calcul des stats des "cumul maximaux" par convolution sur base d'un vecteur de nombre d'heures
        Unité : mm
        '''
        mymaxQ=np.zeros(len(listhours),dtype=np.float64)
        k=0
        
        for locstat in listhours:
            a = np.ones(locstat)
            mymaxQ[k]=np.max(np.convolve(rain,a,'same'))
            k+=1

        return mymaxQ

    def compute_stats_i(self,rain,listhours):
        '''
        Calcul des stats des "intensités moyennes maximales" par convolution sur base d'un vecteur de nombre d'heures
        Unité : mm/h
        '''
        mymeanQ=self.compute_stats_Q(rain,listhours)/np.asarray(listhours,dtype=np.float64)

        return mymeanQ
        
    def plot(self,rain:pd.Series,toshow=False):
        fig,ax = plt.subplots(1,1,figsize=(15,8))
        
        x = rain.index
        
        minyear = x[0].year
        maxyear = x[-1].year+1
        
        xticks = [dt.datetime(minyear,1,1)+pd.DateOffset(months=k) for k in range(0,(maxyear-minyear)*12+1,3)]
        
        ax.fill_between(rain.index,rain.values,step='pre',alpha=0.5)
        ax.step(rain.index,rain.values,where='pre')
        ax.set_xticks(xticks)
        
        if toshow:
            plt.show()
    
    def plot_periodic(self,rain:pd.Series,origin:dt.datetime,offset_in_months,toshow=False):
        fig,ax = plt.subplots(1,1,figsize=(15,8))
        
        end = rain.index[-1]

        startdate=origin
        enddate = origin 
        
        offset = pd.DateOffset(months=offset_in_months)
        
        while enddate<=end:
        
            enddate = startdate + offset
            
            locrain = rain[startdate:enddate]
            
            i1=(locrain.index[0]-startdate).days*24
            x = np.arange(i1,i1+len(locrain.values))
                        
            # ax.fill_between(x,locrain.values,step='pre',alpha=0.5)
            ax.step(x,locrain.values,where='pre')

            startdate=enddate
            
        xticks = [k*30*24 for k in range(offset_in_months+1)]
        ax.set_xticks(xticks)
        ax.set_xticklabels([str(k*30) for k in range(offset_in_months+1)])
        
        if toshow:
            plt.show()                

    def saveas(self,rain:pd.Series,filename:str):
        rain.to_csv(filename,header=['Data'])

    def fromcsv(self,filename:str,fromdate:dt.datetime=None,todate:dt.datetime=None):
        mydata= pd.read_csv(filename,header=0,index_col=0,squeeze=True,parse_dates=True)
        
        if fromdate is None and todate is None:
            return mydata
        elif fromdate is None:
            return mydata[:todate]
        elif todate is None:
            return mydata[fromdate:]
        else:
            return mydata[fromdate:todate]
        
        

if __name__=="__main__":
    #exemple
    my = SPW_MI_pluvioraphs()
    myrain=my.get_monthrain_fromweb(name="Jalhay")
    mystats=my.compute_stats_Q(myrain,STATS_HOURS_IRM)
    print(mystats)
