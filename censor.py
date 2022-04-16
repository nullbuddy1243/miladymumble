import random
from better_profanity import profanity
import emoji

'''
https://pypi.org/project/better-profanity/

dirty_text = "That l3sbi4n did a very good H4ndjob."

    profanity.contains_profanity(dirty_text)

text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text, '-')
    print(censored_text)
    # You ---- of ----.
'''

# using unicode standard aliases https://www.webfx.com/tools/emoji-cheat-sheet/
def politePictures():
     
    emojiAliases = [
        ":joy:",
        ":sleeping:",
        ":innocent:",
        ":revolving_hearts:",
        ":v:",
        ":princess:",
        ":tongue:",
        ":baby_chick:",
        ":waxing_gibbous_moon:",
        ":confetti_ball:",
        ":bath:",
        ":8ball:",
        ":baby_symbol:",
        ":signal_strength:",
        ":see_no_evil:",
        ":hear_no_evil:",
        ":speak_no_evil:",
    ]
    return emojiAliases

# def tidyClean(words):
#     for e in politePictures():
        

# is a milady being rude?
def isDirty(words):
    print(f"words: {words}")
    return profanity.contains_profanity(words)

# make a milady polite
def cleanHerWords(words):
    print(f"dirty words: {words}")
    emojiAliases = politePictures()
    emojiReplace = random.choice(emojiAliases)
    politeWords = profanity.censor(words, emojiReplace)
    print(emoji.emojize('Python is :thumbsup:', language='alias'))
    politeWords = emoji.emojize(politeWords, language='alias')
    print(f"polite words: {politeWords}")
    return politeWords

