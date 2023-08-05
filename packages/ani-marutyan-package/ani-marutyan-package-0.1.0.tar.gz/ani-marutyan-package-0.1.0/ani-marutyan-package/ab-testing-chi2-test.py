#!/usr/bin/env python
# coding: utf-8

# # Grocery Sign-up Rate

# ### The Scenario
# 
# #### In late June, we mailed out promotional content to some of our customers for our "Delivery Club" Signing up to the club cost dollars and gave customers free grocery deliveries for one year, starting on July 1st.
# #### We wanted to see if a nicer looking mailer would get more customers to sign-up. We randomly selected 3 groups, the first group received Mailer 1, a very basic and cheap version simple outlining the deal, the second group received Mailer 2, a really nice, colourful mailer printed on cardboard, and the third group were the control group and received to mailer at all.
# #### We're very confident that the customers who were mailed, signed up at a far higher rate than the control group... but we're unsure if there is a significant difference between signup-rate for the cheaper mailer and the more expensive mailer. At first glance, there does appear to be a slightly higher sign-up rate for the expensive version but before making any conclusions we wanted you to run your eyes over the numbers.

# ### The Task
# 
# #### Assess whether there is a difference between mailer 1 and mailer 2 in terms of sign-up rate to the club

# ## Import Required Packages

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import chi2_contingency, chi2


# ## Import Data

# In[2]:


campaign_data = pd.read_excel("grocery_database.xlsx", sheet_name = "campaign_data")
campaign_data.head(5)


# In[3]:


# check shape of dataframe
campaign_data.shape


# In[4]:


# filter data
campaign_data = campaign_data.loc[campaign_data["mailer_type"] != "Control"]


# In[5]:


# check shape of updated dataframe
campaign_data.shape


# In[6]:


campaign_data.count()


# In[7]:


# check number of sign-ups
campaign_data.groupby("mailer_type")["signup_flag"].value_counts()


# In[8]:


observed_values = pd.crosstab(campaign_data["mailer_type"], campaign_data["signup_flag"]).values
observed_values


# In[9]:


# compute sign-up rate
mailer1_signup_rate = 123 / (252 + 123) 
mailer2_signup_rate = 127 / (209 + 127)
print(mailer1_signup_rate, mailer2_signup_rate)


# ## State hypotheses & set acceptance criteria

# In[10]:


null_hypothesis = "There is no relationship between mailer type and signup rate. They are independent"
alternate_hypothesis = "There is a relationship between mailer type and signup rate. They are not independent"
acceptance_criteria = 0.05


# ## Calculate expected frequencies & chi square statistic

# In[11]:


chi2_statistic, p_value, dof, expected_values = chi2_contingency(observed_values, correction = False)
print(chi2_statistic, p_value)


# In[12]:


# find the critical value for our test
critical_value = chi2.ppf(1 - acceptance_criteria, dof)
print(critical_value)


# ## Results

# #### Chi Square Statistic

# In[13]:


if chi2_statistic >= critical_value:
    print(f"As our chi-square statistic of {chi2_statistic} is higher than our critical value of {critical_value} - we reject the null hypothesis, and conclude that: {alternate_hypothesis}.")
else:
    print(f"As our chi-square statistic of {chi2_statistic} is lower than our critical value of {critical_value} - we retain the null hypothesis, and conclude that: {null_hypothesis}.")


# #### p_value

# In[14]:


if p_value <= acceptance_criteria:
    print(f"As our p_value of {p_value} is lower than our acceptance_criteria of {acceptance_criteria} - we reject the null hypothesis, and conclude that: {alternate_hypothesis}.")
else:
    print(f"As our p_value of {p_value} is higher than our acceptance_criteria of {acceptance_criteria} - we retain the null hypothesis, and conclude that: {null_hypothesis}.")


# In[ ]:




