from score import score, get_most_recent_analysis
import json
from pathlib import Path
import sqlite3



DB_PATH = Path("history.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, score REAL NOT NULL, emotion TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def save_history(text, result):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO history (text, score, emotion) VALUES (?, ?, ?)", (text, result, get_most_recent_analysis()))
    conn.commit()
    conn.close()
    
    
    
    
def get_last_entries(n=3):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text, score, emotion FROM history ORDER BY id DESC LIMIT ?", (n,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_entries():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text, score, emotion FROM history ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

        
def sentiment_label(score):
    ranges = [(0.8,  "Very Positive"), (0.5,  "Positive"), (0.2,  "Moderately Positive"), (0.1,  "A little Positive"), (-0.1, "Neutral"), (-0.2, "A little Negative"), (-0.5, "Moderately Negative"), (-0.8, "Negative"),]

    for threshold, label in ranges:
        if score > threshold:
            return label
    
    return "Really Negative"
    
    
    
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
    print("Loading...")
    init_db()
    print("Welcome to the Sentiment CLI.")
    show_help()
    while True:
        try:
            cmd = input("\nCommand > ").strip().lower()
            if cmd == "1":   
                print("Enter text: ")
                text = input("> ").strip()
                if not text:
                    continue
                if len(text) > 5000:
                    text = text[:5000]
                result = safe_score(text)

                

                save_history(text, result)
            elif cmd == "2":
                rows = get_last_entries(3)
                if not rows:
                    print("No history found.")
                else:
                    print("\nLast 3 entries:")
                    for t, s, ts in rows:
                        print(f"Contextual Emotions: [{ts}]  |  Overall Mood: {sentiment_label(s)}  | Text: {t}")
                        
            elif cmd == "3":
                rows = get_all_entries()
                if not rows:
                    print("No history found.")
                else:
                    print("\nAll entries:")
                    for t, s, ts in rows:
                        print(f"Contextual Emotions: [{ts}]  |  Overall Mood: {sentiment_label(s)}  | Text: {t}")


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
