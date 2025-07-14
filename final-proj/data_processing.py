"""Data model used to process and extract data from Github commit messages. 

Final Project submission for Stat 198: Interactive Data Science course at UC Berkeley.

Data extracted from GH Archive: https://www.gharchive.org/. 

Author: Vy Ho
License: BSD-3-Clause
"""
import pandas as pd
from numpy import random

STOP_WORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

FILE_NAME = 'data_commit000000000000'

class DataModel: 
    """Data model that transforms CSV data to a df and allows for extraction of information."""
    def __init__(self): 
        self.df = None
        self.get_data()

    def get_data(self): 
        """Combine all csvs and create dfs."""
        self.combine_csvs((0, 1119))
        self.make_commit_counts_df()
        self.make_word_count_df()

    # DATA PREPROCESSING
    def combine_csvs(self, file_range):
        """
        file_range: tuple of the starting and ending range of the csv files to combine

        Reads csv files and adds data to a list that is then converted into one dataframe.
        Additional columns time and comment_tokenized are created in addition. 

        returns a df 
        """
        # list to contain all of the data
        data = [] 

        # iterate through csv file range
        for i in range(file_range[0], file_range[1] + 1): 
            # format file name
            num_length = len(str(i))
            file = f'commit-data/{FILE_NAME[:-num_length]}{str(i)}.csv'
            print(file)

            # get csv as df --> convert data to list --> add to data list
            curr = pd.read_csv(file, keep_default_na=False)
            df_as_lst = curr.values.tolist()
            data.extend(df_as_lst)
            
        df = pd.DataFrame(data, columns = ['time', 'repo', 'user', 'comment'])

        # remove multiline characters
        df['comment'] = df['comment'].str.replace('\n', '')
        
        # removing messages from users identified as bots based on the username
        df = df[~df['user'].str.contains('[bot]', case=False)] 

        # tokenize comments and create a day column
        df['comment_tokenized'] = df['comment'].str.lower().str.replace('[.,?!]', '', regex=True).str.split()
        df['time'] = pd.to_datetime(df['time'])
        df['day'] = df['time'].dt.day

        self.df = df
        return df
    
    def group_df(self, column): 
        """
        column: string 
        Given a column, group the main df by the columnn and returns the count of occurrences of the column.
        
        returns a df
        """
        curr = self.df.groupby(column).size().reset_index(name='count')
        return curr
    
    def make_commit_counts_df(self): 
        """
        Create df of the counts of commit messages per user.
        """
        self.user_counts = self.group_df('user').sort_values(by='count', ascending=False).reset_index()
            
    def make_word_count_df(self): 
        """
        Creates a df counting the appearances of each word's appearance across all commit messages.
        """
        # list to hold all the words
        tokenized = []

        curr = self.df['comment_tokenized'].values.tolist()
        for row in curr: 
            tokenized.extend(row)
        raw_count = pd.DataFrame(tokenized, columns=['word'])
        grouped = raw_count.groupby('word').size().reset_index(name='count')

        # removing non alphanumeric words
        word = grouped[grouped['word'].str.isalpha()]
        
        self.word_counts = word.sort_values(by='count', ascending=False)

    # DATA RETRIEVAL
    def get_top5_users(self): 
        """
        return a df with the top 5 users with the most commit messages.
        """
        return self.user_counts.iloc[:5, ]

    def get_top5_words(self): 
        """
        return a df with the top 5 words with the most frequent appearances across commit messages
        """
        filtered = self.word_counts[~self.word_counts['word'].isin(STOP_WORDS)]
        return filtered.iloc[:5, ]

    def get_commit(self, word):
        """
        word: a string

        Given a word, returns the word, a repo it was used in, the user who sent the commit message, 
        and the commit message that uses the word. If the word cannot be found it returns the word and 
        a string. The commit message returned is at random.
        """
        # filter df 
        filtered = self.df[self.df['comment_tokenized'].apply(lambda comment: word in comment)]
        
        # if there is at least one commit message that uses word
        if filtered.shape[0] > 0: 
            # randomize row returned
            k = filtered.shape[0]
            row = filtered.iloc[random.randint(0, k)]
            return word, row['repo'], row['user'], row['comment']
        return word, 'no commit message found'
    
    def get_word_count(self, word): 
        """
        word: a string
        
        Given a word return the count of commit messages that used the word. 
        """
        return self.df[self.df['comment_tokenized'].apply(lambda comment: word in comment)].shape[0]
        return self.word_counts.loc[self.word_counts['word'] == word]['count'].values[0]

    def get_user_count(self, word): 
        """
        word: a string

        Given a word return the number of users who have used the word in a commit message. 
        """
        return self.df[self.df['comment_tokenized'].apply(lambda comment: word in comment)]['user'].nunique()

    def get_word_timeline(self, word): 
        """
        word: a string

        Given a word return a df with the number of counts of a word's usage in commit messages 
        for each day of the month. 

        returns a df
        """
        # filter df
        filtered = self.df[self.df['comment_tokenized'].apply(lambda comment: word in comment)]
        
        # group by day and interpolate days of the month not included to have a count of 0
        grouped = filtered.groupby('day').size().reset_index(name='count').sort_values(by='day', ascending=True).reset_index()
        grouped = grouped.set_index('day')
        interpolated = grouped.reindex(range(1, 32), fill_value=0).sort_values(by='day', ascending=True).reset_index()
        return interpolated

    # DEPRECATED
    def get_random_commit(self): 
        """
        returns a random commit message
        """
        k = self.filtered_df.shape[0]
        return self.filtered_df.iloc[random.randint(k),]
    
    def get_top3_repo(self): 
        """
        returns a df of the top 3 repos with the most commit messages
        """
        return self.repo_counts.iloc[:3,]
