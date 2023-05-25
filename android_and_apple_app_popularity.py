#!/usr/bin/env python
# coding: utf-8

# # App Popularity Analysis

# In this project, our primary goal is to identify profitable mobile app profiles within both the Apple App Store and Google Play markets. Playing the role of a data analyst for a company that designs and builds mobile applications for iOS and Android platforms, our responsibility is to empower our development team with data-driven decision-making capabilities regarding the types of applications they should be focusing on.
# 
# Our organization develops free apps only. The principal revenue stream is derived from in-app advertisements. Therefore, the aim of this project is to analyze pertinent data to provide the business with a clearer understanding of what type of apps are more likely to draw in more users to see and interact with ads. This understanding will ultimately guide our development strategies and lead to more profitable applications.

# ### 1. Exploration

# In[1]:


from csv import reader

# open and read Applie and Android app data from 
#https://dq-content.s3.amazonaws.com/350/googleplaystore.csv
#and https://dq-content.s3.amazonaws.com/350/AppleStore.csv

with open('AppleStore.csv') as f:
    read_file = reader(f)
    apple = list(read_file)
    apple_header = apple[0]
    apple = apple[1:]
    
with open('googleplaystore.csv') as f:
    read_file = reader(f)
    android = list(read_file)
    android_header = android[0]
    android = android[1:]


# In[2]:


# define data exploration function

def explore_data(dataset, header, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') 
    
    print(header)
    print('\n')
    
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


# explore Apple data

explore_data(apple, apple_header, 0, 3, True)


# In[4]:


# explore Android data

explore_data(android, android_header, 0, 3, True)


# ## 2. Cleaning

# First, check for apps with missings values and delete those records

# In[5]:


def delete_missing_data(dataset, header, dataset_name):
    # delete rows with missing values  
    indices_to_delete = []
    
    dataset_clean = dataset.copy()
    
    for row in dataset_clean:
        if len(row) != len(header):
            indices_to_delete.append(dataset_clean.index(row))
    
    for index in sorted(indices_to_delete, reverse=True):
        del dataset_clean[index]
        
    print(f'Number of records in dataset {dataset_name}: {len(dataset)}')    
    print(f'Number of records in clean dataset (without missing values): {len(dataset_clean)}')
    
    return dataset_clean


# Next, check for duplicate app records and keep only the record with the highest number of ratings

# #### Check for duplicated records

# In[6]:


# check for duplicate records in each dataset

# create empty lists for unique and duplicate app records
# android
app_list = []
dup_app_list = []

for row in android:
    name = row[0]

    if name in app_list:
        dup_app_list.append(name)
    else:
        app_list.append(name)
    
print(f'Number of Anroid unique apps: {len(app_list)}')
print(f'Number of Anroid duplicate apps: {len(dup_app_list)}')

# apple
app_list = []
dup_app_list = []

for row in apple:
    name = row[0]
    
    if name in app_list:
        dup_app_list.append(name)
    else:
        app_list.append(name)

print(f'Number of Apple unique apps: {len(app_list)}')
print(f'Number of Apple duplicate apps: {len(dup_app_list)}')


# #### This function will return a dictionary with only unique app reviews

# In[7]:


def remove_dup_records(dataset, dataset_name):
    # since apple has no duplicates, we will not modify this dataset
    if dataset_name == 'apple':
        return dataset
    
    else:
        # create empty dict for holding max rating per app name
        reviews_max = {}

        # store max number of reviews per app name in dict
        for row in dataset:
            name = row[0]
            n_reviews = float(row[3])

            if name in reviews_max and reviews_max[name] < n_reviews:
                reviews_max[name] = n_reviews
            elif name not in reviews_max:
                reviews_max[name] = n_reviews
            else:
                pass

        # create empty lists to hold rows for clean dataset and names of reviews already added
        dataset_clean = []
        already_added = []
        
        for row in dataset:
            name = row[0]
            n_reviews = float(row[3])
            
            if name in reviews_max and name not in already_added:
                dataset_clean.append(row)
                already_added.append(name)
            

        print(f'Number of duplicate records deleted {dataset_name}: {len(dataset) - len(dataset_clean)}')
        print(f'Number of records in clean dataset (unique) {dataset_name}: {len(dataset_clean)}')
        
        return dataset_clean


# After removing duplicates, remove non-English app reviews

# #### Define function to check if the name of an app is in English

# In[8]:


def check_language(string):
    # initialize counter
    count = 0
    
    # count number of non-English characters
    for char in string:
        # 127 is max number for English text per ASCII
        if ord(char) > 127:
            count += 1
            
    #if there are at least 3 non-English characters, set to False      
    if count > 3:
        return False
    else:
        return True       
            


# #### Define function to filter dataset to only English apps

# In[9]:


def filter_language(dataset, dataset_name):
    # create empty list to hold only English apps
    dataset_clean = []
    
    # loop through each app in android, if app is English add to cleaned dataset list
    if dataset_name == 'android':
        for row in dataset:
            name = row[0]
            check = check_language(name)
            if check:
                dataset_clean.append(row)
            else:
                pass
            
    # loop through each app in apple, if app is English add to cleaned dataset list
    elif dataset_name == 'apple':
        for row in dataset:
            name = row[1]
            check = check_language(name)
            if check:
                dataset_clean.append(row)
            else:
                pass
        
    print(f'Number of non-English records deleted {dataset_name}: {len(dataset) - len(dataset_clean)}')
    print(f'Number of records in clean dataset (English) {dataset_name}: {len(dataset_clean)}')   
    
    return dataset_clean


# Finally, after removing non-English apps, remove non-free apps

# #### Define Function to filter only free apps

# In[10]:


def filter_free(dataset, dataset_name):
    # create empty list to hold only free apps
    dataset_clean = []
    
    # loop through each app in android, if app is free add to cleaned dataset list
    if dataset_name == 'android':
        for row in dataset:
            price = row[7]
            if price == '0':
                dataset_clean.append(row)
                
    # loop through each app in apple, if app is free add to cleaned dataset list         
    if dataset_name == 'apple':
        for row in dataset:
            price = row[4]
            if price == '0.0':
                dataset_clean.append(row)
                
                
    print(f'Number of non-free records deleted {dataset_name}: {len(dataset) - len(dataset_clean)}')
    print(f'Number of records in clean dataset (free) {dataset_name}: {len(dataset_clean)}')   
    
    return dataset_clean


# ### Combine all cleaning steps in one cleaning function and call the function on the raw datasets

# In[11]:


def all_cleaning(dataset, header, dataset_name):
    dataset = delete_missing_data(dataset, header, dataset_name)
    dataset = remove_dup_records(dataset, dataset_name)
    dataset = filter_language(dataset, dataset_name)
    dataset = filter_free(dataset, dataset_name)
    return dataset

android = all_cleaning(android, android_header, 'android')
apple = all_cleaning(apple, apple_header, 'apple')


# In[12]:


android


# ## 3. Analysis

# As mentioned, the goal is to determine the types of apps which are likely to attract more users, and therefore generate more revenue from in-app advertisements.
# 
# To minimize risks and overhead, the validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we develop it further.
# 3. If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets.

# The first step will be to identify the most common genres for each market.

# #### Identify columns of interest and indexes - Category and Genres for Android, prime_genre for Apple

# In[13]:


print(android_header)
print('\n')
print(apple_header)


# #### Define function to create freq tables

# In[14]:


def freq_table(dataset, index):
    # create empty dict to hold freqs
    freqs = {}
    
    # loop through apps and populate dictionary with freqs
    for row in dataset:
        if row[index] in freqs:
            freqs[row[index]] += 1
        else:
            freqs[row[index]] = 1
            
    for key in freqs:
        freqs[key] = round(freqs[key] / len(dataset), 2)
    
    return freqs


# #### Define function to display sorted freq tables

# In[15]:


def display_table(dataset, index):
    
    #call freq_table() function
    table = freq_table(dataset, index)
    
    # create empty list to display table
    table_display = []
    
    # add tuple of key val pairs to display table
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
    
    # sort the display table from highest to lowest freqs
    table_sorted = sorted(table_display, reverse = True)
    
    #print the keys and freqs from the sorted display table
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# What are the most common app genres/categories? 

# In[16]:


display_table(apple, 11)


# Looking at the Apple App Store apps, it's obvious that games dominate the market. After a significant gap, Entertainment ranks as the second most common genre, and Photo and Video ranks third just behind Entertainment.

# In[17]:


display_table(android, 1)


# In[18]:


display_table(android, 9)


# Looking at Android Apps, Family, Games, Entertainment, and Tools app categories/genres are most popular. However, the most popular categories/genres do not lead by a large margin. In general, it appears there is a balance between entertainment and productivity apps.

# Next, we'll look at popularity of the individual apps within the genres.

# In[19]:


apple_freq_table = freq_table(apple, 11)

apple_app_popularity = []

for genre in apple_freq_table:
    total = 0
    len_genre = 0
    for row in apple:
        genre_app = row[11]
        if genre_app == genre:
            rating_count = float(row[5])
            total += rating_count
            len_genre += 1
    average_ratings = int(total / len_genre)
    apple_app_popularity.append((genre, average_ratings))

sorted(apple_app_popularity, key = lambda x: x[1], reverse = True)


# We can now see the most popular app genres by total number of user reviews for apps in that genre. This doesn't tell the full story, however. There are likely a few specific apps in the Navigation and Social Networking genres, and it may not make sense to attempt to build a similar app. 

# In[20]:


nav_dict = {}

for row in apple:
    if row[11] == 'Navigation':
        nav_dict[row[1]] = float(row[5])
        
social_network_dict = {}

for row in apple:
    if row[11] == 'Social Networking':
        social_network_dict[row[1]] = float(row[5])
    
reference_dict = {}

for row in apple:
    if row[11] == 'Reference':
        reference_dict[row[1]] = float(row[5])    

    
print(nav_dict)
print('\n')
print(social_network_dict)
print('\n')
print(reference_dict)


# The Navigation genre would not make sense and already has its market leaders clearly established. The Social Networking genre is also dominated by a few apps, but there are some niche audiences and perhaps this is a viable option. The Reference genre also has some room for apps designed for niche audiences.

# Finally, looking at the most common app genres for android apps.

# In[21]:


android_freq_table = freq_table(android, 1)

android_app_popularity = []

for category in android_freq_table:
    total = 0
    len_category = 0
    for row in android:
        category_app = row[1]
        if category_app == category:
            installs = float(row[5].replace('+', '').replace(',',''))
            total += installs
            len_category += 1
    avg_install = int(total / len_category)
    android_app_popularity.append((category, avg_install))
    
sorted(android_app_popularity, key = lambda x: x[1], reverse = True)


# Analyzing apps in a few of these categories in the same manner:

# In[22]:


comm_dict = {}

for row in android:
    if row[1] == 'COMMUNICATION':
        comm_dict[row[0]] = float(row[5].replace('+', '').replace(',',''))
 
entertainment_dict = {}

for row in android:
    if row[1] == 'ENTERTAINMENT':
        entertainment_dict[row[0]] = float(row[5].replace('+', '').replace(',',''))
        
books_dict = {}

for row in android:
    if row[1] == 'BOOKS_AND_REFERENCE':
        books_dict[row[0]] = float(row[5].replace('+', '').replace(',',''))
    
print(comm_dict)
print('\n')
print(entertainment_dict)
print('\n')
print(books_dict)


# Perhaps there is some room for new entertainment apps, as there is a very wide range of possibilities and a wide range of interests. We could find a niche here. 

# Books and References are also popular in Apple apps. This could be our starting point. Is there a market for a reference guide on a specific topic that has not yet been saturated with alternatives?

# ## 4. Conclusion
# 
# We have cleaned data about apps in both the Android and Apple Stores, analyzed that data to identify which app categories are most popular for users, and dug a bit deeper to examine which categories are already dominated by a few key players, and which may present some opportunities for us to create a unique app filling a need for a specific audience or covering a specific topic. 
