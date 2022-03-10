#!/usr/bin/env python
# coding: utf-8

# # 1) IMPORTING THE DATA
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

#players
pl2 = pd.read_csv("player_overviews_unindexed.csv")

#rankings
rk2 = pd.read_csv('rankings_1973-2017.csv')
rk2 = rk2.set_index('week_title')

#match results
mtch_67 = pd.read_csv('match_scores_1877-1967.csv')
mtch_90 = pd.read_csv('match_scores_1968-1990.csv')
mtch_16 = pd.read_csv('match_scores_1991-2016.csv')
mtch_17 = pd.read_csv('match_scores_2017.csv')

#match stats
matchestats_2017 = pd.read_csv('match_stats_2017.csv')
mstat = pd.read_csv('match_stats_1991-2016.csv')

#tournaments
trmt = pd.read_csv('tournaments_1877-2017.csv')


# # 2) ARRANGING THE DATA
# 

# ## INSIGHTS WE WILL TRY TO EXTRACT
# 
# ### 1) Competitiveness of tennis!
# 
# #### | Are there more/less players and more/less tournaments? With more players and tournaments tennis would be more competitive!
# 
# ##### a) evolution of the amount of tournaments across the years
# ##### b) evolution of the amount of players across the years
# 
# 
# #### | Is the circuit more diverse? 
# ##### c) amount of different nationalities in top (10, 25, 50) across time
# ##### d) Ranking race between countries with across time
# 
# 
# #### | Is it tougher to play?
# ##### e) average match duration across time and across surface
# ##### e) closeness/wideness of scores across time
# ##### f) Surface advantage per nationality
# 
# ### 2) The optimal tennis player!
# 
# #### | Are players' physique evolving?
# ##### c) Evolution of height across time of top (10, 25, 50)
# ##### d) Evolution of weight across time of top, (10, 25, 50)
# ##### e) Average age entrance in top 1(0, 25, 50) across time
# 
# #### | Are players changing their style of play across the years?
# ##### c) Serves data: evolutions of amount of aces & double faults across time
# ##### d) evolution of the amount of players doing One hand return and being left handed

# ### A) Players dataset
# 

# In[7]:


#pl2.head()


# In[8]:


#pl2.info()


# ### B) Rankings dataset
# 

# In[11]:


#rk2.head()


# In[10]:


#rk2.info()


# ### c) Matches and match stats

# In[13]:


#mstat.head()


# In[12]:


#mstat.info()


# In[14]:


#mtch_67.info()


# In[19]:


#mtch_90.info()


# In[18]:


#mtch_16.info()


# In[20]:


#mtch_17.info()


# In[21]:


a = mtch_17.dtypes
b = mtch_16.dtypes
c = mtch_90.dtypes
d = mtch_67.dtypes 

a = pd.DataFrame( a, columns = ['mtch_17'])
a['mtch_16'] = b
a['mtch_90'] = c
a['mtch_67'] = d

a


# In[22]:


del mtch_67['match_stats_url_suffix']
del mtch_90['match_stats_url_suffix']
del mtch_16['match_stats_url_suffix']
del mtch_17['match_stats_url_suffix']

del mtch_67['winner_seed']
del mtch_90['winner_seed']
del mtch_16['winner_seed']
del mtch_17['winner_seed']

del mtch_67['loser_seed']
del mtch_90['loser_seed']
del mtch_16['loser_seed']
del mtch_17['loser_seed']


# In[23]:


mtches = [mtch_67, mtch_90, mtch_16, mtch_17]
mtch = pd.concat(mtches)


# In[25]:


#mtch.head()


# # 3) EXTRACTING INSIGHTS
# 

# ### creating top 10,25,50 per year
# 
# 

# #### merging pl2 and rk2 !
# 

# In[34]:


pl = pl2
rk = rk2
pl = pl.set_index('player_id')
rk = rk.set_index('player_id')


# In[35]:


plrk = pd.merge(
    rk,
    pl,
    how="outer",
    left_index= True,
    right_index= True,
  
)


# #### obtaining amount of weeks in top (10, 25, 50) per country per year
# 

# In[41]:


#t10_flags/year
t10_flags_yearly = plrk.loc[plrk['rank_number'] <= 10, ['week_year', 'rank_number','flag_code']]
t10_flags_yearly = t10_flags_yearly.groupby(['week_year', 'flag_code']).count()

#t25_flags/year
t25_flags_yearly = plrk.loc[plrk['rank_number'] <= 25, ['week_year', 'rank_number','flag_code']]
t25_flags_yearly = t25_flags_yearly.groupby(['week_year', 'flag_code']).count()

#t50_flags/year
t50_flags_yearly = plrk.loc[plrk['rank_number'] <= 50, ['week_year', 'rank_number','flag_code']]
t50_flags_yearly = t50_flags_yearly.groupby(['week_year', 'flag_code']).count()


# In[42]:


#t25_flags_yearly.tail()


# In[43]:


#t50_flags_yearly.tail()


# In[44]:


t10_flags_yearly = t10_flags_yearly.sort_values(['week_year'], ascending = False)
t10_flags_yearly

file_name = 't10_flags_yearly.xlsx'
t10_flags_yearly.to_excel(file_name)

file_name = 't25_flags_yearly.xlsx'
t50_flags_yearly.to_excel(file_name)

file_name = 't50_flags_yearly.xlsx'
t25_flags_yearly.to_excel(file_name)


# #### evolution of height and weight in top across time
# 

# In[46]:


#plrk.info()


# In[47]:


#t10 stats

t10_player_stats_year = plrk.loc[plrk['rank_number'] <= 10, ['week_year','player_age','tourneys_played','weight_kg','height_cm', 'turned_pro', 'ranking_points']]
t10_player_stats_year = t10_player_stats_year.pivot_table(index='week_year')
#height
t10_player_height_year = t10_player_stats_year['height_cm']
#wheight
t10_player_weight_year = t10_player_stats_year['weight_kg']
#age
t10_player_age_year = t10_player_stats_year['player_age']
#tournaments played
t10_player_tournaments_year = t10_player_stats_year['tourneys_played']

#t25 stats
t25_player_stats_year = plrk.loc[plrk['rank_number'] <= 25, ['week_year','player_age','tourneys_played','weight_kg','height_cm', 'turned_pro', 'ranking_points']]
t25_player_stats_year = t25_player_stats_year.pivot_table(index='week_year')
#height
t25_player_height_year = t25_player_stats_year['height_cm']
#wheight
t25_player_weight_year = t25_player_stats_year['weight_kg']
#age
t25_player_age_year = t25_player_stats_year['player_age']
#tournaments played
t25_player_tournaments_year = t25_player_stats_year['tourneys_played']


#t50 stats
t50_player_stats_year = plrk.loc[plrk['rank_number'] <= 50, ['week_year','player_age','tourneys_played','weight_kg','height_cm', 'turned_pro', 'ranking_points']]
t50_player_stats_year = t50_player_stats_year.pivot_table(index='week_year')
#height
t50_player_height_year = t50_player_stats_year['height_cm']
#wheight
t50_player_weight_year = t50_player_stats_year['weight_kg']
#age
t50_player_age_year = t50_player_stats_year['player_age']
#tournaments played
t50_player_tournaments_year = t50_player_stats_year['tourneys_played']

#all players
all_player_stats_year = plrk.loc[plrk['rank_number']>0, ['week_year','player_age','tourneys_played','weight_kg','height_cm', 'turned_pro', 'ranking_points']]
all_player_stats_year = all_player_stats_year.pivot_table(index='week_year')
#height
all_player_height_year = all_player_stats_year['height_cm']
#wheight
all_player_weight_year = all_player_stats_year['weight_kg']
#age
all_player_age_year = all_player_stats_year['player_age']
#tournaments played
all_player_tournaments_year = all_player_stats_year['tourneys_played']

#plotting
fig,ax = plt.subplots(4, 1, figsize = (16,32))

#heights
ax[0].plot(t10_player_height_year, c = 'red', label = 't10')
ax[0].plot(t25_player_height_year, c = 'green', label = 't20')
ax[0].plot(t50_player_height_year, c = 'blue', label = 't50')
ax[0].plot(all_player_height_year, c = 'purple', label = 'all')
ax[0].set_title('Evolution of Tennis players height in cm across time', size = 30)
ax[0].set_xlabel('year', size = 25)
ax[0].set_ylabel('height in cm', size = 25)
ax[0].legend(fontsize = 12)

#pweights
ax[1].plot(t10_player_weight_year, c = 'red', label = 't10')
ax[1].plot(t25_player_weight_year, c = 'green', label = 't20')
ax[1].plot(t50_player_weight_year, c = 'blue', label = 't50')
ax[1].plot(all_player_weight_year, c = 'purple', label = 'all')
ax[1].set_title('Evolution of Tennis players weight in kg across time', size = 30)
ax[1].set_xlabel('year', size = 25)
ax[1].set_ylabel('weight in kg', size = 25)
ax[1].legend(fontsize = 12)

#plotting age
ax[2].plot(t10_player_age_year, c = 'red', label = 't10')
ax[2].plot(t25_player_age_year, c = 'green', label = 't20')
ax[2].plot(t50_player_age_year, c = 'blue', label = 't50')
ax[2].plot(all_player_age_year, c = 'purple', label = 'all')
ax[2].set_title('Evolution of Tennis players average age across time', size = 30)
ax[2].set_xlabel('year', size = 25)
ax[2].set_ylabel('average age', size = 25)
ax[2].legend(fontsize = 12)

#tournaments played
ax[3].plot(t10_player_tournaments_year, c = 'red', label = 't10')
ax[3].plot(t25_player_tournaments_year, c = 'green', label = 't20')
ax[3].plot(t50_player_tournaments_year, c = 'blue', label = 't50')
ax[3].plot(all_player_tournaments_year, c = 'purple', label = 'all')
ax[3].set_title('Evolution of Tennis players tournaments played across time', size = 30)
ax[3].set_xlabel('year', size = 25)
ax[3].set_ylabel('tournaments played', size = 25)
ax[3].legend(fontsize = 12)


# In[48]:


file_name = 't10_player_stats_year.xlsx'
t10_player_stats_year.to_excel(file_name)

file_name2 = 't25_player_stats_year.xlsx'
t25_player_stats_year.to_excel(file_name2)

file_name3 = 't50_player_stats_year.xlsx'
t50_player_stats_year.to_excel(file_name3)

file_name4 = 'all_player_stats_year.xlsx'
all_player_stats_year.to_excel(file_name4)


# #### evolution frequency of one handed backhand across time

# In[54]:


plrk_backhand = plrk.loc[~plrk['backhand'].isnull()]
plrk_backhand.head()


# In[55]:


#t10_backhand_yearly
t10_backhand_yearly = plrk_backhand.loc[plrk_backhand['rank_number'] <= 10, ['week_year', 'backhand', 'rank_number']]


# In[56]:


#calculating one hand ratios t10

#getting for t10 the one handed and 2 handed
ratio_t10_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
ratio_t10_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]

# pivoting one ahnded
ratio_t10_backhand_yearly_one = ratio_t10_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t10_backhand_yearly_one['Two-Handed Backhand'] =  ratio_t10_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t10_backhand_yearly_one['One-Hand Ratio'] = ratio_t10_backhand_yearly_one['One-Handed Backhand'] / (ratio_t10_backhand_yearly_one['One-Handed Backhand'] + ratio_t10_backhand_yearly_one['Two-Handed Backhand'])
#deleting unnecessary columns
del ratio_t10_backhand_yearly_one['One-Handed Backhand']
del ratio_t10_backhand_yearly_one['Two-Handed Backhand']


# In[57]:


##Backhands insight

#t10 one hand backhand data
t10_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
t10_backhand_yearly_one = t10_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#t10 two hand backhand data
t10_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]
t10_backhand_yearly_two = t10_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#t25 one hand backhand data
t25_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
t25_backhand_yearly_one = t25_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#t25 two hand backhand data
t25_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]
t25_backhand_yearly_two = t25_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#t50 one hand backhand data
t50_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
t50_backhand_yearly_one = t50_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#t50 two hand backhand data
t50_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]
t50_backhand_yearly_two = t50_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#all two hand and one hand backhand data
#all one hand backhand data
all_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
all_backhand_yearly_one = all_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')

#all two hand backhand data
all_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]
all_backhand_yearly_two = all_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')


#calculating one hand ratios 

#t10

#getting for t10 the one handed and 2 handed
ratio_t10_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
ratio_t10_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]

# pivoting one ahnded
ratio_t10_backhand_yearly_one = ratio_t10_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t10_backhand_yearly_one['Two-Handed Backhand'] =  ratio_t10_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t10_backhand_yearly_one['One-Hand Ratio'] = ratio_t10_backhand_yearly_one['One-Handed Backhand'] / (ratio_t10_backhand_yearly_one['One-Handed Backhand'] + ratio_t10_backhand_yearly_one['Two-Handed Backhand'])
#deleting unnecessary columns
del ratio_t10_backhand_yearly_one['One-Handed Backhand']
del ratio_t10_backhand_yearly_one['Two-Handed Backhand']

#t25

#getting for t10 the one handed and 2 handed
ratio_t25_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
ratio_t25_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]

# pivoting one ahnded
ratio_t25_backhand_yearly_one = ratio_t25_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t25_backhand_yearly_one['Two-Handed Backhand'] =  ratio_t25_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t25_backhand_yearly_one['One-Hand Ratio'] = ratio_t25_backhand_yearly_one['One-Handed Backhand'] / (ratio_t25_backhand_yearly_one['One-Handed Backhand'] + ratio_t25_backhand_yearly_one['Two-Handed Backhand'])
#deleting unnecessary columns
del ratio_t25_backhand_yearly_one['One-Handed Backhand']
del ratio_t25_backhand_yearly_one['Two-Handed Backhand']

#t50

#getting for t10 the one handed and 2 handed
ratio_t50_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
ratio_t50_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]

# pivoting one ahnded
ratio_t50_backhand_yearly_one = ratio_t50_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t50_backhand_yearly_one['Two-Handed Backhand'] =  ratio_t50_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t50_backhand_yearly_one['One-Hand Ratio'] = ratio_t50_backhand_yearly_one['One-Handed Backhand'] / (ratio_t50_backhand_yearly_one['One-Handed Backhand'] + ratio_t50_backhand_yearly_one['Two-Handed Backhand'])
#deleting unnecessary columns
del ratio_t50_backhand_yearly_one['One-Handed Backhand']
del ratio_t50_backhand_yearly_one['Two-Handed Backhand']

#t50
#getting for t10 the one handed and 2 handed
ratio_all_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['backhand'] == 'One-Handed Backhand')]
ratio_all_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['backhand'] == 'Two-Handed Backhand')]

# pivoting one ahnded
ratio_all_backhand_yearly_one = ratio_all_backhand_yearly_one.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_all_backhand_yearly_one['Two-Handed Backhand'] =  ratio_all_backhand_yearly_two.pivot_table(index='week_year', columns = 'backhand', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_all_backhand_yearly_one['One-Hand Ratio'] = ratio_all_backhand_yearly_one['One-Handed Backhand'] / (ratio_all_backhand_yearly_one['One-Handed Backhand'] + ratio_all_backhand_yearly_one['Two-Handed Backhand'])
#deleting unnecessary columns
del ratio_all_backhand_yearly_one['One-Handed Backhand']
del ratio_all_backhand_yearly_one['Two-Handed Backhand']


#plotting
fig,ax = plt.subplots(2, 1, figsize = (16,32))

#amount backhand one and 2
ax[0].plot(t10_backhand_yearly_one, c = 'red', label = 't10 one hand', linestyle = 'dotted')
ax[0].plot(t10_backhand_yearly_two, c = 'red', label = 't10 two hands', linestyle = 'solid')
ax[0].plot(t25_backhand_yearly_one, c = 'green', label = 't25 one hand', linestyle = 'dotted')
ax[0].plot(t25_backhand_yearly_two, c = 'green', label = 't25 two hands', linestyle = 'solid')
ax[0].plot(t50_backhand_yearly_one, c = 'blue', label = 't50 one hand', linestyle = 'dotted')
ax[0].plot(t50_backhand_yearly_two, c = 'blue', label = 't50 two hands', linestyle = 'solid')
ax[0].plot(all_backhand_yearly_one, c = 'purple', label = 'all one hand', linestyle = 'dotted')
ax[0].plot(all_backhand_yearly_two, c = 'purple', label = 'all two hands', linestyle = 'solid')
ax[0].set_title('Evolution of backhand among Tennis players across time', size = 30)
ax[0].set_xlabel('year', size = 25)
ax[0].set_ylabel('#players', size = 25)
ax[0].legend(fontsize = 12)

#ratio backhand one

ax[1].plot(ratio_t10_backhand_yearly_one, c = 'red', label = 'ratio t10 one hand', linestyle = 'solid')
ax[1].plot(ratio_t25_backhand_yearly_one, c = 'green', label = 'ratio t25 one hand', linestyle = 'solid')
ax[1].plot(ratio_t50_backhand_yearly_one, c = 'blue', label = 'ratio t25 one hand', linestyle = 'solid')
ax[1].plot(ratio_all_backhand_yearly_one, c = 'purple', label = 'ratio all one hand', linestyle = 'solid')
ax[1].set_title('Ratio of one hand backhand among Tennis players across time', size = 30)
ax[1].set_xlabel('year', size = 25)
ax[1].set_ylabel('ratio one hand backhand', size = 25)
ax[1].legend(fontsize = 12)


# In[58]:


all_backhand_yearly_one


# In[59]:



all_backhand_yearly_one['all_one']= all_backhand_yearly_one
all_backhand_yearly_one['all_two']= all_backhand_yearly_two
all_backhand_yearly_one['t10_one'] = t10_backhand_yearly_one
all_backhand_yearly_one['t25_one'] = t25_backhand_yearly_one
all_backhand_yearly_one['t10_two'] = t10_backhand_yearly_two
all_backhand_yearly_one['t25_two'] = t25_backhand_yearly_two
all_backhand_yearly_one['t50_two'] = t10_backhand_yearly_two
all_backhand_yearly_one['t50_one'] = t25_backhand_yearly_one
all_backhand_yearly_one['ratio_t10'] = ratio_t10_backhand_yearly_one
all_backhand_yearly_one['ratio_t25'] = ratio_t25_backhand_yearly_one
all_backhand_yearly_one['ratio_t50'] = ratio_t50_backhand_yearly_one
all_backhand_yearly_one['ratio_all'] = ratio_all_backhand_yearly_one
all_backhand_yearly_one.head()


# In[60]:


file_name = 'all_backhand_yearly_one.xlsx'
all_backhand_yearly_one.to_excel(file_name)


# ### evolution frequency handedness across time

# In[61]:


plrk_backhand = plrk.loc[~plrk['handedness'].isnull()]
plrk_backhand.head()


# In[62]:


## insight handedness

#t10 one hand backhand data
t10_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['handedness'] == 'Left-Handed')]
t10_backhand_yearly_one = t10_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#t10 two hand backhand data
t10_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['handedness'] == 'Right-Handed')]
t10_backhand_yearly_two = t10_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#t25 one hand backhand data
t25_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['handedness'] == 'Left-Handed')]
t25_backhand_yearly_one = t25_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#t25 two hand backhand data
t25_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['handedness'] == 'Right-Handed')]
t25_backhand_yearly_two = t25_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#t50 one hand backhand data
t50_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['handedness'] == 'Left-Handed')]
t50_backhand_yearly_one = t50_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#t50 two hand backhand data
t50_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['handedness'] == 'Right-Handed')]
t50_backhand_yearly_two = t50_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#all two hand and one hand backhand data
#all one hand backhand data
all_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['handedness'] == 'Left-Handed')]
all_backhand_yearly_one = all_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')

#all two hand backhand data
all_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['handedness'] == 'Right-Handed')]
all_backhand_yearly_two = all_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')


#calculating one hand ratios 

#t10

#getting for t10 the one handed and 2 handed
ratio_t10_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['handedness'] == 'Left-Handed')]
ratio_t10_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 10) & (plrk_backhand['handedness'] == 'Right-Handed')]

# pivoting one ahnded
ratio_t10_backhand_yearly_one = ratio_t10_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t10_backhand_yearly_one['Right-Handed'] =  ratio_t10_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t10_backhand_yearly_one['Left-Handed Ratio'] = ratio_t10_backhand_yearly_one['Left-Handed'] / (ratio_t10_backhand_yearly_one['Right-Handed'] + ratio_t10_backhand_yearly_one['Left-Handed'])
#deleting unnecessary columns
del ratio_t10_backhand_yearly_one['Right-Handed']
del ratio_t10_backhand_yearly_one['Left-Handed']

#t25

#getting for t10 the one handed and 2 handed
ratio_t25_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['handedness'] == 'Left-Handed')]
ratio_t25_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 25) & (plrk_backhand['handedness'] == 'Right-Handed')]

# pivoting one ahnded
ratio_t25_backhand_yearly_one = ratio_t25_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t25_backhand_yearly_one['Right-Handed'] =  ratio_t25_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t25_backhand_yearly_one['Left-Hand Ratio'] = ratio_t25_backhand_yearly_one['Left-Handed'] / (ratio_t25_backhand_yearly_one['Left-Handed'] + ratio_t25_backhand_yearly_one['Right-Handed'])
#deleting unnecessary columns
del ratio_t25_backhand_yearly_one['Right-Handed']
del ratio_t25_backhand_yearly_one['Left-Handed']

#t50

#getting for t10 the one handed and 2 handed
ratio_t50_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['handedness'] == 'Left-Handed')]
ratio_t50_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] <= 50) & (plrk_backhand['handedness'] == 'Right-Handed')]

# pivoting one ahnded
ratio_t50_backhand_yearly_one = ratio_t50_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_t50_backhand_yearly_one['Right-Handed'] =  ratio_t50_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_t50_backhand_yearly_one['Left-Handed Ratio'] = ratio_t50_backhand_yearly_one['Left-Handed'] / (ratio_t50_backhand_yearly_one['Right-Handed'] + ratio_t50_backhand_yearly_one['Left-Handed'])
#deleting unnecessary columns
del ratio_t50_backhand_yearly_one['Left-Handed']
del ratio_t50_backhand_yearly_one['Right-Handed']

#t50
#getting for t10 the one handed and 2 handed
ratio_all_backhand_yearly_one = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['handedness'] == 'Left-Handed')]
ratio_all_backhand_yearly_two = plrk_backhand.loc[(plrk_backhand['rank_number'] > 0) & (plrk_backhand['handedness'] == 'Right-Handed')]

# pivoting one ahnded
ratio_all_backhand_yearly_one = ratio_all_backhand_yearly_one.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#adding new two handed colum
ratio_all_backhand_yearly_one['Right-Handed'] =  ratio_all_backhand_yearly_two.pivot_table(index='week_year', columns = 'handedness', values = 'rank_number', aggfunc = 'count')
#computing the ratio
ratio_all_backhand_yearly_one['Left-Handed Ratio'] = ratio_all_backhand_yearly_one['Left-Handed'] / (ratio_all_backhand_yearly_one['Right-Handed'] + ratio_all_backhand_yearly_one['Left-Handed'])
#deleting unnecessary columns
del ratio_all_backhand_yearly_one['Left-Handed']
del ratio_all_backhand_yearly_one['Right-Handed']


#plotting
fig,ax = plt.subplots(2, 1, figsize = (16,16))

#amount backhand one and 2
ax[0].plot(t10_backhand_yearly_one, c = 'red', label = 't10 left hand', linestyle = 'dotted')
ax[0].plot(t10_backhand_yearly_two, c = 'red', label = 't10 right hand', linestyle = 'solid')
ax[0].plot(t25_backhand_yearly_one, c = 'green', label = 't25 left hand', linestyle = 'dotted')
ax[0].plot(t25_backhand_yearly_two, c = 'green', label = 't25 right hand', linestyle = 'solid')
ax[0].plot(t50_backhand_yearly_one, c = 'blue', label = 't50 left hand', linestyle = 'dotted')
ax[0].plot(t50_backhand_yearly_two, c = 'blue', label = 't50 right hand', linestyle = 'solid')
ax[0].plot(all_backhand_yearly_one, c = 'purple', label = 'all left hand', linestyle = 'dotted')
ax[0].plot(all_backhand_yearly_two, c = 'purple', label = 'all right hands', linestyle = 'solid')
ax[0].set_title('Evolution of Left-handed Tennis players across time', size = 30)
ax[0].set_xlabel('year', size = 25)
ax[0].set_ylabel('#players', size = 25)
ax[0].legend(fontsize = 12)

#ratio backhand one

ax[1].plot(ratio_t10_backhand_yearly_one, c = 'red', label = 'ratio t10 left-hand', linestyle = 'solid')
ax[1].plot(ratio_t25_backhand_yearly_one, c = 'green', label = 'ratio t25 left-hand', linestyle = 'solid')
ax[1].plot(ratio_t50_backhand_yearly_one, c = 'blue', label = 'ratio t25 left-hand', linestyle = 'solid')
ax[1].plot(ratio_all_backhand_yearly_one, c = 'purple', label = 'ratio all left-hand', linestyle = 'solid')
ax[1].set_title('Ratio of Left-handed Tennis players across time', size = 30)
ax[1].set_xlabel('year', size = 25)
ax[1].set_ylabel('ratio left handed', size = 25)
ax[1].legend(fontsize = 12)


# In[63]:



all_backhand_yearly_one['all_left']= all_backhand_yearly_one
all_backhand_yearly_one['all_right']= all_backhand_yearly_two
all_backhand_yearly_one['t10_left'] = t10_backhand_yearly_one
all_backhand_yearly_one['t25_left'] = t25_backhand_yearly_one
all_backhand_yearly_one['t10_right'] = t10_backhand_yearly_two
all_backhand_yearly_one['t25_right'] = t25_backhand_yearly_two
all_backhand_yearly_one['t50_left'] = t25_backhand_yearly_one
all_backhand_yearly_one['t50_right'] = t10_backhand_yearly_two
all_backhand_yearly_one['ratio_left_t10'] = ratio_t10_backhand_yearly_one
all_backhand_yearly_one['ratio_left_t25'] = ratio_t25_backhand_yearly_one
all_backhand_yearly_one['ratio_left_t50'] = ratio_t50_backhand_yearly_one
all_backhand_yearly_one['ratio_left_all'] = ratio_all_backhand_yearly_one
all_backhand_yearly_left = all_backhand_yearly_one

file_name = 'all_backhand_yearly_left.xlsx'
all_backhand_yearly_left.to_excel(file_name)


# ### MERGING matches, match stats, players, and tournament dtst

# In[64]:


mtchstats = pd.merge(mtch, mstat, on = "match_id", how = 'outer')
mst = pd.merge(mtchstats,trmt, on = 'tourney_year_id', how = 'outer')


# In[65]:


mst['player_id'] = mst['winner_player_id']
mstp = pd.merge(mst, pl2, on = 'player_id', how = 'outer')
mstp.columns


# In[66]:


df_surf = mstp[['tourney_year_id', 'tourney_year','tourney_name', 'tourney_id','tourney_location', 'match_id', 'tourney_surface', 'singles_winner_player_id', 'winner_aces', 'loser_aces', 'winner_double_faults', 'loser_double_faults', 'match_duration', 'player_id','weight_kg','height_cm', 'flag_code', 'winner_player_id' ,'player_slug']].copy()


# In[68]:


#mtch.info()


# In[69]:


df_surf['total_aces'] = mst['winner_aces'] + mst['loser_aces']


# In[70]:


df_surfgby = df_surf.groupby(['tourney_surface'])
df_surfgby


# ### Average amount of aces per surface across time

# In[71]:


#average amount of aces per surface

pvtsurf_aces = df_surf.pivot_table(index = 'tourney_year', columns = 'tourney_surface', values = 'total_aces', aggfunc = 'mean')
pvtsurf_aces


# In[74]:


file_name = 'pvtsurf_aces.xlsx'
#pvtsurf_aces.to_excel(file_name)


# ### match duration per surface type across time 

# In[75]:


#match duration per surface
pvtsurf_time = df_surf.pivot_table(index = 'tourney_year', columns = 'tourney_surface', values = 'match_duration', aggfunc = 'mean')
pvtsurf_time


# In[77]:


file_name = 'pvtsurf_time.xlsx'
#pvtsurf_time.to_excel(file_name)


# ### country ranking per surface (in ABSOLUTE terms)

# In[54]:


#players
pop = pd.read_csv("ideal_nationality.csv")
pop['flag_code'] = pop['Unnamed: 2']
pop['population'] = pop['?????']
del  pop['?????']
del pop['Unnamed: 2']

pop = pop[['flag_code','population']]


# In[55]:


df_surfadv = df_surf[['winner_player_id', 'flag_code', 'tourney_surface']]
surfflag = pd.merge(pop, df_surfadv, on = 'flag_code', how = 'outer')
surfflag


# In[56]:


#absolute value insight
df_surfadv = df_surfadv.groupby(['tourney_surface','flag_code']).count()
df_surfadv


# ### country ranking per surface ratioed! (we take into account country population!)
# 

# In[57]:


#ratioed insight

df_surfadv_ratio = surfflag[['winner_player_id', 'flag_code', 'tourney_surface','population']]
df_surfadv_ratio = (df_surfadv_ratio.groupby(['tourney_surface','flag_code', 'population']).count())
df_surfadv_ratio['winner_player_id'] = df_surfadv_ratio['winner_player_id']


df_surfadv_ratio = df_surfadv_ratio.reset_index('population')
df_surfadv_ratio['ratioed'] = df_surfadv_ratio['winner_player_id']/df_surfadv_ratio['population']
df_surfadv_ratio['ratioed'] = df_surfadv_ratio['ratioed']*1000
df_surfadv_ratio


# In[58]:


file_name = 'df_surfadv_ratio.xlsx'
#df_surfadv_ratio.to_excel(file_name)


# ### Height and aces 

# In[78]:


df_heightaces = df_surf.loc[df_surf['total_aces']!= 0]
#

df_heightaces_player = df_heightaces.pivot_table(index = ['height_cm'], values = 'total_aces', aggfunc = 'sum')
df_heightaces_player.sort_values(['height_cm'], ascending = False)


# In[79]:


#extracting insight!
df_heightaces = df_heightaces.pivot_table(index = 'height_cm', values = 'winner_aces', aggfunc = 'mean')
df_heightaces

#note that we are taking the mean here! we want to see how many aces the players do on average based on height

file_name = 'df_heightaces.xlsx'
#df_heightaces.to_excel(file_name)


# In[82]:


#df_surf.info()


# In[64]:


df_surf_flags = df_surf.groupby(['tourney_surface', 'flag_code']).count()
df_surf_flags


# # Last groupby 

# In[83]:


#group by of backhands
t10_backhand_yearly = t10_backhand_yearly.groupby(['week_year','backhand']).count()
t10_backhand_yearly


# In[ ]:




