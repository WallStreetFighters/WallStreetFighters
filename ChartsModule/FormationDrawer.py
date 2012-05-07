import TechAnalysisModule.candles as candles
import TechAnalysisModule.trendAnalysis as trend


class FormationDrawer:
    """Klasa odpowiedzialna za rysowanie wybranych przez użytkownika formacji
    (przekazywanych w tablicy configuration) na wykresie."""
    
    def __init__(self, chart):
        """chart = obiekt klasy Chart. Domyślnie ustawiamy pustą listę formacji."""
        self.chart=chart
        self.configuration=[]
    
    def setConfiguration(config):
        """Ustawiamy listę formacji, które będziemy rysować. config jest tablicą krotek postaci
        (nazwa,kolor,linestyle,linewidth) Rozpoznawane nazwy są takie jak te w wartościach
        zwracanych przez funkcje znajdujące formacje, oraz 'trend' """
        self.configuration=config

    def drawFormations(self):
        """Rysujemy formacje, które są zdefiniowane w tablicy configuration."""
        geoForm=['rect', 'symmetric_triangle', 'rising_triangle', 'falling_triangle',
                'rising_wedge', 'falling_wedge'] 
        candleForm=['bull3','bear3','morning_star','evening_star','piercing','dark_cloud']
        gaps=['rising_breakaway_gap','rising_continuation_gap','rising_exhaustion_gap',
              'falling_breakaway_gap','falling_continuation_gap','falling_exhaustion_gap']
        fandp=['risingTrendFlagOrPennant','fallingTrendFlagOrPennant']                      
        computedGeo=False
        computedCandle=False
        computedGaps=False
        computedFandp=False
        data=self.chart.getData()
        self.chart.clearLines()
        self.chart.clearRectangles()
        for entry in self.configuration:
            name=entry[0]
            if name in geoForm:
                if not computedGeo:
                    foundGeo=trend.findGeometricFormations(data.close)
                    computedGeo=True
                for formation in computedGeo:
                    if name==formation[0]:
                        self.drawGeometricFormation(formation)
            elif name in candleForm:
                if not computedCandle:
                    foundCandle=candles.findCandleFormations(data.open, data.high, data.low, data.close)
                    computedCandle=True
                for formation in computedCandle:
                    if name==formation[0]:
                        self.drawCandleFormation(formation)
            elif name in gaps:
                if not computedGaps:
                    foundGaps=candles.findGaps(data.high, data.low, data.close)
                    computedGaps=True
                for gapsList in foundGaps:
                    for gap in gapsList:
                        if name==gap[0]:
                            self.drawGap(gap)
            elif name in fandp:
                if not computedFandp:
                    #foundFandp=trend.findFlagsAndPennants(data.close, data.volume)
                    #tak to się wywołuje?
                    computedFandp=True
                if name == foundFandp[0]:
                    self.drawFlagAndPennant(foundFanp)                
            elif name=='trend':
                self.drawTrend()
            elif name=='rate_lines':
                self.drawRateLines()        
            elif name=='head_shoulders':
                self.drawHeadAndShoulders()
    
    def drawGeometricFormation(self,formation):
        for entry in settings:
            if entry[0]==formation[0]:
                color=entry[1]
                lstyle=entry[2]
                lwidth=entry[2]
                break
        self.chart.drawLine(form[1][0], form[1][1], form[1][2], form[1][3], 
                            color, lwidth, lstyle)
        self.chart.drawLine(form[2][0], form[2][1], form[2][2], form[2][3], 
                            color, lwidth, lstyle)

    def drawCandleFormation(self,formation):                        
        for entry in settings:
            if entry[0]==formation[0]:
                color=entry[1]
                lstyle=entry[2]
                lwidth=entry[2]
                break
        x=formation[1]-0.5
        y=0.97*min(self.data.low[formation[1]],self.data.low[formation[2]])
        width=formation[2]-formation[1]+1
        height=1.06*(max((self.data.high[formation[1]],self.data.high[formation[2]]))
                    -min((self.data.low[formation[1]],self.data.low[formation[2]])))           
        self.chart.drawRectangle(x,y,width,height,color,lwidth,lstyle)     
        
    
    def drawGap(self,gap):
        for entry in settings:
            if entry[0]==gap[0]:
                color=entry[1]
                lstyle=entry[2]
                lwidth=entry[2]
                break
        x=gap[1]
        width=1
        data=self.chart.getData()
        if("rising" in gap[0]):
            y=data.high[gap[1]]            
            height=data.low[gap[1]+1]-data.high[gap[1]]
        else:
            y=data.high[gap[1]+1]            
            height=data.low[gap[1]]-data.high[gap[1]+1]
        self.chart.drawRectangle(x,y,width,height)
    
    def drawHeadAndShoulders(self,formation):
        #uzupełnić
        pass
    
    def drawFlagAndPennant(self,formation):
        #uzupełnić
        pass

    def drawTrend(self):
        #uzupełnić
        pass
    
    def drawRateLines(self):        
        values = trend.rateLines(array(self.chart.getData().close),0.38,0.62)
        print values
        self.drawLine(values[0][0],values[0][1],values[0][2],values[0][3],'y')
        self.drawLine(values[1][0],values[1][1],values[1][2],values[1][3],'y')
        self.drawLine(values[2][0],values[2][1],values[2][2],values[2][3],'y')           