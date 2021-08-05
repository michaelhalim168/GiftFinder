import numpy as np
import pandas as pd
import praw

class Reddit:
    
    '''
    Class used to scrape top posts from specified subreddits.
    '''
    
    def __init__(self, username, password, client_id, secret_key, user_agent):
        
        '''
        -Initialize username, password, client-id, api key, and user agent
        -Generate Reddit instance using PRAW
        -Setup Dataframe to store scraped Reddit information
        -Create list to store comments 
        '''
        
        self.username = username
        self.password = password
        self.client_id = client_id
        self.secret_key = secret_key
        self.user_agent = user_agent
        
        self.reddit = praw.Reddit(username=self.username, password=self.password, client_id=self.client_id,
                                 client_secret= self.secret_key, user_agent = self.user_agent)
        
        self.posts = pd.DataFrame(columns=['title', 'score', 'id', 'subreddit', 'url',
                                     'num_comments', 'body', 'created', 'category'])
        
        self.comments = list()
        
    def get_posts(self, category, subreddit_list):
        
        '''
        Input: 
            - category: name of category/topic (ex. electronics, nature, travel, etc.)
            - subreddit_list: list of subreddits
        Output:
            - stores title, score, id, subreddit name, url, number of comments, text, and date of post from 
            specified subreddit into self.posts Dataframe
        '''
        
        posts = list()
        
        for sub in subreddit_list:
            try:
                subreddit = self.reddit.subreddit(sub)
            except:
                print('Error in subreddit search.')
            else:
                for post in subreddit.hot(limit=500):
                    posts.append([post.title, post.score, post.id, post.subreddit,
                                 post.url, post.num_comments, post.selftext, post.created, category])
                df = pd.DataFrame(posts, columns=self.posts.columns)
                self.posts = pd.concat([self.posts, df])
                
        self.posts.drop_duplicates(inplace=True)
    
    def get_comments(self, df):  
        for row in df.iterrows():
            submission = self.reddit.submission(id=row[1]['id'])
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                self.comments.append(comment.body)
                
        df['comments'] = self.comments
        return df