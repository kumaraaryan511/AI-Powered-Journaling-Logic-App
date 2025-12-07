from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
from nltk.tokenize import sent_tokenize


import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)



model_name2 = "monologg/bert-base-cased-goemotions-original"
tokenizer2 = AutoTokenizer.from_pretrained(model_name2)
model2 = AutoModelForSequenceClassification.from_pretrained(model_name2)
id2label = model2.config.id2label


POSITIVE_EMOTIONS = {
    "admiration", "amusement", "approval", "caring", "confidence",
    "curiosity", "desire", "excitement", "gratitude", "joy",
    "love", "optimism", "pride", "relief", "surprise"
}

NEGATIVE_EMOTIONS = {
    "anger", "annoyance", "disappointment", "disgust", "embarrassment",
    "fear", "grief", "nervousness", "remorse", "sadness"
}



def get_most_recent_analysis():
    return most_recent_analysis

def fmt(emotions):
    parts = [f"{e.title()} — {v*100:.2f}%" for e, v in emotions]
    return " | ".join(parts)


def print_analysis(text, sentiment_score, pos_score, neg_score, top_emotions, mood_label):
    separator = "─" * 50  


    print(separator)
    print(" TEXT EMOTION ANALYSIS".center(50))
    print(separator + "\n")


    print(f" Overall Mood:        {mood_label}")
    print(f" ")
    print(f" Sentiment Score:     {pos_score*100:+.1f}% (Positive)   |   {-neg_score*100:+.1f}% (Negative)\n")


    print(" Contextual Emotions:")
    if top_emotions:
        max_name_len = max(len(e) for e, _ in top_emotions)
        for e, v in top_emotions:
            print(f"   • {e.title():<{max_name_len}} {v*100:.2f}%")
    else:
        print("   • No strong emotions detected")

    print("\n" + separator)




def score(text):
    global most_recent_analysis
    most_recent_analysis = "-"
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]

    
    sentiment_score = float(probs[2] - probs[0])


    inputs2 = tokenizer2(text, return_tensors="pt", truncation=True)
    outputs2 = model2(**inputs2)
    probs2 = torch.sigmoid(outputs2.logits)[0]

    neutral_idx = [i for i, label in id2label.items() if label == "neutral"][0]
    probs2[neutral_idx] = 0.0

    top3_idx = torch.topk(probs2, k=25).indices.tolist()
    top3_emotions = [(id2label[i], float(probs2[i])) for i in top3_idx]
    
    
    if sentiment_score > 0.2:
        filtered = [(e, v) for e, v in top3_emotions if e in POSITIVE_EMOTIONS]
        filtered = filtered[:3]  # up to 3
        most_recent_analysis = fmt(filtered)
        

    elif sentiment_score < -0.2:
        filtered = [(e, v) for e, v in top3_emotions if e in NEGATIVE_EMOTIONS]
        filtered = filtered[:3]  # up to 3
        most_recent_analysis = fmt(filtered)
        #print(fmt(filtered))

    else:
        filtered = []
        most_recent_analysis = "No strong emotions detected"
        

        

    if sentiment_score > 0.6:
        mood_label = "VERY POSITIVE"
    elif sentiment_score > 0.2:
        mood_label = "POSITIVE"
    elif sentiment_score < -0.6:
        mood_label = "VERY NEGATIVE"
    elif sentiment_score < -0.2:
        mood_label = "NEGATIVE"
    else:
        mood_label = "NEUTRAL"
    
    print_analysis(text, sentiment_score, probs[2], probs[0], filtered, mood_label)
        
    


    return float(probs[2] - probs[0])



