from score import score
import json
from pathlib import Path

historyfile = Path("history.json")

if historyfile.exists():
    with open(historyfile, "r") as f:
        history = json.load(f)
else:
    history = []
    
def save_history(text, result):
    history.append({"text": text, "score": result})
    with open(historyfile, "w") as f:
        json.dump(history, f, indent=2)
        
        
        
def sentiment_label(score):
    ranges = [(0.8,  "Very Happy"), (0.5,  "Happy"), (0.2,  "Moderately Happy"), (0.1,  "A little happy"), (-0.1, "Neutral"), (-0.2, "A little Sad"), (-0.5, "Moderately Sad"), (-0.8, "Sad"),]

    for threshold, label in ranges:
        if score > threshold:
            return label
    
    return "Really Sad"


def main():
    print("Give me some text!  (Press Ctrl+C to exit)")
    while True:
        try:
            text = input("> ").strip()
            if not text:
                continue
            if len(text) > 5000:
                text = text[:5000]
            result = score(text)
            print(sentiment_label(result))
            
            #print(result)
            save_history(text, result)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
