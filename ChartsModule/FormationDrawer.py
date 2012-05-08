import TechAnalysisModule.candles as candles
import TechAnalysisModule.trendAnalysis as trend


class FormationDrawer:
    """Klasa odpowiedzialna za rysowanie wybranych przez użytkownika formacji
    (przekazywanych w tablicy configuration) na wykresie."""
    
    def __init__(self, chart, strategy=None):
        """chart = obiekt klasy Chart. Domyślnie ustawiamy pustą listę formacji."""
        self.chart=chart
        setFormations(strategy)
    
    def setFormations(self, s):
        """Ustawiamy listę formacji, które będziemy rysować, poprzez przekazanie
        obiektu klasy Strategy. Narysowane zostaną formacje o niezerowej wartości"""                
        self.configuration={}
        if s==None:
            return
        if abs(s.trendVal)>0:
            self.configuration['trend']=(self.trendColor,self.trendLwidth,self.trendLstyle)
        if abs(s.headAndShouldersVal)>0:
            self.configuration['head_shoulders']=(self.headShouldersColor,self.headShouldersLwidth,self.headShouldersLstyle)
        if abs(s.tripleTopVal)>0:
            self.configuration['triple_top']=(self.tripleTopColor,self.tripleTopLwidth,self.tripleTopLstyle)        
        if abs(s.risingWedgeVal)>0:
            self.configuration['rising_wedge']=(self.risingWedgeColor,self.risingWedgeLwidth,self.risingWedgeLstyle)        
        if abs(s.fallingTriangleVal)>0:
            self.configuration['falling_triangle']=(self.fallingTriangleColor,self.fallingTriangleLwidth,self.fallingTriangleLstyle)        
        if abs(s.reversedHeadAndShouldersVal)>0:
            self.configuration['reversed_head_shoulders']=(self.reversedHeadShouldersColor,self.reversedHeadShouldersLwidth,self.reversedHeadShouldersLstyle)        
        if abs(s.tripleBottomVal)>0:
            self.configuration['triple_bottom']=(self.tripleBottomColor,self.tripleBottomLwidth,self.tripleBottomLstyle)        
        if abs(s.fallingWedgeVal)>0:
            self.configuration['falling_wedge']=(self.fallingWedgeColor,self.fallingWedgeLwidth,self.fallingWedgeLstyle)                        
        if abs(s.risingTriangleVal)>0:
            self.configuration['rising_triangle']=(self.risingTriangleColor,self.risingTriangleLwidth,self.risingTriangleLstyle)                                                                                          
        if abs(s.symetricTriangleVal)>0:
            self.configuration['symmetric_triangle']=(self.symetricTriangleColor,self.symetricTriangleLwidth,self.symetricTriangleLstyle)                                                                                          
        if abs(s.risingBreakawayGapVal)>0:
            self.configuration['rising_breakaway_gap']=(self.risingBreakawayGapColor,self.risingBreakawayGapLwidth,self.risingBreakawayGapLstyle)                                                                                          
        if abs(s.risingContinuationGapVal)>0:
            self.configuration['rising_continuation_gap']=(self.risingContinuationGapColor,self.risingContinuationGapLwidth,self.risingContinuationGapLstyle)                                                                                          
        if abs(s.risingExhaustionGapVal)>0:
            self.configuration['rising_exhaustion_gap']=(self.risingExhaustionGapColor,self.risingExhaustionGapLwidth,self.risingExhaustionGapLstyle)                                                                                          
        if abs(s.fallingBreakawayGapVal)>0:
            self.configuration['falling_breakaway_gap']=(self.fallingBreakawayGapColor,self.fallingBreakawayGapLwidth,self.fallingBreakawayGapLstyle)                                                                                                  
        if abs(s.fallingContinuationGapVal)>0:
            self.configuration['falling_breakaway_gap']=(self.fallingContinuationGapColor,self.fallingContinuationGapLwidth,self.fallingContinuationGapLstyle)                                                                                          
        if abs(s.fallingExhaustionGapVal)>0:
            self.configuration['falling_continuation_gap']=(self.fallingExhaustionGapColor,self.fallingExhaustionGapLwidth,self.fallingExhaustionGapLstyle)                                                                                          
        if abs(s.bull3Val)>0:
            self.configuration['bull3']=(self.bull3Color,self.bull3Lwidth,self.bull3Lstyle)                                                                                                      
        if abs(s.bear3Val)>0:
            self.configuration['bear3']=(self.bear3Color,self.bear3Lwidth,self.bear3Lstyle)                                                                                          
        if abs(s.mornigStarVal)>0:
            self.configuration['morning_star']=(self.mornigStarColor,self.mornigStarLwidth,self.mornigStarLstyle)                                                                                          
        if abs(s.eveningStarVal)>0:
            self.configuration['evening_star']=(self.eveningStarColor,self.eveningStarLwidth,self.eveningStarLstyle)                                                                                                  
        if abs(s.darkCloudVal)>0:
            self.configuration['dark_cloud']=(self.darkCloudColor,self.darkCloudLwidth,self.darkCloudLstyle)                                                                                          
        if abs(s.piercingVal)>0:
            self.configuration['piercing']=(self.piercingColor,self.piercingLwidth,self.piercingLstyle) 
        #flag & penant nie mają w strategy wartości!
                

    def drawFormations(self):
        """Rysujemy formacje, które są zdefiniowane w strategy."""
        if self.strategy==None:
            return
        data=self.chart.getData()        
        geoForm=['rect', 'symmetric_triangle', 'rising_triangle', 'falling_triangle',
                'rising_wedge', 'falling_wedge'] 
        foundGeo=trend.findGeometricFormations(data.close)
        candleForm=['bull3','bear3','morning_star','evening_star','piercing','dark_cloud']        
        gaps=['rising_breakaway_gap','rising_continuation_gap','rising_exhaustion_gap',
              'falling_breakaway_gap','falling_continuation_gap','falling_exhaustion_gap']        
        fandp=['risingTrendFlagOrPennant','fallingTrendFlagOrPennant']                                
        self.chart.clearLines()
        self.chart.clearRectangles()
        for name, values in self.configuration.iteritems():            
            if name in geoForm:
                if not computedGeo:
                    foundGeo=trend.findGeometricFormations(data.close)
                    computedGeo=True
                for formation in computedGeo:
                    if name==formation[0]:
                        self.drawGeometricFormation(formation,values[0],values[1],values[2])
            elif name in candleForm:
                if not computedCandle:
                    foundCandle=candles.findCandleFormations(data.open, data.high, data.low, data.close)
                    computedCandle=True
                for formation in computedCandle:
                    if name==formation[0]:
                        self.drawCandleFormation(formation,values[0],values[1],values[2])
            elif name in gaps:
                if not computedGaps:
                    foundGaps=candles.findGaps(data.high, data.low, data.close)
                    computedGaps=True
                for gapsList in foundGaps:
                    for gap in gapsList:
                        if name==gap[0]:
                            self.drawGap(gap,values[0],values[1],values[2])
            elif name in fandp:
                if not computedFandp:
                    #foundFandp=trend.findFlagsAndPennants(data.close, data.volume)
                    #tak to się wywołuje?
                    computedFandp=True
                if name == foundFandp[0]:
                    self.drawFlagAndPennant(foundFanp,values[0],values[1],values[2])                
            elif name=='trend':
                self.drawTrend(values[0],values[1],values[2])
            elif name=='rate_lines':
                self.drawRateLines(values[0],values[1],values[2])        
            elif name=='head_shoulders':
                self.drawHeadAndShoulders(values[0],values[1],values[2])
    
    def drawGeometricFormation(self,form,color,lstyle,lwidth):        
        self.chart.drawLine(form[1][0], form[1][1], form[1][2], form[1][3], 
                            color, lwidth, lstyle)
        self.chart.drawLine(form[2][0], form[2][1], form[2][2], form[2][3], 
                            color, lwidth, lstyle)

    def drawCandleFormation(self,formation,color,lstyle,lwidth):                                
        x=formation[1]-0.5
        y=0.97*min(self.data.low[formation[1]],self.data.low[formation[2]])
        width=formation[2]-formation[1]+1
        height=1.06*(max((self.data.high[formation[1]],self.data.high[formation[2]]))
                    -min((self.data.low[formation[1]],self.data.low[formation[2]])))           
        self.chart.drawRectangle(x,y,width,height,color,lwidth,lstyle)     
        
    
    def drawGap(self,gap,color,lstyle,lwidth):        
        x=gap[1]
        width=1
        data=self.chart.getData()
        if("rising" in gap[0]):
            y=data.high[gap[1]]            
            height=data.low[gap[1]+1]-data.high[gap[1]]
        else:
            y=data.high[gap[1]+1]            
            height=data.low[gap[1]]-data.high[gap[1]+1]
        self.chart.drawRectangle(x,y,width,height,color,lwidth,lstyle)
    
    def drawHeadAndShoulders(self,formation,color,lstyle,lwidth):
        #uzupełnić
        pass
    
    def drawFlagAndPennant(self,formation,color,lstyle,lwidth):
        #uzupełnić
        pass

    def drawTrend(self,color,lstyle,lwidth):
        #uzupełnić
        pass
    
    def drawRateLines(self,color,lstyle,lwidth):        
        values = trend.rateLines(array(self.chart.getData().close),0.38,0.62)
        print values
        self.drawLine(values[0][0],values[0][1],values[0][2],values[0][3],'y')
        self.drawLine(values[1][0],values[1][1],values[1][2],values[1][3],'y')
        self.drawLine(values[2][0],values[2][1],values[2][2],values[2][3],'y')           