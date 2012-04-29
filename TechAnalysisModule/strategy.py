from TechAnalysisModule.candles import *
import TechAnalysisModule.trendAnalysis as trend
import TechAnalysisModule.oscilators as osc

trendVal = 100
"""Formacje"""
"""Odwrocenie trendu wzrostowego"""
headAndShouldersVal = -100
risingWedgeVal = -80
fallingTriangleVal = -80
"""Odwrocenie trendu spadkowego"""
reversedHeadAndShouldersVal = 100
fallingWedgeVal = 80
risingTriangleVal = 80
"""Kontynuacja trendu"""
symetricTriangleVal = 50
rectangleVal = 30
"""Wskazniki i oscylatory"""
oscilatorsVal = 50
# newHighNewLowVal - New High New Low Index
# bollignerVal - Bollinger Bands
# momentumVal - Momentum Oscillator
# rocVal - ROC
# cciVal - CCI
# rsiVal - RSI
# williamsVal - Williams Oscillator
"""Luki"""
"""Wzrostowe"""
risingBreakawayGap = 30
risingContinuationGap = 30
risingExhaustionGap = 30
"""Spadkowe"""
fallingBreakawayGap = -30
fallingContinuationGap = -30
fallingExhaustionGap = -30
"""Formacje swiecowe"""



def analyze(values, volumine):
    trend = trendVal * trend.optimizedTrend(values)
    hs = trend.lookForHeadAndShoulders(self.data.close, self.data.volume, 0)*headAndShouldersVal
    tTop = trend.lookForTripleTop(self.data.close, self.data.volume, 0)*tripleTopVal
        
        