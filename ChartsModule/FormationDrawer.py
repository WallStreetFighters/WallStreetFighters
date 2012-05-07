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
        (nazwa,kolor,linewidth) Rozpoznawane nazwy są takie jak te w wartościach
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
        pass

    def drawCandleFormation(self,formation):
        pass
    
    def drawGap(self,gap):
        pass
    
    def drawHeadAndShoulders(self,formation):
        pass
    
    def drawFlagAndPennant(self,formation):
        #uzupełnić
        pass

    def drawTrend(self):
        pass