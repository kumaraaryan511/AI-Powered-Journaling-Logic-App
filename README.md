#  AI-Powered Journaling CLI: Palo Alto Networks Intern Challenge Submission

---

## Overview

Welcome to my submission for the **Palo Alto Networks Intern Engineer Challenge**. 

My goal is to build a robust, interpretable, and resilient **text emotion analysis tool**. Users can enter free-form text and quickly obtain:

* **Overall Mood:** Very Positive to Very Negative
* **Sentiment Score:** Positive vs. Negative probability
* **Contextual Emotions:** Top detected emotions from the text
* **Persistence:** Save entries locally in **SQLite** for historical tracking

This project focuses on performance and robustness while maintaining clean logic, readable code, reproducibility, and handling edge cases gracefully. 

---


## Background

In real-world applications, raw textual input is rarely well-structured. The tool is designed to handle linguistic ambiguity and context by addressing common challenges like mixed slang, idioms, emojis, and inconsistent grammar.

| Text Input | Expected Sentiment | Contextual Challenge |
| :--- | :--- | :--- |
| "I'm crushing it at work!" | Positive / Excited | "**Crushing**" can also be negative |
| "The workload is crushing me..." | Negative / Dissapointed | Same keyword, different context |
| "lmao that was wild 😂" | Positive / Amusement | Emoji conveys strong sentiment |

---


## Installation & Setup

Since this project relies on powerful pre-trained transformer models and platform-specific Python environments, the setup steps must be clearly defined.

### 1. Dependencies and Environment

The application requires **Python 3.10+** and several external libraries.

* `torch`: The core framework for running the model inference. I chose PyTorch for its widespread support in the academic and industrial ML community.
* `transformers`: Hugging Face's library, used to easily download and manage the pre-trained **RoBERTa** (sentiment) and **BERT** (emotion) models. This abstracts away complex model loading logic.
* `nltk`: Used here primarily for basic text processing necessities, such as tokenization.
* `sqlite3`: This is used for persistence and is part of Python's standard library (`sqlite3` module). I chose this for its **zero-dependency, self-contained nature**, making the project highly portable and resilient across different operating systems without requiring external database services.

### 2. Setup Steps

Follow these steps to set up the project locally. These commands are universal across Windows (using an Anaconda/WSL terminal), macOS, and Linux.

```bash
# 1. Clone the repository
git clone https://github.com/kumaraaryan511/AI-Powered-Journaling-Logic-App.git
cd AI-Powered-Journaling-Logic-App

# 2. Create and activate a virtual environment 
python3 -m venv venv    #SKIP IF USING WINDOWS
source venv/bin/activate  #SKIP IF USING WINDOWS

# 3. Install required packages
pip install torch transformers nltk hf-xet

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt')"

# 5. Run the app
python app.py

#NOTE: wait for the model.safetensors to load for a bit after running app.py, it may take some time

```

---

## Technical Design & Methodology

This project is built on a **dual-model architecture** to ensure both high-level mood assessment and granular emotional insight, explicitly balancing accuracy with context sensitivity.

### Sentiment Analysis

    Model: cardiffnlp/twitter-roberta-base-sentiment-latest
    
    Use: Excellent at understanding general sentiment, even during ambiguity

    Process: Tokenize → Compute softmax → Calculate Score: (Positive - Negative) → Map score to mood thresholds.
#### Justification for using RoBERTa:
I initially prototyped with **VADER (Valence Aware Dictionary and sEntiment Reasoner)**, but quickly found it failed in real-world scenarios, particularly with modern slang, emojis, and contextual ambiguities (e.g., failing to distinguish "This job is sick" from "I am sick of this job"). The RoBERTa model is **excellent at understanding general sentiment even with messy, abbreviated language**, providing a robust foundation.

### Contextual Emotion Extraction

    Model: monologg/bert-base-cased-goemotions-original
    
    Use: Good at picking up specific emotions (anger, joy, excitement), but struggles with ambiguity

    Process: Tokenize → Apply sigmoid to logits → Zero-out neutral label → Filter for top 3 strongest.

#### Justification for GoEmotions:
While I tested several other multi-label BERT models, this model, trained on the **GoEmotions dataset** (known for its fine-grained classification across 27 distinct emotion labels), consistently **outshined other models** in its ability to detect specific psychological states like *admiration*, *grief*, or *surprise*. Its strength lies in picking up specific emotions, which is useful in a journaling tool.

---
## Tests
I have included a file of test data and its resulting output in the repository. You can find it in "test_outputs.txt"

---



## Features

### 1. Overall Mood Analysis

Sentiment is calculated as **Positive probability − Negative probability** using the `cardiffnlp/twitter-roberta-base-sentiment-latest` model.

| Sentiment Score | Mood Label |
| :--- | :--- |
| > 0.6 | **VERY POSITIVE** |
| > 0.2 | **POSITIVE** |
| -0.2 → 0.2 | **NEUTRAL** |
| < -0.2 | **NEGATIVE** |
| < -0.6 | **VERY NEGATIVE** |

### 2. Contextual Emotions

Uses `monologg/bert-base-cased-goemotions-original` to detect emotions.

* Processes top 25 predicted emotions but displays only the **top 3 strongest** to avoid clutter.
* **Neutral or weak emotions are ignored.** If no strong emotions are detected, the output is: `No strong emotions detected`.
* **Positive Set:** Admiration, Amusement, Approval, Caring, Confidence, Curiosity, Desire, Excitement, Gratitude, Joy, Love, Optimism, Pride, Relief, Surprise
* **Negative Set:** Anger, Annoyance, Disappointment, Disgust, Embarrassment, Fear, Grief, Nervousness, Remorse, Sadness

### 3. Persistence + Database schema

All entries are stored in a **SQLite database** (`history.db`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique identifier for the entry. |
| `text` | TEXT NOT NULL | Raw user input text. |
| `score` | REAL NOT NULL | Calculated sentiment score. |
| `emotion` | TEXT NOT NULL | Formatted string of top emotions. |

**CLI Options for History:**

* `Show last 3 entries`: Quick recap of recent input and predictions.
* `Show all entries`: Full historical log.

### 4. User Experience (UX) Design

The CLI features clear formatting, fixed-width separators, and aligned columns for readability.

#### Example Output Formatting:

<img width="1486" height="1322" alt="image" src="https://github.com/user-attachments/assets/d3489b40-5869-401e-bf88-075162866d70" />


--- 


## Edge Case Handling

  - Empty input is ignored.

  -  Long input is truncated at 5000 characters.

  - AI model exceptions are handled with try/except blocks.

  - Invalid scores are programmatically coerced to the range [-1.0, 1.0].
    
---

## AI Usage Disclosure and code verification

In compliance with the challenge requirements regarding modern tools, I declare the following:

### Transparency
I utilized **ChatGPT** to assist with the development of this project. Specifically, it was used to:
* Generate boilerplate code for the CLI interface.
* Format the documentation structure.

### Validation & Ownership
While AI tools were used for efficiency, 
* I have manually reviewed and understood every line of code in this repository.
* I validated that no security flaws or logic bugs were introduced by the AI suggestions.
* The final architectural decisions, specifically regarding how to handle ambiguous sentiment context, were made by me.

### Verification Methodology
To ensure the integrity of the AI-generated components and the pre-trained models, I used the following verification process:
1.  **Edge Case Testing:** I manually tested ambiguous inputs (e.g., "crushing it" vs. "crushing me") to verify the sentiment analysis logic was functional.
2.  **Persistence Check:** I inspected the local `history.db` file using a SQLite viewer to confirm data was being saved and retrieved correctly.
3.  **Sanitization:** I verified that the code properly handles empty strings and excessively long inputs to prevent crashes.

    

