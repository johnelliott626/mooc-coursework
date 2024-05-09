#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //declare variables
    int height;
    
    //prompt user for input between 1 and 7
    do 
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    
    
    //print out # pyramid
    for (int i = 0; i < height; i++)
    {
        for(int k = (height-1); k > i ; k--)
        {
            printf(" ");
        }
        
        for(int j = 0; j <= i; j++)
        {
            printf("#");   
        }
        
        printf("\n");
       
    }
}