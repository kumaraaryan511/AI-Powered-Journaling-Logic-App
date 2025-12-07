from score import score
import json
from pathlib import Path
import sqlite3
from datetime import datetime


DB_PATH = Path("history.db")


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
    
    
def get_last_entries(n=3):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text, score FROM history ORDER BY id DESC LIMIT ?", (n,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_entries():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text, score, timestamp FROM history ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

        
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
    
    
    
    
def show_help():
    print("""
Available Commands:
  1      Enter text and get mood analysis
  2      Show last 3 entries
  3      Show all entries
  help   Show this help menu
  exit   Quit the program
""")




def main():
    init_db()
    print("Welcome to the Sentiment CLI.")
    show_help()
    while True:
        try:
            cmd = input("\nCommand > ").strip().lower()
            if cmd == "1":   
                text = input("> ").strip()
                if not text:
                    continue
                if len(text) > 5000:
                    text = text[:5000]
                result = safe_score(text)
                print(sentiment_label(result))
                
                #print(result)
                save_history(text, result)
            elif cmd == "2":
                rows = get_last_entries(3)
                if not rows:
                    print("No history found.")
                else:
                    print("\nLast 3 entries:")
                    for t, s in rows:
                        print(f"Mood: {sentiment_label(s)}  | Text: {t}")
                        
            elif cmd == "3":
                rows = get_all_entries()
                if not rows:
                    print("No history found.")
                else:
                    print("\nAll entries:")
                    for t, s, ts in rows:
                        print(f"Timestamp: [{ts}]  |  Mood: {sentiment_label(s)}  | Text: {t}")


            elif cmd == "exit":
                print("bye!")
                break
                
            else:
                show_help()

            
            
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
