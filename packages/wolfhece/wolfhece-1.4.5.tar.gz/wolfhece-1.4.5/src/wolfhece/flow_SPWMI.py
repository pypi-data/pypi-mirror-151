import requests
import pandas as pd
import numpy as np
from calendar import monthrange
from datetime import timedelta, date
import matplotlib.pyplot as plt
import datetime as dt
import pyextremes as eva

from .PyTranslate import _

STATIONS_MI_FLOW="""6228	CHAUDFONTAINE
1951	TUBIZE
2341	CLABECQ
2371	RONQUIERES
2473	OISQUERCQ
2483	RONQUIERES Bief Aval
2536	GOUY
2537	GOUYCanal
2707	LESSINESBiefAmont
2713	PAPIGNIESBiefAval
2952	IRCHONWELZ
2971	ATHDENDREORIENTALE
3274	KAIN Avnt Bar-Ecl
3282	TOURNAI
3561	BOUSSOIT
3643	HYON
3778	SAINT-DENIS
3884	COMINES Aval Bar-Ecl
3886	COMINES Amont
3891	PLOEGSTEERT
5291	KELMIS
5436	LIXHE Aval
5447	LIXHE Bief Amont
5572	BERGILERS Amont
5771	HACCOURT
5796	MAREXHE
5804	ANGLEUR GR
5806	ANGLEUR GR
5826	SAUHEID
5857	MERy
5904	COMBLAIN-AU-PONT
5921	TABREUX
5922	HAMOIR
5953	DURBUY
5962	HOTTON
5991	NISRAMONT
6021	MABOMPRe
6122	ORTHO
6228	CHAUDFONTAINE
6387	EUPEN
6517	POLLEUR
6526	BELLEHEID
6621	MARTINRIV
6651	REMOUCHAMPS
6671	TARGNON
6732	STAVELOT
6753	LASNENVILLE
6803	CHEVRON
6832	TROIS-PONTS
6933	MALMEDY
6946	BEVERCE
6971	WIRTZFELD
6981	BULLINGEN
6991	MALMEDY
7117	IVOZ-RAMET
7132	AMAY
7137	AMPSIN
7139	HUYUS
7141	HUY
7228	MODAVE
7242	MOHA
7244	HUCCORGNE
7319	SALZINNES
7394	MONCEAU_Aval_Bar-EcL
7396	MONCEAU_AmBar-Ecl
7466	FONT-VALMON_Am B-E
7474	LABUISSIERE__Av B-E
7487	SOLRE
7711	JAMIOUL
7781	WALCOURT
7784	WALCOURT
7812	WALCOURT-VOGENEE
7831	SILENRIEUX
7843	BOUSSU-LEZ-WALCOURT
7863	SILENRIEUX
7883	SOUMOY
7891	CERFONTAINE
7944	WIHERIES
7978	BERSILLIES-L'ABBAYE
8017	PROFONDEVILLE
8022	LUSTIN
8059	DINA
8067	ANSEREMME Monia
8134	YVOIR
8163	WARNANT
8166	SOSOYE
8181	FOY
8221	GENDRON
8231	HOUYET
8341	DAVERDISSE
8527	JEMELLE
8622	HASTIERE
8661	FELENNE
8702	CHOOZ
9021	TREIGNES
9071	COUVIN
9081	NISMES
9111	MARIEMBOURG
9201	COUVIN Ry de Rome
9221	PETIGNY Ry de Rome
9223	PETIGNY Ermitage
9224	PETIGNY Fd Serpents
9232	BRULY RY PERNELLE
9434	MEMBRE Pont
9435	MEMBRE Amont
9461	BOUILLON
9531	LACUISINE
9541	CHINY
9561	TINTIGNY
9571	SAINTE-MARIE
9651	STRAIMONT
9741	TORGNY
9914	REULAND
9926	SCHOENBERG
"""

STATS_HOURS_IRM=np.asarray([1,2,3,6,12,24,2*24,3*24,4*24,5*24,7*24,10*24,15*24,20*24,25*24,30*24],dtype=np.int32)
STATS_MINUTES_IRM=np.asarray(STATS_HOURS_IRM)*60

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def is_bissextile(years):
    if(years%4==0 and years%100!=0 or years%400==0):
        return True
    else:
        return False
    
class SPW_MI_flows():
    '''
    Gestion des données pluviographiques du SPW-MI au travers de l'ancien site web "voies-hydrauliques.be"
    http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/
    '''

    def __init__(self) -> None:
        #Création de 2 dictionnaires de recherche sur base de la chaîne
        self.code2name={}
        self.name2code={}
        
        for mystations in STATIONS_MI_FLOW.splitlines():
            mycode,myname=mystations.split("\t")
            self.code2name[mycode]=myname
            self.name2code[myname.lower()]=mycode
            
    def get_names(self):
        return list(self.name2code.keys())
    def get_codess(self):
        return list(self.code2name.keys())

    def get_dailyflow_fromweb(self,year=2021,code='',name=''):
        
        station=code
        if name!="":
            station=self.name2code[name.lower()]
        
        #il faut chercher les mois 
        name_month=12
        url="http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/annuaires/statjourtab.do?code="+station+ "1002&annee="+str(year)
        res=requests.get(url)
        html_tables = pd.read_html(res.content, match='.+')
        Tableau=html_tables[12].to_numpy()[0:31,1:name_month+1].astype('float')
        Tableau=Tableau.transpose().tolist()
        
        remove = []
        for j in range(12):
            if j==1:
                i=28
                if is_bissextile(year):
                    remove+=[[j,29]]
                    remove+=[[j,30]]
                    del Tableau[j][29]
                    del Tableau[j][29]
                else:
                    remove+=[[j,28]]
                    remove+=[[j,29]]
                    remove+=[[j,30]]
                    for l in range(3):
                        del Tableau[j][28]
            else:
                i=30
                if j in [3,5,8,10]:
                    remove += [[j,30]]
                    del Tableau[j][30]
        data=[]
        for i in Tableau:
            data += i 
            
        startdate = dt.date(year,1,1)
        enddate = startdate+pd.DateOffset(year=1)
        flow = pd.Series(data,index=pd.date_range(startdate,enddate,closed='left',freq='1D'))
        # flow= np.array(data)
        return flow
 

    def get_flow_fromweb(self,fromyear,toyear,code='',name='',filterna=True):
        flow=[]
        for curyear in range(fromyear,toyear+1):
            flow.append(self.get_yearflow_fromweb(curyear,code,name,filterna))            
        return pd.concat(flow)
    
    def get_yearflow_fromweb(self,year=2021,code='',name='',filterna=True):
        flow=[]
        for curmonth in range(1,13):
            flow.append(self.get_hourlyflow_fromweb(curmonth,year,code,name))
            
        flow = pd.concat(flow)
        
        if filterna:
            flow[flow.isna()]=0.
            
        return flow

    def get_hourlyflow_fromweb(self,month='',year='',code='',name=''):
        #récupération des données au pas horaire depuis le site SPW-MI VH
        #http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/

        station=code
        if name!="":
            station=self.name2code[name.lower()]

        nbdays = monthrange(year, month)[1] 

        url="http://voies-hydrauliques.wallonie.be/opencms/opencms/fr/hydro/Archive/annuaires/stathorairetab.do?code="+station+"1002&mois="+str(month)+"&annee="+str(year)

        res=requests.get(url)
        html_tables = pd.read_html(res.content, match='.+')

        flow = html_tables[12].to_numpy()[0:24,1:nbdays+1].astype('float').reshape(24*nbdays,order='F')

        startdate = dt.date(year,month,1)
        enddate = startdate+pd.DateOffset(months=1)
        flow = pd.Series(flow,index=pd.date_range(startdate,enddate,closed='left',freq='1H'))

        return flow
 
    def plot(self,name,years=np.arange(2008,2022)):
        
        STATS_day_SPW=np.linspace(0,365,365)
        STATS_days_SPW= np.linspace(0,366,366)

        for curyear in years:
            myflow=self.get_yearflow_fromweb(year=curyear,name=name)
            if len(myflow)==365:
                plt.plot(STATS_day_SPW,myflow,'.',label='Year:{:.0f}'.format(curyear))
            else:
                plt.plot(STATS_days_SPW,myflow,'.',label='Year:{:.0f}'.format(curyear))

        plt.xticks(np.arange(0, 366, 31),['Jan','Feb','Mrch','April','May','June','July','August','Sep','Oct','Nov','Dec'])
        plt.xlabel(_('Time (days)'))
        plt.ylabel(_('Flow  (m3/s) '))
        plt.title('Station: CHAUDFONTAINE',loc='center')
        plt.legend().set_draggable(True)
        plt.grid()
        plt.show()        
    
if __name__=="__main__":
    #exemple
    my = SPW_MI_flows()
    myflow=my.get_yearflow_fromweb(name="Jalhay")
