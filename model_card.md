# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of it less like a model that "learns" and more like a judge that scores every song in the catalog against what you told it you like, then hands you the songs with the highest scores.

For every song, the judge looks at four things: its **genre** (pop, lofi, rock, etc.), its **mood** (happy, chill, intense, etc.), how **energetic** it is on a scale from calm to high-energy, and whether it sounds **acoustic** or more produced/electronic.

It compares each of those to what you said you wanted: your favorite genre, your favorite mood, the energy level you're in the mood for, and whether you generally prefer acoustic-leaning songs.

Each of the four comparisons earns the song some points, but not the same amount of points:
- An exact **genre** match is worth the most, since I'm treating "what kind of music you listen to" as your most stable, defining taste.
- An exact **mood** match is worth a bit less — moods shift more often than genre taste does, so it's treated as a secondary preference.
- **Energy** isn't a yes/no match — a song doesn't have to hit your exact energy level to get credit, it gets partial credit the closer it lands to what you asked for.
- The **acoustic** preference is worth the least — it's more of a tie-breaker than a core reason to recommend something.

All four point amounts get added up into one total score per song. The catalog gets sorted from highest score to lowest, and you're shown the top few. Alongside every recommendation, the system also prints out exactly which of the four things matched and how many points each one contributed, so a recommendation never just says "trust me" — it shows its work.

Starting from the starter logic, the main change was turning vague "give a bonus" placeholders into an actual weighted point recipe (genre worth more than mood, energy scored as a sliding scale rather than all-or-nothing, acoustic treated as a minor tie-breaker), plus making sure every recommendation comes with a plain-language reason attached.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
