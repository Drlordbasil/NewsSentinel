import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.summarization import summarize
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class NewsAggregator:
    def __init__(self):
        self.sources = ['https://example.com/source1', 'https://example.com/source2', 'https://example.com/source3']
    
    def scrape_articles(self):
        articles = []
        
        for source in self.sources:
            response = requests.get(source)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            news_articles = soup.find_all('article')
            
            for article in news_articles:
                title = article.find('h2').text.strip()
                content = article.find('div', class_='content').text.strip()
                
                articles.append({
                    'title': title,
                    'content': content
                })
        
        return articles
    
    def analyze_sentiment(self, articles):
        stop_words = set(stopwords.words('english'))
        sia = SentimentIntensityAnalyzer()
        
        for article in articles:
            content = article['content']
            
            # Tokenize the content
            words = word_tokenize(content.lower())
            
            # Remove stopwords
            words = [word for word in words if word not in stop_words]
            
            # Calculate sentiment scores for each sentence
            sentiment_scores = []
            sentences = sent_tokenize(content)
            for sentence in sentences:
                sentiment_scores.append(sia.polarity_scores(sentence)['compound'])

            # Calculate average sentiment score
            if sentiment_scores:
                average_score = sum(sentiment_scores) / len(sentiment_scores)
                article['sentiment_score'] = average_score
            else:
                article['sentiment_score'] = 0.0
    
    def generate_summaries(self, articles):
        for article in articles:
            content = article['content']
            
            # Generate summary
            summary = summarize(content)
            
            article['summary'] = summary
    
    def display_articles(self, articles):
        for i, article in enumerate(articles, 1):
            print(f'Article {i}:')
            print(f'Title: {article["title"]}')
            print(f'Summary: {article["summary"]}')
            print(f'Sentiment Score: {article["sentiment_score"]}')
            print('---')
    
    def send_email_notification(self, email, topic, articles):
        sender = 'sender@example.com'
        receiver = email
        subject = f'News Articles on {topic}'
        
        message = f'Here are some news articles on {topic}:\n\n'

        for i, article in enumerate(articles, 1):
            message += f'Article {i}:\n'
            message += f'Title: {article["title"]}\n'
            message += f'Summary: {article["summary"]}\n'
            message += f'Sentiment Score: {article["sentiment_score"]}\n'
            message += '---\n'

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.sendmail(sender, receiver, msg.as_string())
    
    def generate_sentiment_trends(self, articles):
        scores = []
        
        for article in articles:
            scores.append(article['sentiment_score'])
        
        plt.plot(scores)
        plt.xlabel('Article')
        plt.ylabel('Sentiment Score')
        plt.title('Sentiment Trends')
        plt.show()
    
    def generate_sentiment_comparison(self, articles):
        titles = []
        scores = []
        
        for article in articles:
            titles.append(article['title'])
            scores.append(article['sentiment_score'])
        
        fig = go.Figure(data=go.Bar(x=titles, y=scores))
        fig.update_layout(
            title='Sentiment Comparison',
            xaxis_title='Article',
            yaxis_title='Sentiment Score'
        )
        fig.show()


if __name__ == '__main__':
    news_aggregator = NewsAggregator()
    articles = news_aggregator.scrape_articles()
    news_aggregator.analyze_sentiment(articles)
    news_aggregator.generate_summaries(articles)
    news_aggregator.display_articles(articles)
    news_aggregator.send_email_notification('user@example.com', 'Python', articles)
    news_aggregator.generate_sentiment_trends(articles)
    news_aggregator.generate_sentiment_comparison(articles)