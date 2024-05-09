// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 676;
// Will count number of words in dictionary
int COUNT = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    bool found = false;
    int hashIndex;
    node* cursor;
    
    hashIndex = hash(word);
    
    cursor = table[hashIndex];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //
    char firstLetter;
    char secondLetter;
    int first;
    int second;
    int offset;
    int hashed;
    
    firstLetter = tolower(word[0]);
    first = (int)firstLetter;
    if (strlen(word) == 1)
    {
        firstLetter = tolower(word[0]);
        offset = first - 97;
        return (offset * 26);
    }
    
    secondLetter = tolower(word[1]);
    second = (int)secondLetter;
    
    offset = first - 97;
    hashed = (offset * 26) + (second - 97);
    
    return hashed;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //declare variables
    FILE* dictFile;
    char currentWord[LENGTH + 1];
    int hashIndex;
    
    //1. Open Dictionary file
    //Opens file, checks if return value is NULL
    dictFile = fopen(dictionary, "r");
    if (dictFile == NULL)
    {
        return false;
    }
    
    //2. Read strings from file one at a time
    while (fscanf(dictFile, "%s", currentWord) != EOF)  //scans file until it reaches the end
    {
        
        //3. Create a new node for each word
        node* n = malloc(sizeof(node));
        //check that malloc did not return NULL
        if (n == NULL)
        {
            return false;
        }
        //copy the current word into the new node
        strcpy(n->word, currentWord);
        n->next = NULL;
        
        //4. Hash word to obtain a hash value
        hashIndex = hash(currentWord);
        
        
        //5. Insert node into hash table at that index's linked list
        //if currentWord is the first word placed in its bucket
        if (table[hashIndex] == NULL)
        {
            table[hashIndex] = n;
        }
        else    //else insert the newest node at the beginning of its linked list
        {
            n->next = table[hashIndex];
            table[hashIndex] = n;
        }
        COUNT++;
    }
    
    //close file and return true
    fclose(dictFile);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return COUNT;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    node* temp;
    node* cursor;
    
    for (int i = 0;  i < N; i++)
    {
        if (table[i] != NULL)
        {
            cursor = table[i];
            temp = cursor;
            while (cursor->next != NULL)
            {
                cursor = cursor->next;
                free(temp);
                temp = cursor;
            }
            free(cursor);
        }
    }
    return true;
}
