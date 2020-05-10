# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ### Replication power simulation
#
# Strategy:
#
# - sample subjects from wessel replication 1 in order to create a dataset with particular N (using fabricatr
# - fit lmer to dataset 
# - create 3 simulated datasets using appropriate value for interaction beta
# - run models on simulated datasets after combining across sites (simulating our 3 sites)
# - store pvalue and cohen's d for observed effect
#

# +
import numpy as np
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import r, pandas2ri
import time
from pathlib import Path
import pickle
import random
import string

pandas2ri.activate()
lme4 = importr('lme4')
stats = importr('stats')
lmerTest = importr('lmerTest')
EMAtools = importr('EMAtools')
fabricatr = importr('fabricatr')
# %load_ext rpy2.ipython


# -

# Load the data
# + magic_args="-o rep1Df" language="R"
#
r("""
library('tidyverse')
rep1Df = read_delim('../processed_data/study-1_task-auction_data.tsv', '\t')
rep1Df['X1'] = NULL
rep1Df = rep1Df %>% 
   mutate(stimValueFactor = as.factor(auctionStimValue))
""")
rep1Df = r['rep1Df']
# +
# function to run ezANOVA on the summary data

run_ez = r('''run_ez = function(summaryDf){
library(ez)
summaryDf['auctionStimValue'] = as.factor(summaryDf$auctionStimValue)
summaryDf['auctionCondition'] = as.factor(summaryDf$auctionCondition)
summaryDf['site'] = as.factor(summaryDf$site)
summaryDf['subcode_unique'] = as.factor(summaryDf$subcode_unique)

#Run an ANOVA on the mean correct RT data.
CombinedExclusiveAuctionANOVA = ezANOVA(
  data = summaryDf
  , dv = chosenAuctionAmount
  , wid = subcode_unique
  , within = .(auctionStimValue,auctionCondition)
  , detailed = TRUE
)
}
''')
# -

# Now we loop through the main simulation runs.  on each round we generate a simulated dataset for each site (by resampling from the existing dataset using `fabricatr` and then simulating using lme4 `simulate()`), and then we fit three models:
# - full mixed model using `lmer()` with random intercept and interaction slope
# - mixed model on summary data for each subject, with random intercept (i.e. treating slope as fixed effect)
# - standard repeated measures ANOVA model on summary data, using ezANOVA (with Huhyn-Feldt correction for nonsphericity)

# +
# formulas for lmer analyses

testmode = True

# full mixed model with random intercept and interaction slope
formula = """chosenAuctionAmount ~ 
              auctionStimValue*auctionCondition + 
              (1 + auctionStimValue*auctionCondition|subcode_unique)"""

# formula for random intercept model on summary data
formula_summary = """chosenAuctionAmount ~ 
              auctionStimValue*auctionCondition + 
              (1 |subcode_unique)"""

n = 79  # N determined by previous power analysis
seed = None
if testmode:
    nruns=1
else:
    nruns = 1000

# since we can't specify a standardized effect size, we randomly select
# the interaction parameter from within this range (based on pilot simulations)
# and then compute the observed cohen's D for the analysis
int_param_max = 5
int_param_min = 1

# store full results to a dictionary
results_sim_full = {}
results_sim_full['params'] = {'int_param_max': int_param_max,
                            'int_param_min': int_param_min,
                            'n': n,
                            'formulas': [formula, formula_summary]}

results_sim = pd.DataFrame(columns=['int_param', 'cohensd_int', 'int_pval'])

now = time.time()
et = []

# use a specific seed to get reproducible results
rng = np.random.RandomState(seed)

# not sure if this actually works for fabricatr
#r('set.seed(1)')


for i in range(nruns):
    results_sim_full[i] = {}
    # choose an interaction parameter from within the range of interest
    int_param = int_param_min + np.random.rand()*(int_param_max - int_param_min)
    
    # print a progress report with ETA
    if i > 0:
        et.append(time.time() - now)
        print(i, int_param, et[-1], 'eta:', (nruns - i)*np.mean(et)/60, 'mins')
        now = time.time()
    
    # resample data from original, by subject
    simDf = fabricatr.resample_data(rep1Df, n, r("c('subcode')"), True)
    
    # fit mixed model to original dataset, to estimate random effects
    m1 = lme4.lmer(formula=formula, data=simDf)

    # set coefs, with fixed intercept and main effect and 
    # varying interaction parameter
    coefs=r('list(beta=c(139,10,0,%f))' % int_param)
    
    # create simulated data for the three sites using the fitted model
    # with the new coefficients
    s = lme4.simulate_merMod(m1, newparams=coefs, nsim=3, seed=rng.randint(0,10000))
    simDf1 = simDf.copy()
    simDf1['chosenAuctionAmount'] = s.sim_1.values
  
    
    # fit full mixed model to combined data
    # do not include site random effect as it is accounted for by subject
    sm1 = lme4.lmer(formula=formula, data=simDf1)
    sm1_coefs = lmerTest.get_coefmat(sm1)
    results_sim.loc[i, 'int_pval'] = sm1_coefs[3,4]
    results_sim.loc[i, 'cohensd_int'] = EMAtools.lme_dscore(
        sm1, simDf1, 'lme4').loc['auctionStimValue:auctionConditionstop', 'd']
    results_sim.loc[i, 'int_param'] = int_param
    results_sim_full[i]['lmer_full'] = {'coefs': sm1_coefs,
                                        'summary': lmerTest.summary_merModLmerTest(sm1)}
    
    # create summary data for simple repeated measures analyses
    summaryDf = simDf1.groupby(['subcode_unique',
                               'auctionStimValue', 
                               'auctionCondition']).mean().reset_index()

    # use ezanova
    ez = run_ez(summaryDf)
    results_sim.loc[i, 'int_pval_ez'] = ez[2].query(
        'Effect=="auctionStimValue:auctionCondition"').loc[:, "p[HF]"].values[0]
    results_sim_full[i]['ez'] = ez
    
    # fit lmer model with random intercept to summary data
    sm3 = lme4.lmer(formula=formula_summary, data=summaryDf)
    sm3_coefs = lmerTest.get_coefmat(sm3)
    results_sim.loc[i, 'int_pval_simple'] = sm3_coefs[3,4]
    results_sim.loc[i, 'cohensd_int_simple'] = EMAtools.lme_dscore(
        sm3, summaryDf, 'lme4').loc[
            'auctionStimValue:auctionConditionstop', 'd']
    results_sim_full[i]['lmer_summary']={'coefs': sm3_coefs,
                                        'summary': lmerTest.summary_merModLmerTest(sm3)}

run_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

out_path = Path('../processed_data/powersim_singlesite')
if not out_path.exists():
    out_path.mkdir()

results_sim.to_csv(str(out_path) + '/power_sim_mixedmodel_singlesite_%s.csv' % run_string)
with open(str(out_path) + '/power_sim_mixedmodel_singlesite_%s.pkl' % run_string, 'wb') as f:
    pickle.dump(results_sim_full, f)
