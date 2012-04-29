from TechAnalysisModule.candles import *
import TechAnalysisModule.trendAnalysis as trend
import TechAnalysisModule.oscilators as osc

trendVal = 100
"""Formacje"""
"""Odwrocenie trendu wzrostowego"""
headAndShouldersVal = 100
risingWedgeVal = 80
fallingTriangleVal = 80
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
#sygnał kupna
risingBreakawayGapVal = 50
risingContinuationGapVal = 30
fallingExhaustionGapVal = 10 

#sygnał sprzedaży
fallingBreakawayGapVal = -50
risingExhaustionGapVal = -50
fallongContinuationGapVal = -30

"""Formacje swiecowe"""
#sygnał kupna
bull3Val = 15
mornigStarVal = 10
piercingVal = 5

#sygnał sprzedaży
bear3Val= -15
eveningStarVal = -10
darkCloudVal = -5 
