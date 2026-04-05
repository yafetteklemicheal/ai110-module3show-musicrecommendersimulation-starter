# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  

- MoodBeat Recommender

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender is designed to suggest songs from a small catalog based on a users preferred genre, mood, and other attributes like energy, tempo, valence, danceability, and acousticness. It is intended for classroom exploration and prototype testing, not for production use. The model assumes the user can express a single favorite genre and mood, plus numerical targets for their desired audio feel.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The system scores each song by checking whether the songs genre and mood match the users preferences. It measures how close the songs energy, tempo, valence, danceability, and acousticness are to the users target values. Exact genre and mood matches get a boost, while numerical features are scored by distance. The final score is a weighted sum, so some features matter more than others. In this version, energy is weighted more strongly than genre, which means high-energy user profiles will favor songs with a close energy match even if the genre match is weaker.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 20 songs with a mix of genres and moods.
Genres include: pop, rock, indie, lofi, jazz, rnb, metal, edm.
Moods include: happy, chill, intense, melancholic, relaxed, party.

This dataset was expanded from the starter catalog to include more variety, but it is still small and limited. Missing or underrepresented tastes include classical, country, rap, folk, jazz, and other more niche mood categories.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The recommender works well for straightforward cases where the users preferred genre and mood both appear in the catalog. High-energy pop listeners tend to get upbeat pop songs that match both energy and mood. Chill lofi listeners tend to get low-energy, relaxed tracks. The scoring reflects intuitive tradeoffs between audio closeness and genre/mood similarity. Since the model returns an explanation for each recommendation, it is easier to inspect why a song was recommended.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The model struggles when preferences conflict or when the catalog lacks a strong genre match. It does not use user history, ratings, lyrics, artist familiarity, and song popularity. The catalog is small and underrepresents metal, jazz variants, classical, and many other music styles. The current scoring can overemphasize energy such that a high-energy user may receive a song with a good energy match even when genre is not ideal. Edge cases, like a calm listener who likes metal, can produce recommendations from more common genres because matching energy and mood outweighs genre in the current weight settings.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested the recommender using several user profiles and looked at the top ranked songs and explanations. Profiles include High-Energy Pop, Chill Lofi, Deep Intense Rock, High Energy + Sad Mood, and Calm Metal. I checked whether the top picks matched the intended mood and energy and whether the explanations aligned with the chosen songs. The biggest surprise was when I ran a test using the edge case calm metal profile received a more relaxed pop/rock song recommendations instead of metal. This shows that the current weights were not enough to maintain the users genre preferences when energy and mood were very different.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Improvements to make for future versions:

- Add more songs to cover more genres, moods, and instruments.
- Include artist, era preferences, and let users choose multiple favorite genres.
- Add playlist diversity constraints so the top recommendations are not all the same style.
- Allow users to adjust the importance of energy, genre, and mood directly.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

This exercise showed how even a simple content-based recommender can change behavior with weight choices. I also learned that even qualitative descriptions of songs are numerically represented in order to recommend better songs that fit the users preferences. I learned that mood and energy are powerful signals, but they must be balanced against genre and user preference so that the recommended songs match the users expectations. Working on this project has taught me that small datasets can make edge cases visible quickly, which is useful for debugging and improving recommendation logic, but that a larger dataset is still necessary to properly and thoroughly test the recommendation logic across many different user profiles.