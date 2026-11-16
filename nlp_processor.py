"""
Project: 06_Social_Media_Analytics_Dashboard_with_Python_Scrap
Module: nlp_processor.py
Author: Rajneesh Chaubey (ABES Engineering College)
GitHub: https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap
Description: Natural Language Processing (NLP) pipeline for cleaning, tokenization,
             hashtag/mention extraction, and sentiment polarity analysis.
"""

import re
import string

class NLPProcessor:
    def __init__(self):
        # Lexicon-based polarity keywords for resilient sentiment calculation
        self.positive_lexicon = {
            'excited', 'innovation', 'launch', 'award', 'grateful', 'optimized', 'reduced',
            'efficient', 'breakthrough', 'success', 'proud', 'love', 'amazing', 'brilliant',
            'great', 'excellent', 'scalable', 'secure', 'resilient', 'growth', 'improved'
        }
        self.negative_lexicon = {
            'vulnerability', 'downtime', 'frustrated', 'critical', 'challenging', 'bug',
            'fail', 'error', 'outage', 'unreliable', 'bad', 'poor', 'terrible', 'slow',
            'deprecated', 'latency', 'hack', 'breach', 'zero-day', 'broken', 'issue'
        }

    def clean_text(self, text: str) -> str:
        """Strips URLs, user mentions, hashtags, special characters, and emojis."""
        if not text:
            return ""
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove mentions & hashtags symbols
        text = re.sub(r'[@#]\w+', '', text)
        # Lowercase
        text = text.lower()
        # Remove punctuation & numbers
        text = re.sub(r'[^a-z\s]', '', text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def analyze_sentiment(self, text: str):
        """
        Computes polarity score (-1.0 to 1.0), qualitative category, and subjectivity.
        """
        cleaned = self.clean_text(text)
        words = cleaned.split()
        if not words:
            return 0.0, "Neutral", 0.0

        pos_count = sum(1 for w in words if w in self.positive_lexicon)
        neg_count = sum(1 for w in words if w in self.negative_lexicon)

        total_sentiment_words = pos_count + neg_count
        if total_sentiment_words == 0:
            score = 0.05  # baseline neutral-positive
        else:
            score = (pos_count - neg_count) / max(1, total_sentiment_words)
            # Bound strictly between -1.0 and 1.0
            score = max(-1.0, min(1.0, score))

        if score > 0.15:
            category = "Positive"
        elif score < -0.15:
            category = "Negative"
        else:
            category = "Neutral"

        subjectivity = min(1.0, (total_sentiment_words / len(words)) * 2.5 + 0.25)
        return score, category, subjectivity

    def extract_hashtags(self, text: str):
        """Extracts all hashtags from raw post text."""
        return re.findall(r'#\w+', text)

    def extract_mentions(self, text: str):
        """Extracts all mentions from raw post text."""
        return re.findall(r'@\w+', text)

if __name__ == "__main__":
    nlp = NLPProcessor()
    sample = "Excited to launch our new automated data pipeline! Reduced deploy times by 65%. #DevOps"
    cleaned = nlp.clean_text(sample)
    score, cat, subj = nlp.analyze_sentiment(sample)
    print("Sample:", sample)
    print("Cleaned:", cleaned)
    print(f"Sentiment: {cat} (Score: {score:.2f}, Subj: {subj:.2f})")
