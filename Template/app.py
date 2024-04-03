from flask import Flask, render_template, request
from textblob import TextBlob
from wordcloud import WordCloud
from io import BytesIO
import base64

app = Flask(__name__,template)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        lyrics = request.form['lyrics']

        # Perform Sentiment Analysis
        sentiment_score = TextBlob(lyrics).sentiment.polarity
        sentiment = 'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'

        # Generate Word Cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)

        # Save Word Cloud as base64 encoded image
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_data = base64.b64encode(img_buffer.getvalue()).decode()

        return render_template('result.html', sentiment=sentiment, img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True)
