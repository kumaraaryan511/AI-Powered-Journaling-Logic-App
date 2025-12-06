import sys
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def analyze_sentence(text: str) -> float:
    if not text.strip():
        return 0.0
    lowered = text.lower()
    scores = sia.polarity_scores(text)
    return scores["compound"]
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wellbeing.py \"your text\"")
        sys.exit(1)
    sentence = " ".join(sys.argv[1:])
    score = analyze_sentence(sentence)
    print(score)
