# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚀 The Situation
You asked an AI to build a simple Number Guessing Game using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

## ⚙️ Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

## 📥 Document Your Experience
- **Game purpose:** A number guessing game where the player 
  guesses a number between 1 and 100 with 8 attempts. 
  Hints guide the player higher or lower after each guess.

- **Bugs found:**
  1. Hints were backwards - showed "Go LOWER!" when should say "Go HIGHER!"
  2. Attempts counter started at 1 instead of 0, showing 7 instead of 8
  3. Secret number was converted to string on even attempts

- **Fixes applied:**
  - Used GitHub Copilot to move all logic into logic_utils.py
  - Swapped hint messages in check_guess function
  - Fixed attempts initialization from 1 to 0
  - Removed string conversion bug on even attempts

## 🎮 Demo
The fixed game now correctly shows "Go HIGHER!" or "Go LOWER!" 
hints, counts attempts accurately, and compares numbers correctly.