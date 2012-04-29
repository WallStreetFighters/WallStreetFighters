import TechAnalysisModule.candles as candles
import TechAnalysisModule.trendAnalysis as trend
import TechAnalysisModule.oscilators as oscilators

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
    #sygnał kupna
    bull3Val = 15
    mornigStarVal = 10
    piercingVal = 5
    defBull3Val = 15
    defMornigStarVal = 10
    defPiercingVal = 5
    #sygnał sprzedaży
    bear3Val = -15
    eveningStarVal = -10
    darkCloudVal = -5
    defBear3Val = -15
    defEveningStarVal = -10
    defDarkCloudVal = -5
    opening, closing, lowest, highest, volumine
    def __init__(self, opening, closing, lowest, highest, volumine):
        self.setData(self, opening, closing, lowest, highest, volumine)
    
    def setData(self, opening, closing, lowest, highest, volumine):
        self.opening = opening
        self.closing = closing
        self.lowest = lowest
        self.highest = highest
        self.volumine = volumine
        
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
          overallScore += 0
          print "Program will now analyze trend, selected chart patterns, candle patterns, indicators, oscilators and gaps\n"
          print "(+) -> positive (0) -> neutral (-) -> negative signal"
          overallScore += trendVal * trend.optimizedTrend(self.closing)
          if overallScore > 0:
              print " (+) long-term trend is rising\n"
          elif overallScore < 0:
              print " (-) long-term trend is falling\n"
          else
              print " (0) long-term trend is neutral\n"

          print "Program has identified following chart patterns:\n"
          form = trend.lookForHeadAndShoulders(self.closing, self.volume, 0)
          overallScore += form * headAndShouldersVal
          if form * headAndShouldersVal != 0:
              print " (-) head and shoulders\n"

          form = trend.lookForReversedHeadAndShoulders(self.closing, self.volume, 0)
          overallScore += form * reversedHeadAndShouldersVal
          if form * reversedHeadAndShouldersVal != 0:
              print " (+) reversed head and shoulders\n"

          form = trend.lookForTripleTop(self.closing, self.volume, 0)
          overallScore += form * tripleTopVal
          if form * tripleTopVal != 0:
              print " (-) triple top\n"

          form = trend.lookForTripleBottom(self.closing, a, 0)
          overallScore += form * tripleBottomVal
          if form * tripleBottomVal != 0:
              print " (+) triple bottom\n"

          geometricFormations = trend.findGeometricFormations(self.closing)
          for formation in geometricFormations:
              if formation != None:
                  if formation[0] == 'rect':
                      overallScore += rectangleVal * formation[3]
                      if rectangleVal * formation[3] > 0:
                          print " (+)  rising rectangle\n"
                      elif rectangleVal * formation[3] < 0:
                          print " (-) falling rectangle\n"
                  elif formation[0] == 'symmetric_triangle':
                      overallScore += symetricTriangleVal * formation[3]
                      if symetricTriangleVal * formation[3] > 0:
                          print " (+) symmetric triangle - continuation of rising trend\n"
                      elif symetricTriangleVal * formation[3] < 0:
                          print " (-) symmetric triangle - continuation of falling trend\n"
                  elif formation[0] == 'falling_triangle':
                      overallScore += fallingTriangleVal * formation[3]
                      if fallingTriangleVal * formation[3] != 0:
                          print " (-) falling triangle\n"
                  elif formation[0] == 'rising_triangle':
                      overallScore += risingTriangleVal * formation[3]
                      if risingTriangleVal * formation[3] != 0:
                          print " (+) rising triangle\n"
                  elif formation[0] == 'rising_wedge':
                      overallScore += risingWedgeVal * formation[3]
                      if risingWedgeVal * formation[3] != 0:
                          print " (-) rising wedge\n"
                  elif formation[0] == 'falling_wedge':
                      overallScore += fallingWedgeVal * formation[3]
                      if fallingWedgeVal * formation[3] != 0:
                          print " (+) falling wedge\n"

          gaps = trend.findGaps(self.highest,self.lowest,self.closing) 
          for formation in gaps:
              if formation != None:
                  if formation[0] == 'rising_breakaway_gap':
                      overallScore += risingBreakawayGapVal * formation[2]
                      if risingBreakawayGapVal * formation[2] != 0:
                          print " (+) rising breakaway gap\n"
                  elif formation[0] = 'rising_continuation_gap':
                      overallScore += risingContinuationGapVal * formation[2]
                      if risingContinuationGapVal * formation[2] != 0:
                          print " (+) rising continuation gap\n"
                  elif formation[0] = 'rising_exhaustion_gap':
                      overallScore += risingExhaustionGapVal * formation[2]
                      if risingExhaustionGapVal * formation[2] != 0:
                          print " (-) rising exhaoustion gap\n"
                  elif formation[0] == 'falling_breakaway_gap':
                      overallScore += fallingBreakawayGapVal * formation[2]
                      if fallingBreakawayGapVal * formation[2] != 0:
                          print " (-) falling breakaway gap\n"
                  elif formation[0] = 'falling_continuation_gap':
                      overallScore += fallingContinuationGapVal * formation[2]
                      if fallingContinuationGapVal * formation[2] != 0:
                          print " (-) falling contination gap\n"
                  elif formation[0] = 'falling_exhaustion_gap':
                      overallScore += fallingExhaustionGapVal * formation[2]
                      if fallingExhaustionGapVal * formation[2] != 0:
                          print " (+) falling exhaustion gap\n"

          candleFormations = candles.findCandleFormations(self.opening, self.highest, self.lowest, self.closing)
          for formation in candleFormations:
              if formation != None:
                  if formation[0] == 'bull3':
                      overallScore +=  bull3Val * formation[3]
                      if bull3Val * formation[3] != 0:
                          print " (+) triple bull candle pattern\n"
                  elif formation[0] == 'morning_star':
                      overallScore += morningStarVal * formation[3]
                      if morningStarVal * formation[3] != 0:
                          print " (+) morning star candle pattern\n"
                  elif formation[0] == 'piercing':
                      overallScore += piercingVal * formation[3]
                      if piercingVal * formation[3] != 0:
                          print " (+) piercing candle pattern\n"
                  elif formation[0] == 'bear3':
                      overallScore += bear3Val * formation[3]
                      if bear3Val * formation[3] != 0:
                          print " (-) triple bear candle pattern\n"
                  elif formation[0] == 'evening_star':
                      overallScore += eveningStarVal * formation[3]
                      if eveningStarVal * formation[3] != 0:
                          print " (-) evening star candle pattern\n"
                  elif formation[0] == 'dark_cloud':
                      overallScore += darkCloudVal * formation[3]
                      if darkCloudVal * formation[3] != 0:
                          print " (-) dark cloud candle pattern\n"

          score, oscilatorsAndIndicators = oscilators.oscillatorStrategy(self.closing,self.highest,self.lowest,len(self.closing))
          overallScore += newHighNewLowVal * oscilatorsAndIndicators[0]
          if newHighNewLowVal * oscilatorsAndIndicators[0] > 0:
              print " (+) new high - new low index\n"
          elif newHighNewLowVal * oscilatorsAndIndicators[0] < 0:
              print " (-) new high - new low index\n"

          overallScore += bollignerVal * oscilatorsAndIndicators[1]
          if bollignerVal * oscilatorsAndIndicators > 0:
              print " (+) bolligner bounds\n"
          elif bollignerVal * oscilatorsAndIndicators < 0:
              print " (-) bolligner bounds\n"

          overallScore += momentumVal * oscilatorsAndIndicators[2]
          if momentumVal * oscilatorsAndIndicators > 0:
              print " (+) momentum oscilator\n"
          elif momentumVal * oscilatorsAndIndicators < 0:
              print " (-) momentum oscilator\n"

          overallScore += rocVal * oscilatorsAndIndicators[3]
          if rocVal * oscilatorsAndIndicators[3] > 0:
              print " (+) roc oscilator\n"
          elif rocVal * oscilatorsAndIndicators[3] < 0:
              print " (-) roc oscilator\n"

          overallScore += cciVal * oscilatorsAndIndicators[4]
          if cciVal * oscilatorsAndIndicators[4] > 0:
              print " (+) cci oscilator\n"
          elif cciVal * oscilatorsAndIndicators[4] < 0:
              print " (-) cci oscilator\n"

          overallScore += rsiVal * oscilatorsAndIndicators[5]
          if rsiVal * oscilatorsAndIndicators[5] > 0:
              print " (+) rsi oscilator\n"
          elif rsiVal * oscilatorsAndIndicators[5] < 0:
              print " (-) rsi oscilator\n"

          overallScore += williamsVal * oscilatorsAndIndicators[6]
          if williamsVal * oscilatorsAndIndicators[6] > 0:
              print " (+) williams oscilator\n"
          elif williamsVal * oscilatorsAndIndicators[6] < 0:
              print " (-) williams oscilator\n"
          print "\n Overall score: ",overallScore, "\n"
          if  overallScore > positiveSignal:
              print " technical analysis generated positive signal, however fundamental analysis should be also considered\n"
          else
              print " technical analysis generated negative signal, if you own actives it is recommended to sell, however fundamental analysis should be also considered\n"

          print " remember that authors of this software do not take any responsibility for possible financial loss"



    