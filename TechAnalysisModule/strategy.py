import candles as candles
import trendAnalysis as trend
import oscilators as oscilators
from numpy import * 

class Strategy:
    positiveSignal = 50
    negativeSignal = -50
    trendVal = 100
    
    defPositiveSignal = 50
    defNegativeSignal = -50
    defTrendVal = 100

    """Formacje"""
    #Odwrocenie trendu wzrostowego
    headAndShouldersVal = -100
    tripleTopVal = -100
    risingWedgeVal = -80
    fallingTriangleVal = -80
    
    defHeadAndShouldersVal = -100
    defTripleTopVal = -100
    defRisingWedgeVal = -80
    defFallingTriangleVal = -80

    #Odwrocenie trendu spadkowego
    reversedHeadAndShouldersVal = 100
    tripleBottomVal = 100
    fallingWedgeVal = 80
    risingTriangleVal = 80
    
    defReversedHeadAndShouldersVal = 100
    defTripleBottomVal = 100
    defFallingWedgeVal = 80
    defRisingTriangleVal = 80

    #Kontynuacja trendu
    symetricTriangleVal = 50
    rectangleVal = 30

    defFlagPennantVal = 20
    
    defSymetricTriangleVal = 50
    defRectangleVal = 30
    """Wskazniki i oscylatory"""
    oscilatorsVal = 50
    newHighNewLowVal = 50
    bollignerVal = 50
    momentumVal = 50
    rocVal = 50
    cciVal = 50
    rsiVal = 50
    williamsVal = 50
    
    defOscilatorsVal = 50
    defNewHighNewLowVal = 50
    defBollignerVal = 50
    defMomentumVal = 50
    defRocVal = 50
    defCciVal = 50
    defRsiVal = 50
    defWilliamsVal = 50

    """Luki"""
    #Wzrostowe
    risingBreakawayGapVal = 50
    risingContinuationGapVal = 30
    fallingExhaustionGapVal = 10 
    
    defRisingBreakawayGapVal = 50
    defRisingContinuationGapVal = 30
    defFallingExhaustionGapVal = 10 

    #Spadkowe
    fallingBreakawayGapVal = -50
    risingExhaustionGapVal = -50
    fallingContinuationGapVal = -30
    
    defFallingBreakawayGapVal = -50
    defRisingExhaustionGapVal = -50
    defFallingContinuationGapVal = -30

    """Formacje swiecowe"""
    #sygnal kupna
    bull3Val = 15
    mornigStarVal = 10
    piercingVal = 5
    
    defBull3Val = 15
    defMornigStarVal = 10
    defPiercingVal = 5
    #sygnal sprzedazy
    bear3Val = -15
    eveningStarVal = -10
    darkCloudVal = -5
    
    defBear3Val = -15
    defEveningStarVal = -10
    defDarkCloudVal = -5
    open = []
    close = []
    low = []
    high = []
    volume = []
    def __init__(self, open, close, low, high, volume):
        self.setData(open, close, low, high, volume)
    
    def setData(self, open, close, low, high, volume):
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.volume = volume
        
    def resetCoefficients(self):
        positiveSignal = defPositiveSignal  
        negativeSignal = defNegativeSignal
        trendVal = defTrendVal
        headAndShouldersVal = defHeadAndShouldersVal
        tripleTopVal = defTripleTopVal
        risingWedgeVal = defRisingWedgeVal
        fallingTriangleVal = defFallingTriangleVal
        reversedHeadAndShouldersVal = defReversedHeadAndShouldersVal
        tripleBottomVal = defTripleBottomVal
        fallingWedgeVal = defFallingWedgeVal
        risingTriangleVal = defRisingTriangleVal
        symetricTriangleVal = defSymetricTriangleVal
        rectangleVal = defRectangleVal
        oscilatorsVal = defOscilatorsVal
        newHighNewLowVal = defNewHighNewLowVal
        bollignerVal = defBollignerVal
        momentumVal = defMomentumVal
        rocVal = defRocVal
        cciVal = defCciVal
        rsiVal = defRsiVal
        williamsVal = defWilliamsVal
        risingBreakawayGapVal = defRisingBreakawayGapVal
        risingContinuationGapVal = defRisingContinuationGapVal
        fallingExhaustionGapVal = defFallingExhaustionGapVal 
        fallingBreakawayGapVal = -50
        risingExhaustionGapVal = -50
        fallingContinuationGapVal = -30
        defFallingBreakawayGapVal = -50
        defRisingExhaustionGapVal = -50
        defFallingContinuationGapVal = -30
        bull3Val = defBull3Val
        mornigStarVal = defMornigStarVal
        piercingVal = defPiercingVal
        bear3Val = defBear3Val
        eveningStarVal = defEveningStarVal
        darkCloudVal = defDarkCloudVal
            
    def analyze(self):
          resultText = ''
          overallScore = 0
          print "Program will now analyze trend, selected chart patterns, candle patterns, indicators, oscilators and gaps\n"
          resultText = resultText + "Program will now analyze trend, selected chart patterns, candle patterns, indicators, oscilators and gaps\n"
          print "(+) -> positive\n (0) -> neutral\n (-) -> negative signal\n"
          resultText = resultText + "(+) -> positive\n (0) -> neutral\n (-) -> negative signal\n"
          overallScore += self.trendVal * trend.optimizedTrend(self.close)
          if overallScore > 0:
              print " (+) long-term trend is rising\n"
              resultText = resultText + " (+) long-term trend is rising\n"
          elif overallScore < 0:
              print " (-) long-term trend is falling\n"
              resultText = resultText + " (-) long-term trend is falling\n"
          else:
              print " (0) long-term trend is neutral\n"
              resultText = resultText + " (0) long-term trend is neutral\n"

          print "Program has identified following chart patterns:\n"
          resultText = resultText + "Program has identified following chart patterns:\n"
          form = trend.lookForHeadAndShoulders(self.close, self.volume, 1)
          overallScore += form * self.headAndShouldersVal
          if form * self.headAndShouldersVal != 0:
              print " (-) head and shoulders\n"
              resultText = resultText + " (-) head and shoulders\n"

          form = trend.lookForReversedHeadAndShoulders(self.close, self.volume, 1)
          overallScore += form * self.reversedHeadAndShouldersVal
          if form * self.reversedHeadAndShouldersVal != 0:
              print " (+) reversed head and shoulders\n"
              resultText = resultText + " (+) reversed head and shoulders\n"

          form = trend.lookForTripleTop(self.close, self.volume, 1)
          overallScore += form * self.tripleTopVal
          if form * self.tripleTopVal != 0:
              print " (-) triple top\n"
              resultText = resultText + " (-) triple top\n"

          form = trend.lookForTripleBottom(self.close, self.volume, 1)
          overallScore += form * self.tripleBottomVal
          if form * self.tripleBottomVal != 0:
              print " (+) triple bottom\n"
              resultText = resultText + " (+) triple bottom\n"

          geometricFormations = trend.findGeometricFormations(self.close)
          for formation in geometricFormations:
              if formation != None:
                  if formation[0] == 'rect':
                      overallScore += self.rectangleVal * formation[3]
                      if self.rectangleVal * formation[3] > 0:
                          print " (+)  rising rectangle\n"
                          resultText = resultText + " (+)  rising rectangle\n"
                      elif self.rectangleVal * formation[3] < 0:
                          print " (-) falling rectangle\n"
                          resultText = resultText + " (-) falling rectangle\n"
                  elif formation[0] == 'symmetric_triangle':
                      overallScore += self.symetricTriangleVal * formation[3]
                      if self.symetricTriangleVal * formation[3] > 0:
                          print " (+) symmetric triangle - continuation of rising trend\n"
                          resultText = resultText + " (+) symmetric triangle - continuation of rising trend\n"
                      elif self.symetricTriangleVal * formation[3] < 0:
                          print " (-) symmetric triangle - continuation of falling trend\n"
                          resultText = resultText + " (-) symmetric triangle - continuation of falling trend\n"
                  elif formation[0] == 'falling_triangle':
                      overallScore += self.fallingTriangleVal * formation[3]
                      if self.fallingTriangleVal * formation[3] != 0:
                          print " (-) falling triangle\n"
                          resultText = resultText + " (-) falling triangle\n"
                  elif formation[0] == 'rising_triangle':
                      overallScore += self.risingTriangleVal * formation[3]
                      if self.risingTriangleVal * formation[3] != 0:
                          print " (+) rising triangle\n"
                          resultText = resultText + " (+) rising triangle\n"
                  elif formation[0] == 'rising_wedge':
                      overallScore += self.risingWedgeVal * formation[3]
                      if self.risingWedgeVal * formation[3] != 0:
                          print " (-) rising wedge\n"
                          resultText = resultText + " (-) rising wedge\n"
                  elif formation[0] == 'falling_wedge':
                      overallScore += self.fallingWedgeVal * formation[3]
                      if self.fallingWedgeVal * formation[3] != 0:
                          print " (+) falling wedge\n"
                          resultText = resultText + " (+) falling wedge\n"
     
	  flags = trend.findFlagsAndPennants(self.close,self.volume, self.high, self.low)
	  if flags != None:
		overallScore += defFlagPennantVal * flags[1]
		if flags[1] < 0:
			print "(-) falling-trend flag/pennant"
			resultText = resultText + "(-) falling-trend flag/pennant"
		else:
			print "(+) rising-trend flag/pennant"
			resultText = resultText + "(+) rising-trend flag/pennant"

          # gaps = candles.findGaps(self.high,self.low,self.close) 
          # for formation in gaps:
          #     if formation != None:
          #         print "luka ", formation
          #         print "luka2 ", formation[0]
          #         print "luka3 ", formation[0][0]
          #         
          #         if formation[0][0] == 'rising_breakaway_gap':
          #             overallScore += self.risingBreakawayGapVal * formation[1]
          #             if self.risingBreakawayGapVal * formation[1] != 0:
          #                 print " (+) rising breakaway gap\n"
          #         elif formation[0][0] == 'rising_continuation_gap':
          #             overallScore += self.risingContinuationGapVal * formation[1]
          #             if self.risingContinuationGapVal * formation[1] != 0:
          #                 print " (+) rising continuation gap\n"
          #         elif formation[0][0] == 'rising_exhaustion_gap':
          #             overallScore += self.risingExhaustionGapVal * formation[1]
          #             if self.risingExhaustionGapVal * formation[1] != 0:
          #                 print " (-) rising exhaoustion gap\n"
          #         elif formation[0][0] == 'falling_breakaway_gap':
          #             overallScore += self.fallingBreakawayGapVal * formation[1]
          #             if self.fallingBreakawayGapVal * formation[1] != 0:
          #                 print " (-) falling breakaway gap\n"
          #         elif formation[0][0] == 'falling_continuation_gap':
          #             overallScore += self.fallingContinuationGapVal * formation[1]
          #             if self.fallingContinuationGapVal * formation[1] != 0:
          #                 print " (-) falling contination gap\n"
          #         elif formation[0][0] == 'falling_exhaustion_gap':
          #             overallScore += self.fallingExhaustionGapVal * formation[1]
          #             if self.fallingExhaustionGapVal * formation[1] != 0:
          #                 print " (+) falling exhaustion gap\n"

          candleFormations = candles.findCandleFormations(self.open, self.high, self.low, self.close)
          for formation in candleFormations:
              if formation != None:
                  if formation[0][0] == 'bull3':
                      overallScore +=  bull3Val * formation[3]
                      if bull3Val * formation[3] != 0:
                          print " (+) triple bull candle pattern\n"
                          resultText = resultText + " (+) triple bull candle pattern\n"
                  elif formation[0][0] == 'morning_star':
                      overallScore += self.morningStarVal * formation[3]
                      if self.morningStarVal * formation[3] != 0:
                          print " (+) morning star candle pattern\n"
                          resultText = resultText + " (+) morning star candle pattern\n"
                  elif formation[0][0] == 'piercing':
                      overallScore += self.piercingVal * formation[3]
                      if self.piercingVal * formation[3] != 0:
                          print " (+) piercing candle pattern\n"
                          resultText = resultText + " (+) piercing candle pattern\n"
                  elif formation[0][0] == 'bear3':
                      overallScore += self.bear3Val * formation[3]
                      if bear3Val * formation[3] != 0:
                          print " (-) triple bear candle pattern\n"
                          resultText = resultText + " (-) triple bear candle pattern\n"
                  elif formation[0][0] == 'evening_star':
                      overallScore += self.eveningStarVal * formation[3]
                      if self.eveningStarVal * formation[3] != 0:
                          print " (-) evening star candle pattern\n"
                          resultText = resultText + " (-) evening star candle pattern\n"
                  elif formation[0][0] == 'dark_cloud':
                      overallScore += self.darkCloudVal * formation[3]
                      if self.darkCloudVal * formation[3] != 0:
                          print " (-) dark cloud candle pattern\n"
                          resultText = resultText + " (-) dark cloud candle pattern\n"

                          
          # score, oscilatorsAndIndicators = oscilators.oscillatorStrategy(array(self.close), array(self.high), array(self.low), min(10, len(self.close)))
          #           overallScore += self.newHighNewLowVal * oscilatorsAndIndicators[0]
          #           if self.newHighNewLowVal * oscilatorsAndIndicators[0] > 0:
          #               print " (+) new high - new low index\n"
          #           elif self.newHighNewLowVal * oscilatorsAndIndicators[0] < 0:
          #               print " (-) new high - new low index\n"
          # 
          #           overallScore += self.bollignerVal * oscilatorsAndIndicators[1]
          #           if self.bollignerVal * oscilatorsAndIndicators > 0:
          #               print " (+) bolligner bounds\n"
          #           elif self.bollignerVal * oscilatorsAndIndicators < 0:
          #               print " (-) bolligner bounds\n"
          # 
          #           overallScore += self.momentumVal * oscilatorsAndIndicators[2]
          #           if self.momentumVal * oscilatorsAndIndicators > 0:
          #               print " (+) momentum oscilator\n"
          #           elif self.momentumVal * oscilatorsAndIndicators < 0:
          #               print " (-) momentum oscilator\n"
          # 
          #           overallScore += self.rocVal * oscilatorsAndIndicators[3]
          #           if self.rocVal * oscilatorsAndIndicators[3] > 0:
          #               print " (+) roc oscilator\n"
          #           elif self.rocVal * oscilatorsAndIndicators[3] < 0:
          #               print " (-) roc oscilator\n"
          # 
          #           overallScore += self.cciVal * oscilatorsAndIndicators[4]
          #           if self.cciVal * oscilatorsAndIndicators[4] > 0:
          #               print " (+) cci oscilator\n"
          #           elif self.cciVal * oscilatorsAndIndicators[4] < 0:
          #               print " (-) cci oscilator\n"
          # 
          #           overallScore += self.rsiVal * oscilatorsAndIndicators[5]
          #           if self.rsiVal * oscilatorsAndIndicators[5] > 0:
          #               print " (+) rsi oscilator\n"
          #           elif self.rsiVal * oscilatorsAndIndicators[5] < 0:
          #               print " (-) rsi oscilator\n"
          # 
          #           overallScore += self.williamsVal * oscilatorsAndIndicators[6]
          #           if self.williamsVal * oscilatorsAndIndicators[6] > 0:
          #               print " (+) williams oscilator\n"
          #           elif self.williamsVal * oscilatorsAndIndicators[6] < 0:
          #               print " (-) williams oscilator\n"
          print "\n Overall score: ",overallScore, "\n"
          resultText = resultText + "\n Overall score: "+str(overallScore)+ "\n"
          if  overallScore > self.positiveSignal:
              print " technical analysis generated positive signal, however fundamental analysis should be also considered\n"
              resultText = resultText + " technical analysis generated positive signal, however fundamental analysis should be also considered\n"
          elif overallScore < self.negativeSignal:
              print " technical analysis generated negative signal, if you own actives it is recommended to sell, however fundamental analysis should be also considered\n"
              resultText = resultText + " technical analysis generated negative signal, if you own actives it is recommended to sell, however fundamental analysis should be also considered\n"
          else:
              print " technical analysis generated neutral signal\n"
              resultText = resultText + " technical analysis generated neutral signal\n"
          print "\n Remember that authors of this software DO NOT TAKE ANY RESPONSIBILITY for possible financial loss\n"
          resultText = resultText + "\n Remember that authors of this software DO NOT TAKE ANY RESPONSIBILITY for possible financial loss\n"
          return resultText