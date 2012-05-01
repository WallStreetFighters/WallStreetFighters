 # coding: utf-8
__author__="Andrzej Smoliński"
__date__ ="$2012-02-23 19:00:48$"

from ChartData import ChartData
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.finance import candlestick
from matplotlib.ticker import *
from matplotlib.textpath import TextPath
from matplotlib.text import Text
from numpy import *
from PyQt4 import QtGui
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from TechAnalysisModule.candles import *
import TechAnalysisModule.trendAnalysis as trend
import TechAnalysisModule.oscilators as osc
from TechAnalysisModule.strategy import Strategy

    
class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu. Zgodnie z tym, co zasugerował
    Paweł, na jednym wykresie wyświetlam jeden wskaźnik i jeden oscylator, a jak ktoś
    będzie chciał więcej, to kliknie sobie jakiś guzik, który mu pootwiera kilka wykresów
    w nowym oknie."""
    data = None #obiekt klasy Data przechowujący dane    
    
    fig = None #rysowany wykres (tzn. obiekt klasy Figure)
    mainPlot = None #główny wykres (punktowy, liniowy, świecowy)        
    volumeBars = None #wykres wolumenu
    oscPlot = None #wykres oscylatora    
    additionalLines = [] #lista linii narysowanych na wykresie (przez usera, albo przez wykrycie trendu)
    rectangles = [] #lista prostokątów (do zaznaczania świec)
    
    mainType = None #typ głównego wykresu
    oscType = None #typ oscylatora (RSI, momentum, ...)
    mainIndicator = None #typ wskaźnika rysowany dodatkowo na głównym wykresie (średnia krocząca, ...)
    
    x0, y0 = None,None      #współrzędne początku linii        
    drawingMode = False #zakładam, że możliwość rysowania będzie można włączyć/wyłączyć        
    
    scaleType = 'linear' #rodzaj skali na osi y ('linear' lub 'log')                    
    grid = True #czy rysujemy grida
    
    num_ticks = 8 #tyle jest etykiet pod wykresem
    
    #margines (pionowy i poziomy oraz maksymalna wysokość/szerokość wykresu)
    margin, maxSize = 0.1, 0.8     
    #wysokość wolumenu i wykresu oscylatora
    volHeight, oscHeight = 0.1, 0.15        
    
    def __init__(self, parent, finObj=None, width=8, height=6, dpi=100):
        """Konstruktor. Tworzy domyślny wykres (liniowy z wolumenem, bez wskaźników)
        dla podanych danych. Domyślny rozmiar to 800x600 pixli"""                        
        self.additionalLines=[]
        self.rectangles=[]
        self.setData(finObj)
        self.mainType='line'                
        self.fig = Figure(figsize=(width, height), dpi=dpi)        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)        
        self.addMainPlot()
        self.addVolumeBars()                                        
        self.mpl_connect('button_press_event', self.onClick)        
           
    def setData(self, finObj, start=None, end=None, step='daily'):
        """Ustawiamy model danych, który ma reprezentować wykres. Następnie
        konieczne jest jego ponowne odrysowanie"""
        if(finObj==None):
            return;
        self.data=ChartData(finObj, start, end, step)
        if(self.mainPlot!=None):
            self.updatePlot()
    
    def setGrid(self, grid):
        """Włącza (True) lub wyłącza (False) rysowanie grida"""
        self.grid=grid
        self.updateMainPlot()
            
    def setMainType(self, type):
        """Ustawiamy typ głównego wykresu ('point','line','candlestick','none')"""
        self.mainType=type
        self.updateMainPlot()        
        
    def updatePlot(self):
        """Odświeża wszystkie wykresy"""                
        self.updateMainPlot()
        self.updateVolumeBars()
        self.updateOscPlot()                                
        self.draw()        
        self.drawGeometricFormation()
        #self.drawRateLines()
        #self.drawTrend()
        #self.drawCandleFormations()
        #self.drawGaps()
		
    
    def addMainPlot(self):
        """Rysowanie głównego wykresu (tzn. kurs w czasie)"""                                            
        bounds=[self.margin, self.margin, self.maxSize, self.maxSize]
        self.mainPlot=self.fig.add_axes(bounds)                        
        self.updateMainPlot()
    
    def updateMainPlot(self):        
        if(self.mainPlot==None or self.data==None or self.data.corrupted):
            return
        ax=self.mainPlot                
        ax.clear()  
        x=range(len(self.data.close))
        if self.mainType=='line' :
            ax.plot(x,self.data.close,'b-',label=self.data.name)
        elif self.mainType=='point':
            ax.plot(x,self.data.close,'b.',label=self.data.name)
        elif self.mainType=='candlestick':
            self.drawCandlePlot()
        else:            
            return
        if self.mainIndicator != None:
            self.updateMainIndicator()       
        ax.set_xlim(x[0],x[-1])
        ax.set_yscale(self.scaleType)
        ax.set_ylim(0.995*min(self.data.low),1.005*max(self.data.high))                 
        for line in self.additionalLines:
            ax.add_line(line)
            line.figure.draw_artist(line)         
        for rect in self.rectangles:
            ax.add_patch(rect)
            rect.figure.draw_artist(rect)        
        if(self.scaleType=='log'):            
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))            
            ax.yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))            
        for tick in ax.yaxis.get_major_ticks():
            tick.label2On=True
            if(self.grid):
                tick.gridOn=True        
        for label in (ax.get_yticklabels() + ax.get_yminorticklabels()):
            label.set_size(8)
        #legenda
        leg = ax.legend(loc='best', fancybox=True)
        leg.get_frame().set_alpha(0.5)
        self.formatDateAxis(self.mainPlot)        
        self.fixTimeLabels()
        if(self.grid):
            for tick in ax.xaxis.get_major_ticks():
                # print tick.get_loc()
                tick.gridOn=True
    
    def addVolumeBars(self):
        """Dodaje do wykresu wyświetlanie wolumenu."""        
        #tworzymy nowy wykres tylko za pierwszym razem, potem tylko pokazujemy i odświeżamy                
        if(self.volumeBars==None):
            volBounds=[self.margin, self.margin, self.maxSize, self.volHeight]
            self.volumeBars=self.fig.add_axes(volBounds, sharex=self.mainPlot)                                                                               
        self.updateVolumeBars()
        self.volumeBars.set_visible(True)
        self.fixPositions()
        self.fixTimeLabels()
    
    def rmVolumeBars(self):
        """Ukrywa wykres wolumenu"""
        if self.volumeBars==None:
            return
        self.volumeBars.set_visible(False)        
        self.fixPositions()                            
        self.fixTimeLabels()
    
    def setScaleType(self,type):    
        """Ustawia skalę liniową lub logarytmiczną na głównym wykresie."""
        if(type) not in ['linear','log']:
            return        
        self.scaleType=type
        self.updateMainPlot()
        
    def updateVolumeBars(self):
        """Odświeża rysowanie wolumenu"""                
        if self.data==None or self.data.corrupted:
            return        
        ax=self.volumeBars
        ax.clear()
        x=range(len(self.data.close))
        ax.vlines(x,0,self.data.volume)        
        ax.set_xlim(x[0],x[-1])
        if(max(self.data.volume)>0):
            ax.set_ylim(0,1.2*max(self.data.volume))
        for label in self.volumeBars.get_yticklabels():
            label.set_visible(False)                                
        for o in ax.findobj(Text):
            o.set_visible(False)
        self.formatDateAxis(ax)
        self.fixTimeLabels()
        
    def drawCandlePlot(self):
        """Wyświetla główny wykres w postaci świecowej"""    
        
        """candlestick potrzebuje danych w postaci piątek (time, open, close, high, low). 
        time musi być w postaci numerycznej (ilość dni od 0000-00-00 powiększona  o 1).         
        Atrybut width = szerokość świecy w ułamkach dnia na osi x. Czyli jeśli jedna świeca
        odpowiada za 1 dzień, to ustawiamy jej szerokość na ~0.7 żeby był jakiś margines między nimi"""
        if self.data==None or self.data.corrupted:
            return                        
        lines, patches = candlestick(self.mainPlot,self.data.quotes,
                                    width=0.7,colorup='w',colordown='k')                
        #to po to żeby się wyświetlała legenda
        lines[0].set_label(self.data.name)         
        """Ludzie, którzy robili tą bibliotekę byli tak genialni, że uniemożliwili
        stworzenie świec w najbardziej klasycznej postaci, tzn. białe=wzrost, czarne=spadek.
        Wynika to z tego, że prostokąty domyślnie nie mają obramowania i są rysowane POD liniami.
        Poniższy kod to naprawia"""
        for line in lines:                        
            line.set_zorder(line.get_zorder()-2)
        for rect in patches:                                    
            rect.update({'edgecolor':'k','linewidth':0.5})     
    
    def setMainIndicator(self, type):
        """Ustawiamy, jaki wskaźnik chcemy wyświetlać na głównym wykresie"""
        self.mainIndicator=type        
        self.updateMainPlot()
    
    def updateMainIndicator(self):
        """Odrysowuje wskaźnik na głównym wykresie"""
        if self.data==None or self.data.corrupted:
            return
        ax=self.mainPlot
        type=self.mainIndicator
        ax.hold(True) #hold on 
        x=range(len(self.data.close))
        if type=='SMA':
            indicValues=self.data.movingAverage('SMA')        
        elif type=='WMA':
            indicValues=self.data.movingAverage('WMA')
        elif type=='EMA':
            indicValues=self.data.movingAverage('EMA')
        elif type=='bollinger':            
            if self.data.bollinger('upper')!=None:
                ax.plot(x,self.data.bollinger('upper'),'r-',label=type)
            indicValues=self.data.bollinger('lower')
        else:
            ax.hold(False)
            return
        if indicValues!=None:
            ax.plot(x,indicValues,'r-',label=type)
        ax.hold(False) #hold off        
    
    def setOscPlot(self, type):
        """Dodaje pod głównym wykresem wykres oscylatora danego typu lub ukrywa"""
        if type not in ['momentum','CCI','RSI','ROC','williams']:
            """Ukrywa wykres oscylatora"""
            if self.oscPlot==None:
                return
            self.oscPlot.set_visible(False)        
            self.fixPositions()                            
            self.fixTimeLabels()
        else:
            self.oscType=type                
            if self.oscPlot==None:
                oscBounds=[self.margin, self.margin, self.maxSize, self.oscHeight]
                self.oscPlot=self.fig.add_axes(oscBounds, sharex=self.mainPlot)                                            
            self.updateOscPlot()
            self.oscPlot.set_visible(True)
            self.fixPositions()
            self.fixTimeLabels()                
                                    
    def updateOscPlot(self):
        """Odrysowuje wykres oscylatora"""
        if self.oscPlot==None or self.data.corrupted:
            return
        ax=self.oscPlot                
        type=self.oscType
        ax.clear()            
        if type == 'momentum':
            oscData=self.data.momentum()
        elif type == 'CCI':
            oscData=self.data.CCI()
        elif type == 'ROC':
            oscData=self.data.ROC()
        elif type == 'RSI':
            oscData=self.data.RSI()
        elif type == 'williams':
            oscData=self.data.williams()
        elif type == 'TRIN':
            oscData=self.data.TRIN()
        elif type == 'mcClellan':
            oscData=self.data.mcClellan()
        elif type == 'adLine':
            oscData=self.data.adLine()
        else:            
            return
        if oscData!=None:
            x=range(len(self.data.close))        
            ax.plot(x,oscData,'g-',label=type)
            ax.set_xlim(x[0],x[-1])
            #legenda
            leg = ax.legend(loc='best', fancybox=True)
            leg.get_frame().set_alpha(0.5)
            self.formatDateAxis(self.oscPlot)
            self.fixOscLabels()
            self.fixTimeLabels()
    
    def fixOscLabels(self):
        """Metoda ustawia zakres osi poprawny dla danego oscylatora. Ponadto przenosi
        etykiety na prawą stronę, żeby nie nachodziły na kurs akcji"""
        ax=self.oscPlot
        type=self.oscType                
        if type == 'ROC':
            ax.set_ylim(-100, 100)
        elif type == 'RSI':
            ax.set_ylim(0, 100)
            ax.set_yticks([30,70])
        elif type == 'williams':
            ax.set_ylim(-100,0)        
        for tick in ax.yaxis.get_major_ticks():
            tick.label1On = False
            tick.label2On = True
            tick.label2.set_size(7)

    def formatDateAxis(self,ax):
        """Formatuje etykiety osi czasu."""
        chartWidth=int(self.fig.get_figwidth()*self.fig.get_dpi()*self.maxSize)        
        t = TextPath((0,0), '9999-99-99', size=7)
        labelWidth = int(t.get_extents().width)    
        num_ticks=chartWidth/labelWidth/2          
        length=len(self.data.date)
        if(length>num_ticks):
            step=length/num_ticks        
        else:
            step=1
        x=range(0,length,step)
        ax.xaxis.set_major_locator(FixedLocator(x))
        ticks=ax.get_xticks()        
        labels=[]        
        for i, label in enumerate(ax.get_xticklabels()):
            label.set_size(7)                       
            index=int(ticks[i])            
            if(index>=len(self.data.date)):
                labels.append('')
            else:
                labels.append(self.data.date[index].strftime("%Y-%m-%d"))            
            label.set_horizontalalignment('center')                                    
        ax.xaxis.set_major_formatter(FixedFormatter(labels))        
    
    def fixTimeLabels(self):
        """Włącza wyświetlanie etykiet osi czasu pod odpowiednim (tzn. najniższym)
        wykresem, a usuwa w pozostałych"""
        #oscylator jest zawsze na samym dole
        if self.oscPlot!=None and self.oscPlot.get_visible():
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(False)
            for label in self.volumeBars.get_xticklabels():
                label.set_visible(False)
            for label in self.oscPlot.get_xticklabels():
                label.set_visible(True)
        #jeśli nie ma oscylatora to pod wolumenem
        elif self.volumeBars!=None and self.volumeBars.get_visible():
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(False)
            for label in self.volumeBars.get_xticklabels():
                label.set_visible(True)         
        #a jak jest tylko duży wykres to pod nim
        else:
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(True)                        
    
    def fixPositions(self):
        """Dopasowuje wymiary i pozycje wykresów tak żeby zawsze wypełniały całą
        przestrzeń. Główny wykres puchnie albo się kurczy, a wolumen i oscylator 
        przesuwają się w górę lub dół."""
        #na początek wszystko spychamy na sam dół
        mainBounds=[self.margin, self.margin, self.maxSize, self.maxSize]
        volBounds=[self.margin, self.margin, self.maxSize, self.volHeight]
        oscBounds=[self.margin, self.margin, self.maxSize, self.oscHeight]
        #oscylator wypycha wolumen w górę i kurczy maina
        if self.oscPlot!=None and self.oscPlot.get_visible():
            mainBounds[1]+=self.oscHeight
            mainBounds[3]-=self.oscHeight
            volBounds[1]+=self.oscHeight
            self.oscPlot.set_position(oscBounds)
        #wolumen kolejny raz kurczy maina
        if self.volumeBars.get_visible():                    
            mainBounds[1]+=self.volHeight
            mainBounds[3]-=self.volHeight
            self.volumeBars.set_position(volBounds)
        self.mainPlot.set_position(mainBounds)     
    
    def setDrawingMode(self, mode):
        """Włączamy (True) lub wyłączamy (False) tryb rysowania po wykresie"""
        self.drawingMode=mode            
        x0, y0 = None,None
    
    def drawLine(self, x0,y0,x1,y1):
        """Dodaje linię (trend) do wykresu."""
        newLine=Line2D([x0,x1],[y0,y1],color='k')                
        self.mainPlot.add_line(newLine)
        self.additionalLines.append(newLine)
        newLine.figure.draw_artist(newLine)                                        
        self.blit(self.mainPlot.bbox)    #blit to taki redraw
    
    def clearLines(self):
        """Usuwa wszystkie linie narysowane dodatkowo na wykresie (tzn. nie kurs i nie wskaźniki)"""
        for line in self.additionalLines:            
            line.remove()
        self.additionalLines = []
        self.draw()
        self.blit(self.mainPlot.bbox)
    
    def drawRectangle(self, x, y, width, height, colour='blue', lwidth = 2.0, lstyle = 'dashed'):
        """Zaznacza prostokątem lukę/formację świecową czy coś tam jeszcze"""
        newRect=Rectangle((x,y),width,height,facecolor='none',edgecolor=colour,linewidth=lwidth,linestyle=lstyle)                
        self.mainPlot.add_patch(newRect)
        self.rectangles.append(newRect)
        newRect.figure.draw_artist(newRect)                                        
        self.blit(self.mainPlot.bbox)    #blit to taki redraw        
    
    def clearRectangles(self):
        """Usuwa prostokąty"""
        for rect in self.rectangles:            
            rect.remove()
        self.rectangles = []
        self.draw()
        self.blit(self.mainPlot.bbox)

    def onClick(self, event):
        """Rysujemy linię pomiędzy dwoma kolejnymi kliknięciami. Później to będzie 
        pewnie mniej biedne (z podglądem na żywo), ale pół dnia siedziałem żeby to
        gówno w ogóle zadziałało."""        
        if self.drawingMode==False:
            return
        if event.button==3: #nie no kurwa, RMB to tutaj button 3 -_-
            self.clearLines()            
        elif event.button==1:
            if self.x0==None or self.y0==None :
                self.x0, self.y0 = event.xdata, event.ydata
                self.firstPoint=True
            else:
                x1, y1 = event.xdata, event.ydata        
                self.drawLine(self.x0,self.y0,x1,y1)                
                self.x0, self.y0 = None,None
                
    def drawTrendLine(self, x0, y0, x1, y1, colour, lwidth = 3.0, lstyle = '--'):
          """Rysuje linie trendu opcja wyboru koloru i grubosci linii """
          newLine=Line2D([x0,x1],[y0,y1], linewidth = lwidth, linestyle=lstyle, color=colour)                
          self.mainPlot.add_line(newLine)
          self.additionalLines.append(newLine)
          newLine.figure.draw_artist(newLine)                                        
          self.blit(self.mainPlot.bbox)    #blit to taki redraw       
   
    def drawGeometricFormation(self):
        self.clearLines()
        formations=trend.findGeometricFormations(self.data.close)
        print formations
        for form in formations:
            if form!=None:
                self.drawTrendLine(form[1][0], form[1][1], form[1][2], form[1][3], 'r')
                self.drawTrendLine(form[2][0], form[2][1], form[2][2], form[2][3], 'r') 

    def drawRateLines(self):
		# Tutaj sobie testuje strategie bo nie wiedzialem gdzie to wrzucic :)
        a,b = osc.oscillatorStrategy(array(self.data.close),array(self.data.high),array(self.data.low),10)
        print a,b
        self.clearLines()
        print "Rysuje wachlarze."
        values = trend.rateLines(array(self.data.close),0.38,0.62)
        print values
        self.drawTrendLine(values[0][0],values[0][1],values[0][2],values[0][3],'y')
        self.drawTrendLine(values[1][0],values[1][1],values[1][2],values[1][3],'y')
        self.drawTrendLine(values[2][0],values[2][1],values[2][2],values[2][3],'y')           
          
    def drawCandleFormations(self):
        """Test formacji świecowych."""
        print "szukam formacji świecowych"
        self.clearRectangles()
        O=self.data.open
        H=self.data.high
        L=self.data.low
        C=self.data.close        
        formations=findCandleFormations(O,H,L,C)                
        for formation in formations:
            print formation                    
            x=formation[1]-0.5
            y=0.97*min(self.data.low[formation[1]],self.data.low[formation[2]])
            width=formation[2]-formation[1]+1
            height=1.06*(max((self.data.high[formation[1]],self.data.high[formation[2]]))
                        -min((self.data.low[formation[1]],self.data.low[formation[2]])))           
            self.drawRectangle(x,y,width,height)     
        self.drawTrend()   
            
    def drawGaps(self):
        """Test luk."""
        print "szukam luk"
        self.clearRectangles()
        H=self.data.high
        L=self.data.low
        C=self.data.close        
        gapsList=findGaps(H,L,C)       
        print gapsList
        if(gapsList!=[]):
            for gaps in gapsList:
                for gap in gaps[0]:            
                    print gap
                    x=gap[1]
                    width=1
                    if("rising" in gap[0]):
                        y=H[gap[1]]            
                        height=L[gap[1]+1]-H[gap[1]]
                    else:
                        y=H[gap[1]+1]            
                        height=L[gap[1]]-H[gap[1]+1]
                    self.drawRectangle(x,y,width,height)                
        
    def drawTrend(self):
        self.clearLines()
        strategy = Strategy(self.data.open, self.data.close, self.data.low, self.data.high, self.data.volume)
        strategy.analyze()
        a, b = trend.regression(self.data.close)
        trend.optimizedTrend(self.data.close)
        #self.drawTrendLine(0, b, len(self.data.close)-1, a*(len(self.data.close)-1) + b, 'y', 2.0)
        sup, res = trend.getChannelLines(self.data.close)
        self.drawTrendLine(sup[0][1], sup[0][0], sup[len(sup)-1][1], sup[len(sup)-1][0], 'g')
        self.drawTrendLine(res[0][1], res[0][0], res[len(res)-1][1], res[len(res)-1][0], 'r')
        neckLine = trend.lookForHeadAndShoulders(self.data.close, self.data.volume)
        if (neckLine[0] != neckLine[2]):
            self.drawTrendLine(neckLine[0], neckLine[1], neckLine[2], neckLine[3], 'm', 2.0, '-')
        
        trend.hornBottoms(self.data.close, self.data.volume)
        trend.hornTops(self.data.close, self.data.volume)
        neckline = trend.lookForTripleTop(self.data.close, self.data.volume)
        if (neckLine[0] != neckLine[2]):
            self.drawTrendLine(neckLine[0], neckLine[1], neckLine[2], neckLine[3], 'y', 2.0, '-')
        neckline = trend.lookForTripleBottom(self.data.close, self.data.volume)
        if (neckLine[0] != neckLine[2]):
            self.drawTrendLine(neckLine[0], neckLine[1], neckLine[2], neckLine[3], 'b', 2.0, '-')
        neckLine = trend.lookForReversedHeadAndShoulders(self.data.close, self.data.volume)
        if (neckLine[0] != neckLine[2]):
            self.drawTrendLine(neckLine[0], neckLine[1], neckLine[2], neckLine[3], 'c', 2.0, '-')
       # trend.lookForReversedHeadAndShoulders(self.data.close, self.data.volume)
        
     #   min, mindex = trend.findMinLine(asarray(self.data.close))
     #   self.drawTrendLine(mindex[0], min[0], mindex[len(min)-1], min[len(sup)-1], 'b', 1.0)
     #   max, mindex = trend.findMaxLine(asarray(self.data.close))
     #   self.drawTrendLine(mindex[0], max[0], mindex[len(min)-1], max[len(sup)-1], 'b', 1.0)
        if len(self.data.close) > 30:
            sup, res = trend.getChannelLines(self.data.close, 1, 2)
            self.drawTrendLine(sup[0][1], sup[0][0], sup[len(sup)-1][1], sup[len(sup)-1][0], 'g', 2.0)
            self.drawTrendLine(res[0][1], res[0][0], res[len(res)-1][1], res[len(res)-1][0], 'r', 2.0)
            
def getBoundsAsRect(axes):
    """Funkcja pomocnicza do pobrania wymiarów wykresu w formie prostokąta,
        tzn. tablicy."""
    bounds=axes.get_position().get_points()
    left=bounds[0][0]
    bottom=bounds[0][1]
    width=bounds[1][0]-left
    height=bounds[1][0]-bottom
    return [left, bottom, width, height]
