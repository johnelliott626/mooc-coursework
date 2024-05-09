#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) //iterates through each row
    {
        for (int j = 0; j < width; j++) //iterates through each pixel in each row
        {
            int Red = image[i][j].rgbtRed;
            int Green = image[i][j].rgbtGreen;
            int Blue = image[i][j].rgbtBlue;
            float average = ((Red + Green + Blue) / 3.0);
            int intAvg = round(average);

            image[i][j].rgbtRed = intAvg;
            image[i][j].rgbtGreen = intAvg;
            image[i][j].rgbtBlue = intAvg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) //iterates through each row
    {
        for (int j = 0; j < width; j++) //iterates through each pixel in each row
        {
            //Get Each Red, Green, and Blue value of the individual pixel
            int Red = image[i][j].rgbtRed;
            int Green = image[i][j].rgbtGreen;
            int Blue = image[i][j].rgbtBlue;

            //Calculate the new Red, Green, and Blue Sepia values.
            float sepiaRed = .393 * Red + .769 * Green + .189 * Blue;
            float sepiaGreen = .349 * Red + .686 * Green + .168 * Blue;
            float sepiaBlue = .272 * Red + .534 * Green + .131 * Blue;

            //Round the floating point values and assign them to integers.
            int updateRed = round(sepiaRed);
            int updateGreen = round(sepiaGreen);
            int updateBlue = round(sepiaBlue);

            //create an array with the updated values
            int updatedValues[] = {updateRed, updateGreen, updateBlue};

            for (int k = 0; k < 3; k++)
            {
                if (updatedValues[k] > 255)
                {
                    updatedValues[k] = 255;     //changes R,G,B value to 255 if new Sepia value exceeds 255.
                }
                if (updatedValues[k] < 0)
                {
                    updatedValues[k] = 0;       //changes R,G,B value to 0 if new Sepia value is lower than 0.
                }
            }

            //sets new pixel values
            image[i][j].rgbtRed = updatedValues[0];
            image[i][j].rgbtGreen = updatedValues[1];
            image[i][j].rgbtBlue = updatedValues[2];
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int halfWidth = width / 2;

    for (int i = 0; i < height; i++) //iterates through each row
    {
        int k = (width - 1);

        for (int j = 0; j < halfWidth; j++) //iterates through each pixel in each row
        {
            //gets left pixel values
            int Red = image[i][j].rgbtRed;
            int Green = image[i][j].rgbtGreen;
            int Blue = image[i][j].rgbtBlue;

            //gets right pixel values
            int secRed = image[i][k].rgbtRed;
            int secGreen = image[i][k].rgbtGreen;
            int secBlue = image[i][k].rgbtBlue;

            //switches pixel values.
            image[i][j].rgbtRed = secRed;
            image[i][j].rgbtGreen = secGreen;
            image[i][j].rgbtBlue = secBlue;

            image[i][k].rgbtRed = Red;
            image[i][k].rgbtGreen = Green;
            image[i][k].rgbtBlue = Blue;

            k--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //make a duplicate image in a 2D array to store the updated values
    RGBTRIPLE copyPic[height][width];

    //iterate through each pixel
    for (int i = 0; i < height; i++) // each row
    {
        for (int j = 0; j < width; j++) //left to right through the row
        {
            //top left corner
            if (i == 0 && j == 0)
            {
                topLeftCorner();
            }

            //top right corner
            else if (i == 0 && j == (width - 1))
            {
                topRightCorner();
            }

            //bottom left corner
            else if (i == (height - 1) && j == 0)
            {
                bottomLeftCorner();
            }

            //bottom right corner
            else if (i == (height - 1) && j == (width - 1))
            {
                bottomRightCorner();
            }

            //top edge
            else if (i == 0 && j > 0 && j < (width - 1))
            {
                topEdge();
            }

            //right edge
            else if (i > 0 && i < (height - 1) && j == (width - 1))
            {
                rightEdge();
            }

            //bottom edge
            else if (i == (height - 1) && j > 0 && j < (width - 1))
            {
                bottomEdge();
            }

            //left edge
            else if (i > 0 && i < (height - 1) && j == 0)
            {
                leftEdge();
            }

            //everything else
            else
            {
                allSides(height, width, image, copyPic, i, j);
            }
        }
    }
    return;
}


void allSides(int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE copyPic[height][width], int i, int j)
{
    int redSum = 0;
    int greenSum = 0;
    int blueSum = 0;
    for (int k = 0; k < 3; k++)
    {
        for (int g = 0; g < 3; g++)
        {
            int hindex = ((i + k) - 1);
            int windex = ((j + g) - 1);
            redSum += image[hindex][windex].rgbtRed;
            greenSum += image[hindex][windex].rgbtGreen;
            blueSum += image[hindex][windex].rgbtBlue;
        }
    }

    float redAverage = (redSum / 9.0);
    float greenAverage = (greenSum / 9.0);
    float blueAverage = (blueSum / 9.0);
    int redA = round(redAverage);
    int greenA = round(greenAverage);
    int blueA = round(blueAverage);

    copyPic[i][j].rgbtRed = redA;
    copyPic[i][j].rgbtGreen = greenA;
    copyPic[i][j].rgbtBlue = blueA;
        }
    }
    return;
}