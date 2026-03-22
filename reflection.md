# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.


## 1. What was broken when you started?

**Bug 1: Wrong hint direction**
- Expected: When I guessed 10 and the secret number was 86, 
  it should say "Go HIGHER!"
- Actual: It said "Go LOWER!" — the hints are completely backwards.

**Bug 2: Attempts count mismatch**
- Expected: Sidebar and game should both show 8 attempts.
- Actual: Sidebar says 8 but game shows 7 from the start.

**Bug 3: Score stays at 0**
- Expected: Score should update when guessing.
- Actual: Score stays at 0 no matter what.
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

---

## 2. How did you use AI as a teammate?

**Correct AI suggestion:**
- Copilot correctly swapped the hint messages in check_guess.
  When guess > secret it now says "Go LOWER!" and when 
  guess < secret it says "Go HIGHER!". I verified this by 
  guessing 10 and seeing "Go HIGHER!" in the live game.

**Another correct suggestion:**
- Copilot fixed attempts starting at 1 instead of 0, and 
  removed the string conversion bug on even attempts.
  I verified by checking attempts left now shows 8 correctly.

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
**AI tools used:**
- GitHub Copilot (in VS Code)
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
**Correct AI suggestion:**
- I asked Copilot to fix the hint direction bug in check_guess. 
  Copilot correctly identified that "Go HIGHER!" and "Go LOWER!" 
  were swapped and fixed them. I verified it by guessing 10 when 
  the secret number was higher, and the game correctly showed 
  "Go HIGHER!" instead of the wrong "Go LOWER!" it showed before.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
**Incorrect or misleading AI suggestion:**
- When Copilot tried to run pytest to verify the fixes, it tried 
  multiple commands (python, python3, python3.13) because Python 
  was not on PATH. Copilot assumed Python would be accessible 
  normally but it wasn't. I had to manually use the full Python 
  path to run commands instead of the simple ones Copilot suggested
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

**How did I decide whether a bug was really fixed?**
- I ran the Streamlit app and manually tested each bug by 
  playing the game with specific inputs to confirm the 
  expected behavior matched the actual behavior.

- Describe at least one test you ran (manual or using pytest)  
Manual test 1 - Hint direction:
- Guessed 10 when secret number was higher.
- Before fix: showed "Go LOWER!" (wrong)
- After fix: showed "Go HIGHER!" (correct)
Manual test 2 - Attempts count:
- Started a new game and checked attempts left.
- Before fix: showed 7 instead of 8 (off by one)
- After fix: correctly showed 8 attempts left.

Manual test 3 - String conversion bug:
- Played multiple rounds to test even and odd attempts.
- Before fix: wrong comparisons on even attempts caused 
  incorrect outcomes.
- After fix: all attempts compared correctly as integers.

  and what it showed you about your code.

- Did AI help you design or understand any tests? How?
 Copilot automatically ran pytest after making the fixes 
  to verify the existing tests still passed. This helped 
  confirm that the refactoring did not break any existing 
  functionality while fixing the bugs

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

<!-- - What is one habit or strategy from this project that you want to reuse in future labs or projects? -->
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
