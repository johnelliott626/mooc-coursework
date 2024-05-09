//Purpose of program

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

//Function prototypes
void encipherAndPrint(string plaintext, string key);
bool validateKey(string key);
string getPlaintext();

int main(int argc, string argv[])
{
    //check to make sure user has entered key in command line
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //converts the key to all uppercase
    string key = (argv[1]);
    for (int i = 0; i < strlen(key); i++)
    {
        key[i] = toupper(key[i]);
    }

    //calls function to see if the key is valid
    bool isKeyValid = validateKey(key);

    //if the key is valid continue program
    if (isKeyValid)
    {
        string plaintext = getPlaintext(); //get plaintext input from user.
        encipherAndPrint(plaintext, key); //encipher the plaintext and print the new enciphered text.
        return 0;
    }

    else
    {
        return 1;
    }
}

//function that checks to see if input key is valid
bool validateKey(string key)
{
    int n = strlen(key);

    //check that the key length is 26 chars
    if (n != 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }

    //check that all chars are alphabetic characters
    for (int i = 0; i < n; i++)
    {
        if (isalpha(key[i]) == 0)
        {
            printf("Key must onlu contain alphabetic characters.\n");
            return false;
        }
    }

    //check that no two chars repeat
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (key[i] == key[j] || toupper(key[i]) == key[j] || key[i] == toupper(key[j]))
            {
                printf("Key must not contain repeated characters.\n");
                return false;
            }
        }
    }

    //if all invalid tests are passed then return true
    return true;
}

//recieves plaintext input from user
string getPlaintext()
{
    string plain = get_string("plaintext: ");
    return plain;
}

//enciphers the plaintexts input and prints it out'
void encipherAndPrint(string plaintext, string key)
{


    int alphabet[26];
    for (int i = 0; i < 26; i++)
    {
        alphabet[i] = 65 + i;
    }


    int cipherAlphabet[26];
    for (int j = 0; j < 26; j++)
    {
        cipherAlphabet[j] = (int)key[j];
    }

    int cipherDiffValue[26];
    for (int k = 0; k < 26; k++)
    {
        cipherDiffValue[k] = (alphabet[k] - cipherAlphabet[k]);
    }

    int ciphertext[strlen(plaintext)];
    int alph;
    for (int b = 0; b < strlen(plaintext); b++)
    {
        if (isalpha(plaintext[b]) != 0)
        {
            for (int g = 0; g < 26; g ++)
            {
                if (toupper(plaintext[b]) == alphabet[g])
                {
                    alph = g;
                }
            }
            ciphertext[b] = ((int)plaintext[b] - cipherDiffValue[alph]);
        }

        else
        {
            ciphertext[b] = (int)plaintext[b];
        }
    }


    printf("ciphertext: ");
    for (int v = 0; v < strlen(plaintext); v++)
    {
        printf("%c", (char)ciphertext[v]);
    }
    printf("\n");


}