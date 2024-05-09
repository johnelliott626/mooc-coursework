//Author: John Elliott
//Class: CS50 pset2 readability
//Purpose: This program determines the U.S. grade reading level of a text.

//Header files included
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

//prototypes of functions
int countLetters(string textInput);
int countWords(string textInput);
int countSentences(string textInput);
int gradeLevel(int numLetters, int numWords, int numSentences);
void printGrade(int grade);

//main function
int main(void)
{
    string textInput = get_string("Text: ");
    int numLetters = countLetters(textInput);
    int numWords = countWords(textInput);
    int numSentences = countSentences(textInput);
    int gradeReadingLevel = gradeLevel(numLetters, numWords, numSentences);

    printGrade(gradeReadingLevel);

}



//this function counts all of the uppercase and lowercase letters in a string
//by first checking if it an upper or lowercase char and then adds to a counter.
int countLetters(string textInput)
{
    int n = strlen(textInput); //length of input string
    int numOfLetters = 0; //letter counter to return

    for (int i = 0; i < n; i++) //iterates through string
    {
        if (isalpha(textInput[i])) //checks if each char in string is an alphabet char
        {
            numOfLetters += 1;
        }
    }

    return numOfLetters;

}


//this function counts and returns the number of words in the input string.
int countWords(string textInput)
{
    int n = strlen(textInput);
    int numOfWords = 0;

    if (isalpha(textInput[0])) //count the initial word
    {
        numOfWords += 1;
    }

    for (int i = 0; i < n; i++)
    {
        if (textInput[i] == ' ' && isalpha(textInput[i + 1])) //counts all proceeding words
        {
            numOfWords += 1;
        }
    }

    return numOfWords;
}


//this function counts and returns the number of sentences in the input string.
int countSentences(string textInput)
{
    int n = strlen(textInput);
    int numOfSentences = 0;

    for (int i = 0; i < n; i++)
    {
        if (textInput[i] == '.' || textInput[i] == '!' || textInput[i] == '?')
        {
            numOfSentences += 1;
        }
    }

    return numOfSentences;
}

//this function calculates the Coleman-Liau index to and thus returns
// the approprate grade level of the text
int gradeLevel(int numLetters, int numWords, int numSentences)
{
    //convert ints to doubles
    double letters = (double)numLetters;
    double words = (double)numWords;
    double sentences = (double)numSentences;

    //calculate averages per 100 words
    double avgLetters = (letters / words) * 100.00;
    double avgSentences = (sentences / words) * 100.00;

    //calculate index value
    int gradeIndex = round(0.0588 * avgLetters - 0.296 * avgSentences - 15.8);

    return gradeIndex;

}

//This function outputs the gradelevel.
void printGrade(int grade)
{
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

}