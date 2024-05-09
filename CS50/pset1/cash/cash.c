#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //declare variables
    float change;
    int coins = 0;
    int quarters, dimes, nickels, pennies;
    
    //prompt user for non-negative input of change amount
    do
    {
        change = get_float("Change owed: ");
    }
    while (change < 0);
    
    int cents = round(change * 100);
    
    //computes number of coins from largest to smallest
    //check quarters
    if ((cents / 25) >= 1)
    {
        quarters = (int)(cents / 25);
        coins += quarters;
        cents = cents - (25 * quarters);
    }
    
    //checks dimes
    if ((cents / 10) >= 1)
    {
        dimes = (int)(cents / 10);
        coins += dimes;
        cents = cents - (10 * dimes);
    }
    
    //checks nickels
    if ((cents / 5) >= 1)
    {
        nickels = (int)(cents / 5);
        coins += nickels;
        cents = cents - (5 * nickels);
    }
    
    //checks pennies
    if ((cents / 1) >= 1)
    {
        pennies = (int)(cents / 1);
        coins += pennies;
        cents = cents - (1 * pennies);
    }
    
    //prints number of coins
    printf("%i\n", coins);

}