# Run matched case control McNemar tests on baseline and simulated treatment profiles

import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from collections import defaultdict
from hbs.utils import create_engine_to_hbs, get_mcnemar_test_inputs, get_mcnemar_contingency_table

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# pd.set_option('display.float_format', '{:,.4f}'.format)  # display 2 decimal places and use ',' thousands separator

# set environment variables
# hbs_env = 'local'
hbs_env = 'remote'
engine = create_engine_to_hbs(access=hbs_env)

## McNemar tests: Matched pairs of dementia status
# Contingency table summarizes the status of matched pairs at the end of a period.
# Each matched pair contains one treated and one control subject (selected randomly from available controls).
# Each box counts the number of pairs that have the corresponding disease flag status, where the control status is listed first and the treated status is listed second. Control with disease and Treated without disease is 10, both with disease 11, Control without disease and treated with disease 01, and both without 00.
# According to McNemar's analysis, if treatment is unrelated to diabetes status then there should be about as many discordant pairs in one direction (YN) as the other (NY). This is what the statistic tests for. The null hypothesis is equal number of discordant pairs (no relationship between disease status and treatment arm).
# The rejection condition is one sided. The test statistic should be greater than 1 - alpha % of the chi-square distribution.
# Another way to describe the chi-square test: The p-value gives the probability of obtaining the observed frequencies if the expected frequencies are equal (H0: f1 = f2 = 0.5).

# Baseline McNemar tests
baseline_mcnemar_stats = defaultdict(list)
contingency_tables_baseline = {}
baseline_inputs_df = pd.DataFrame()
for year in range(1,31):
    category = 'dementia'
    inputs = get_mcnemar_test_inputs(year=year, category=category, engine=engine, baseline=True)
    inputs['year'] = year
    baseline_inputs_df = pd.concat([baseline_inputs_df, inputs])
    contingency_table = get_mcnemar_contingency_table(inputs)
    contingency_tables_baseline[year] = pd.DataFrame(
        contingency_table,
        index=pd.MultiIndex.from_tuples([('Control Group', 'Dementia'), ('Control Group', 'No Dementia')]),
        columns=pd.MultiIndex.from_tuples([('Treated Group', 'Dementia'), ('Treated Group', 'No Dementia')])
    )
    mcnemar_test = mcnemar(contingency_table, exact=False, correction=True)
    baseline_mcnemar_stats['year'].append(year)
    baseline_mcnemar_stats['pvalue'].append(mcnemar_test.pvalue)
    baseline_mcnemar_stats['statistic'].append(mcnemar_test.statistic)
baseline_mcnemar_df = pd.DataFrame(baseline_mcnemar_stats)
# observations: all tests fail to reject the null hypothesis at alpha=0.05.
#     year    pvalue  statistic
# 0      1  0.106674   2.602815
# 1      2  0.395179   0.722946
# 2      3  0.244801   1.352730
# 3      4  0.111047   2.539264
# 4      5  0.255079   1.295271
# 5      6  0.276313   1.185136
# 6      7  0.576802   0.311433
# 7      8  0.619061   0.247189
# 8      9  0.353552   0.860667
# 9     10  0.190139   1.716543
# 10    11  0.358709   0.842406
# 11    12  0.481154   0.496248
# 12    13  0.974226   0.001044
# 13    14  0.459664   0.546713
# 14    15  0.961235   0.002362
# 15    16  0.452595   0.564146
# 16    17  0.966726   0.001740
# 17    18  0.940212   0.005626
# 18    19  0.734762   0.114784
# 19    20  0.778005   0.079478
# 20    21  0.863734   0.029455
# 21    22  0.983472   0.000429
# 22    23  0.284691   1.144560
# 23    24  0.348509   0.878880
# 24    25  0.359538   0.839506
# 25    26  0.149480   2.077547
# 26    27  0.841567   0.039956
# 27    28  0.077752   3.111268
# 28    29  0.501624   0.451499
# 29    30  0.437682   0.602353

for year in contingency_tables_baseline.keys():
    print(f"Year {year}:")
    print(contingency_tables_baseline[year])
    print("__________________________________________________")
# Year 1:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             6572        5210
#               No Dementia          5377       32841
# __________________________________________________
# Year 2:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             9318        7428
#               No Dementia          7533       24183
# __________________________________________________
# Year 3:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            12327        8131
#               No Dementia          8281       18537
# __________________________________________________
# Year 4:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            15055        8092
#               No Dementia          8297       14625
# __________________________________________________
# Year 5:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            17312        7932
#               No Dementia          8077       11550
# __________________________________________________
# Year 6:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            19282        7508
#               No Dementia          7643        9225
# __________________________________________________
# Year 7:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            20794        7173
#               No Dementia          7241        7326
# __________________________________________________
# Year 8:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            21892        6775
#               No Dementia          6834        5939
# __________________________________________________
# Year 9:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22963        6231
#               No Dementia          6336        4800
# __________________________________________________
# Year 10:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            23460        5720
#               No Dementia          5862        3905
# __________________________________________________
# Year 11:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            23780        5292
#               No Dementia          5197        3039
# __________________________________________________
# Year 12:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            23472        4762
#               No Dementia          4832        2446
# __________________________________________________
# Year 13:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            23229        4309
#               No Dementia          4313        1938
# __________________________________________________
# Year 14:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22762        3831
#               No Dementia          3897        1536
# __________________________________________________
# Year 15:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22165        3384
#               No Dementia          3389        1220
# __________________________________________________
# Year 16:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            21315        3011
#               No Dementia          2952         948
# __________________________________________________
# Year 17:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            20203        2588
#               No Dementia          2584         738
# __________________________________________________
# Year 18:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            19041        2225
#               No Dementia          2219         589
# __________________________________________________
# Year 19:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            17830        1910
#               No Dementia          1932         474
# __________________________________________________
# Year 20:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            16611        1619
#               No Dementia          1602         363
# __________________________________________________
# Year 21:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            15121        1370
#               No Dementia          1380         260
# __________________________________________________
# Year 22:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            13943        1165
#               No Dementia          1165         206
# __________________________________________________
# Year 23:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            12801         989
#               No Dementia           941         162
# __________________________________________________
# Year 24:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            11611         841
#               No Dementia           802         122
# __________________________________________________
# Year 25:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            10307         706
#               No Dementia           671          91
# __________________________________________________
# Year 26:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             9102         579
#               No Dementia           530          67
# __________________________________________________
# Year 27:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             8016         454
#               No Dementia           447          57
# __________________________________________________
# Year 28:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             6997         379
#               No Dementia           331          41
# __________________________________________________
# Year 29:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             5943         292
#               No Dementia           275          36
# __________________________________________________
# Year 30:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             4842         221
#               No Dementia           204          24
# __________________________________________________

## Simulated Treatment McNemar Tests
simulated_mcnemar_stats = defaultdict(list)
contingency_tables_simulated = {}
sim_inputs_df = pd.DataFrame()
for year in range(1,31):
    category = 'dementia'
    inputs = get_mcnemar_test_inputs(year=year, category=category, engine=engine, baseline=False)
    inputs['year'] = year
    sim_inputs_df = pd.concat([sim_inputs_df, inputs])
    contingency_table = get_mcnemar_contingency_table(inputs)
    contingency_tables_simulated[year] = pd.DataFrame(
        contingency_table,
        index=pd.MultiIndex.from_tuples([('Control Group', 'Dementia'), ('Control Group', 'No Dementia')]),
        columns=pd.MultiIndex.from_tuples([('Treated Group', 'Dementia'), ('Treated Group', 'No Dementia')])
    )
    mcnemar_test = mcnemar(contingency_table, exact=False, correction=True)
    simulated_mcnemar_stats['year'].append(year)
    simulated_mcnemar_stats['pvalue'].append(mcnemar_test.pvalue)
    simulated_mcnemar_stats['statistic'].append(mcnemar_test.statistic)
simulated_mcnemar_df = pd.DataFrame(simulated_mcnemar_stats)
# mcnemar tests detected prevention in the simulated treatment arm every year except year 1.
#     year        pvalue   statistic
# 0      1  3.466172e-01    0.885803
# 1      2  6.506598e-04   11.625150
# 2      3  1.028234e-05   19.458238
# 3      4  3.795627e-07   25.795549
# 4      5  1.451248e-10   41.093410
# 5      6  3.014702e-13   53.198622
# 6      7  1.124775e-17   73.280432
# 7      8  3.309796e-20   84.794884
# 8      9  3.614284e-21   89.174774
# 9     10  1.220802e-21   91.322250
# 10    11  4.882106e-34  147.942926
# 11    12  2.636747e-27  117.168587
# 12    13  9.277146e-32  137.520693
# 13    14  1.148417e-29  127.954572
# 14    15  1.586503e-34  150.176227
# 15    16  5.710500e-40  175.094025
# 16    17  1.234538e-36  159.826737
# 17    18  2.666803e-36  158.295876
# 18    19  5.241899e-34  147.801655
# 19    20  6.354956e-37  161.146705
# 20    21  6.628457e-33  142.761343
# 21    22  4.175088e-33  143.679492
# 22    23  5.693638e-38  165.942667
# 23    24  3.525722e-36  157.740935
# 24    25  5.567813e-34  147.681818
# 25    26  1.672324e-33  145.496933
# 26    27  6.777030e-26  110.730989
# 27    28  2.638417e-29  126.303772
# 28    29  2.285658e-23   99.197236
# 29    30  8.239434e-20   82.991803

# spot check contingency tables for direction of difference
# expected result: top right corner > bottom left corner
# the number of matched pairs where the treated subject does not have dementia and the control does (top right corner) consistently exceeds the number of matched pairs where the treated subject has dementia and the control does (bottom left corner). This confirms that there is a relationship between treatment arm and disease diagnosis, and that the direction is that of decreased tendency to get the disease in the simulated treated group.
# In all 30 years of the treatment simulation, the number of discordant matched pairs where the treated subject does not have dementia is greater than the number of pairs where only the control subject is without a dementia diagnosis. In year 1, the difference is not great enough to reach a significance level of alpha=0.05.

for year in contingency_tables_simulated.keys():
    print(f"Year {year}:")
    print(contingency_tables_simulated[year])
    print("__________________________________________________")
# Year 1:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             6422        5360
#               No Dementia          5262       32956
# __________________________________________________
# Year 2:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             9058        7688
#               No Dementia          7270       24446
# __________________________________________________
# Year 3:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            11913        8545
#               No Dementia          7977       18841
# __________________________________________________
# Year 4:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            14529        8618
#               No Dementia          7963       14959
# __________________________________________________
# Year 5:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            16693        8551
#               No Dementia          7732       11895
# __________________________________________________
# Year 6:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            18569        8221
#               No Dementia          7311        9557
# __________________________________________________
# Year 7:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            19993        7974
#               No Dementia          6928        7639
# __________________________________________________
# Year 8:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            21022        7645
#               No Dementia          6547        6226
# __________________________________________________
# Year 9:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22063        7131
#               No Dementia          6046        5090
# __________________________________________________
# Year 10:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22546        6634
#               No Dementia          5577        4190
# __________________________________________________
# Year 11:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22830        6242
#               No Dementia          4954        3282
# __________________________________________________
# Year 12:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22520        5714
#               No Dementia          4613        2665
# __________________________________________________
# Year 13:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            22295        5243
#               No Dementia          4108        2143
# __________________________________________________
# Year 14:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            21846        4747
#               No Dementia          3706        1727
# __________________________________________________
# Year 15:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            21270        4279
#               No Dementia          3217        1392
# __________________________________________________
# Year 16:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            20428        3898
#               No Dementia          2813        1087
# __________________________________________________
# Year 17:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            19362        3429
#               No Dementia          2458         864
# __________________________________________________
# Year 18:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            18257        3009
#               No Dementia          2108         700
# __________________________________________________
# Year 19:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            17097        2643
#               No Dementia          1829         577
# __________________________________________________
# Year 20:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            15925        2305
#               No Dementia          1519         446
# __________________________________________________
# Year 21:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            14494        1997
#               No Dementia          1309         331
# __________________________________________________
# Year 22:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            13372        1736
#               No Dementia          1097         274
# __________________________________________________
# Year 23:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            12270        1520
#               No Dementia           887         216
# __________________________________________________
# Year 24:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia            11116        1336
#               No Dementia           760         164
# __________________________________________________
# Year 25:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             9865        1148
#               No Dementia           634         128
# __________________________________________________
# Year 26:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             8716         965
#               No Dementia           502          95
# __________________________________________________
# Year 27:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             7674         796
#               No Dementia           427          77
# __________________________________________________
# Year 28:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             6709         667
#               No Dementia           314          58
# __________________________________________________
# Year 29:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             5696         539
#               No Dementia           257          54
# __________________________________________________
# Year 30:
#                           Treated Group
#                                Dementia No Dementia
# Control Group Dementia             4645         418
#               No Dementia           192          36
# __________________________________________________

