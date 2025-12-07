from score import score
import json
from pathlib import Path
import sqlite3
from datetime import datetime



#historyfile = Path("history.json")

DB_PATH = Path("history.db")

#if historyfile.exists():
#    with open(historyfile, "r") as f:
#        history = json.load(f)
#else:
#    history = []



def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, score REAL NOT NULL, timestamp TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def save_history(text, result):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO history (text, score, timestamp) VALUES (?, ?, ?)", (text, result, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    
#def save_history(text, result):
#    history.append({"text": text, "score": result})
#    with open(historyfile, "w") as f:
#        json.dump(history, f, indent=2)
        
        
        
def sentiment_label(score):
    ranges = [(0.8,  "Very Happy"), (0.5,  "Happy"), (0.2,  "Moderately Happy"), (0.1,  "A little happy"), (-0.1, "Neutral"), (-0.2, "A little Sad"), (-0.5, "Moderately Sad"), (-0.8, "Sad"),]

    for threshold, label in ranges:
        if score > threshold:
            return label
    
    return "Really Sad"
    
def safe_score(text):

    try:
        r = score(text)
    except Exception:
        return 0.0
    
    if not isinstance(r, (float, int)):
        return 0.0
    
    if r != r:
        return 0.0
    
    return max(min(float(r), 1.0), -1.0)


def main():
    init_db()
    print("Give me some text!  (Press Ctrl+C to exit)")
    while True:
        try:
            text = input("> ").strip()
            if not text:
                continue
            if len(text) > 5000:
                text = text[:5000]
            result = safe_score(text)
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
