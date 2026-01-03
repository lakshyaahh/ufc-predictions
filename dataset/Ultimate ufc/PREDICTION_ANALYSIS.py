"""
UFC FIGHT PREDICTION ANALYSIS & RESULTS
========================================

PREDICTION EXECUTION SUMMARY
============================

Date: January 3, 2026
Event: December 14, 2024 UFC Card (13 Fights)
Model Used: RandomForestClassifier (trained on 6,528 historical fights)
Output File: predictions.csv

OVERALL PREDICTIONS
===================

Total Fights Analyzed: 13
- Red Corner (First Fighter) Predicted to Win: 8 fights (61.5%)
- Blue Corner (Second Fighter) Predicted to Win: 5 fights (38.5%)
- Average Prediction Confidence: 62.2%

DETAILED FIGHT-BY-FIGHT PREDICTIONS
===================================

1. COLBY COVINGTON vs JOAQUIN BUCKLEY
   Prediction: JOAQUIN BUCKLEY (BlueFighter)
   Colby Covington:    45.5%
   Joaquin Buckley:    54.5% ✓
   Confidence: 54.5%
   
2. CUB SWANSON vs BILLY QUARANTILLO
   Prediction: CUB SWANSON (RedFighter)
   Cub Swanson:        51.0% [PRED]
   Billy Quarantillo:  49.0%
   Confidence: 51.0%
   
3. MANEL KAPE vs BRUNO SILVA
   Prediction: BRUNO SILVA (BlueFighter)
   Manel Kape:         43.5%
   Bruno Silva:        56.5% ✓
   Confidence: 56.5%
   
4. VITOR PETRINO vs DUSTIN JACOBY
   Prediction: VITOR PETRINO (RedFighter)
   Vitor Petrino:      68.5% ✓
   Dustin Jacoby:      31.5%
   Confidence: 68.5% (HIGH)
   
5. ADRIAN YANEZ vs DANIEL MARCOS
   Prediction: DANIEL MARCOS (BlueFighter)
   Adrian Yanez:       48.0%
   Daniel Marcos:      52.0% ✓
   Confidence: 52.0%
   
6. NAVAJO STIRLING vs TUCO TOKKOS
   Prediction: NAVAJO STIRLING (RedFighter)
   Navajo Stirling:    74.2% ✓
   Tuco Tokkos:        25.8%
   Confidence: 74.2% (HIGH)
   
7. MICHAEL JOHNSON vs OTTMAN AZAITAR
   Prediction: OTTMAN AZAITAR (BlueFighter)
   Michael Johnson:    48.0%
   Ottman Azaitar:     52.0% ✓
   Confidence: 52.0%
   
8. JOEL ALVAREZ vs DRAKKAR KLOSE
   Prediction: JOEL ALVAREZ (RedFighter)
   Joel Alvarez:       51.5% ✓
   Drakkar Klose:      48.5%
   Confidence: 51.5%
   
9. SEAN WOODSON vs FERNANDO PADILLA
   Prediction: SEAN WOODSON (RedFighter)
   Sean Woodson:       86.5% ✓
   Fernando Padilla:   13.5%
   Confidence: 86.5% (VERY HIGH)
   
10. MILES JOHNS vs FELIPE LIMA
    Prediction: MILES JOHNS (RedFighter)
    Miles Johns:        77.0% ✓
    Felipe Lima:        23.0%
    Confidence: 77.0% (HIGH)
    
11. MIRANDA MAVERICK vs JAMEY-LYN HORTH
    Prediction: MIRANDA MAVERICK (RedFighter)
    Miranda Maverick:   64.0% ✓
    Jamey-Lyn Horth:    36.0%
    Confidence: 64.0%
    
12. DAVEY GRANT vs RAMON TAVERAS
    Prediction: RAMON TAVERAS (BlueFighter)
    Davey Grant:        43.5%
    Ramon Taveras:      56.5% ✓
    Confidence: 56.5%
    
13. JOSEFINE KNUTSSON vs PIERA RODRIGUEZ
    Prediction: JOSEFINE KNUTSSON (RedFighter)
    Josefine Knutsson:  65.0% ✓
    Piera Rodriguez:    35.0%
    Confidence: 65.0%

HIGHEST CONFIDENCE PREDICTIONS
==============================

1. Sean Woodson vs Fernando Padilla - Sean Woodson 86.5%
2. Miles Johns vs Felipe Lima - Miles Johns 77.0%
3. Navajo Stirling vs Tuco Tokkos - Navajo Stirling 74.2%
4. Josefine Knutsson vs Piera Rodriguez - Josefine Knutsson 65.0%
5. Miranda Maverick vs Jamey-Lyn Horth - Miranda Maverick 64.0%

CLOSEST PREDICTIONS (Most Uncertain)
====================================

1. Cub Swanson vs Billy Quarantillo - 51.0% vs 49.0% (1% margin)
2. Joel Alvarez vs Drakkar Klose - 51.5% vs 48.5% (3% margin)
3. Adrian Yanez vs Daniel Marcos - 48.0% vs 52.0% (4% margin)
4. Michael Johnson vs Ottman Azaitar - 48.0% vs 52.0% (4% margin)
5. Colby Covington vs Joaquin Buckley - 45.5% vs 54.5% (9% margin)

MODEL PERFORMANCE CONTEXT
=========================

Training Data: 6,528 historical UFC fights
Test Accuracy: 56.89%
Model Type: RandomForestClassifier (200 trees)

Class Performance:
- RedFighter: Precision 61%, Recall 72%, F1-Score 0.66
- BlueFighter: Precision 48%, Recall 36%, F1-Score 0.41

The model performs better at predicting RedFighter wins (61% precision)
compared to BlueFighter wins (48% precision).

FEATURES USED FOR PREDICTIONS
==============================

1. ReachDiff - Reach difference between fighters (cm)
2. HeightDiff - Height difference between fighters (cm)
3. AgeDif - Age difference between fighters (years)
4. WinStreakDif - Win streak difference
5. LoseStreakDif - Lose streak difference
6. KODif - KO wins difference
7. SubDif - Submission wins difference
8. WinDif - Total wins difference
9. LossDif - Total losses difference

RECOMMENDATIONS FOR IMPROVEMENT
================================

1. Add More Features:
   - Striking accuracy/volume stats
   - Takedown defense stats
   - Recent form (last 3 fights)
   - Head-to-head history
   - Octagon time/experience

2. Try Alternative Models:
   - XGBoost (often better for tabular data)
   - Gradient Boosting
   - Neural Networks
   - Ensemble methods combining multiple models

3. Hyperparameter Tuning:
   - Adjust RandomForest max_depth, min_samples_split
   - Cross-validation for better evaluation
   - Weighted classes for imbalanced data

4. Data Improvements:
   - Include more recent fights (2024+)
   - Weight recent fights more heavily
   - Add engagement metrics (strikes per minute, etc.)

5. Post-Processing:
   - Calibrate probability predictions
   - Ensemble with expert opinions
   - Create confidence bands

FILES GENERATED
===============

✓ predictions.csv - All 13 fight predictions with probabilities
✓ Analysis report (this file)

NEXT STEPS
==========

1. Monitor actual fight results when December 14, 2024 fights occur
2. Calculate actual accuracy of these predictions
3. Use results to retrain and improve model
4. Consider adding more features as suggested above
5. Try alternative modeling approaches

"""

print(__doc__)
