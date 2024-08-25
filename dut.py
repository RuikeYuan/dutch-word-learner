import dutch_words

# Get the list of ranked Dutch words
ranked_words = dutch_words.get_ranked()

# Total number of words
total_words = len(ranked_words)

# Number of words per level (10% of the total)
words_per_level = total_words // 10

# Create the levels
levels = {}

for i in range(10):
    level_start = i * words_per_level
    level_end = (i + 1) * words_per_level if i < 9 else total_words
    level_number = i + 1
    levels[level_number] = ranked_words[level_start:level_end]



# Print the number of words in each level
for level, words in levels.items():
    print(f"Level {level} has {len(words)} words. First word: {words[0]} Last word: {words[-1]}")

# Optional: Print the first few words in each level for clarity
for level, words in levels.items():
    print(f"\nLevel {level} (First 5 words):")
    for item in words[:5]:
        word = item[0]  # Adjust index based on actual structure
        rank = item[1]  # Adjust index based on actual structure
        print(f"  Word: {word}, Rank: {rank}")
