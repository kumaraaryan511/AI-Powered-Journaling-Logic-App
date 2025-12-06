from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"

import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def score(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]

    return float(probs[2] - probs[0])



text = " ".join(sys.argv[1:])
print(score(text))


