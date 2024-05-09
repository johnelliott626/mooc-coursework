from cs50 import get_string

text = get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i in text:
    if i.isalpha():
        letters += 1
    if i == " ":
        words += 1
    if i == "." or i == "!" or i == "?":
        sentences += 1

avgLetters = (letters / words) * 100.00
avgSentences = (sentences / words) * 100.00
grade = round(.0588 * avgLetters - .296 * avgSentences - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")