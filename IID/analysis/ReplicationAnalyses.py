# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Statistical analysies for Wessel replication 1
#

# %%
import pandas as pd
import statsmodels.formula.api as smf
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

datadir = Path('../data/processed_data')


# %% [markdown]
# ### Auction data analyses

# %%
### load data

auction_datafile = datadir / 'study-1_task-auction_data.tsv'
auction_data = pd.read_csv(auction_datafile, sep='\t', index_col=0)

print(auction_data.columns)

# %%
viol_plot = sns.catplot(
    x='auctionStimValue',
    y='chosenAuctionAmount',
    hue='auctionCondition',
    data=auction_data,
    palette="colorblind",
    kind='violin',
    height=6,
    aspect=1.5,
    legend=False)

plt.ylim([0, 500])
viol_plot.ax.legend(loc=2, fontsize=18)

# %%
### Fit model to data

md = smf.mixedlm("chosenAuctionAmount ~ auctionStimValue*auctionCondition", auction_data, groups=auction_data["subcode"])
mdf = md.fit()
print(mdf.summary())

# %%
## Diagnostic plots

auction_data['mixedlm_resid'] = mdf.resid
sns.pairplot(auction_data)
