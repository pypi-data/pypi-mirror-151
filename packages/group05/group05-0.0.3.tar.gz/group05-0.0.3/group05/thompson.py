

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

data_path = 'D:\韩特\研究生文档\研一下学期文档\抽样技术\作业/Ads_CTR_Optimisation.csv'

df = pd.read_csv(data_path)
df.head()
df.shape

# Thompson Sampling

N = 10000  # 10.000 users
a = 10  # there are 10 ads type in total
# Ni⁰(n) -> the number of times '1' arrives so far
# Ni¹(n) -> the number of times '1' arrives so far
total_reward = 0  # sum of rewards
chosen_ads = []  # an empty list created for choosed ads
ones = [0] * a  # '1' as a reward from each ad
zeros = [0] * a  # '0' as a reward from each ad

for n in range(1, N):  # Outer loop that allows us to navigate rows
    chosen_ad = 0
    max_beta = 0
    for i in range(0, a):  # Inner loop that allows us to navigate columns
        random_beta = random.betavariate(ones[i] + 1,
                                         zeros[i] + 1)  # Creating random beta by giving α(alpha) and β values
        if random_beta > max_beta:
            max_beta = random_beta  # Max_beta is constantly updated, if a value greater than itself, it changes.
            chosen_ad = i  # We add which ad we clicked for each line to the selected ads
    chosen_ads.append(chosen_ad)  # We add whichever ad we choose in each row to the selected ads list
    reward = df.values[n, chosen_ad]  # If n. chosed ad data in row=1, reward=1. otherwise 0
    if reward == 1:
        ones[chosen_ad] = ones[chosen_ad] + 1  # When the reward is 1, increase the reward of the corresponding ad by 1.
    else:
        zeros[chosen_ad] = zeros[
                               chosen_ad] + 1  # When the reward is 1, increase the value of the corresponding ad in the ones list by 1.
    total_reward = total_reward + reward  # Add the reward resulting from the operation performed on each row of the dataset to the total reward.

print('\033[1m' + f'Total Reward: {total_reward}')

# True Clicks of Ads

true_clicks = []
for i in range(0, 10):
    true_clicks.append(sum(df.iloc[:, i:i + 1].values))

true_clicks = [int(item) for item in true_clicks]

true_clicks_array = np.array(true_clicks)
true_clicks_array = true_clicks_array.reshape(1, 10)

true_clicks_df = pd.DataFrame(data=true_clicks_array, columns=df.columns, index=['Total True Clicks'])
print(true_clicks_df)


max_ad_click = true_clicks_df.values.max()
max_ad_click_name = true_clicks_df.idxmax(axis=1)[0]

sum_of_clicks = 0
for i in range(1, 10):
    sum_of_clicks = sum_of_clicks + true_clicks_df.values[0][i]

ratio = max_ad_click / sum_of_clicks

print(f'Sum of clicks                   : {sum_of_clicks}')
print(f'The name of the most clicked ad : {max_ad_click_name}')
print(f'The ratio of {max_ad_click_name} to all clicks : {ratio:.2f}\n')


# Let's show the number of clicks with a graph.

plt.figure(figsize = (12,8), facecolor='#9DF08E')
plt.bar(x=df.columns, height=true_clicks, color=sns.color_palette('bright'))
plt.title('True Clicks on Ads\n', fontsize=30, color='red')
plt.xlabel('\nAds', fontsize=20, color='black')
plt.ylabel('Clicks\n', fontsize=20, color='black')
plt.xticks(horizontalalignment='center', fontsize='15', color='black')
plt.yticks(fontsize='15', color='black')
plt.tight_layout()
plt.show()

# Chosens of Thompson Sampling

number_of_chosens = []
for i in range(0, 10):
    number_of_chosens.append(chosen_ads.count(i))

number_of_chosens_arr = np.array(number_of_chosens)
number_of_chosens_arr = number_of_chosens_arr.reshape(1, 10)

number_of_chosens_df = pd.DataFrame(data=number_of_chosens_arr, columns=df.columns, index=['Number of Chosens'])
print(number_of_chosens_df)


plt.figure(figsize = (12,8),facecolor='#9DF08E')
plt.bar(x=df.columns, height=number_of_chosens, color=sns.color_palette('bright'))
plt.title('Number of Choices\n', fontsize=30, color='red')
plt.xlabel('\nAds', fontsize=20, color='black')
plt.ylabel('Clicks\n', fontsize=20, color='black')
plt.xticks(horizontalalignment='center', fontsize='15', color='black')
plt.yticks(np.arange(0,10001,2000),fontsize='15', color='black')
plt.tight_layout()
plt.show()

# Let's remember the total reward again
print('\033[1m' + f'Total Reward: {total_reward}')
