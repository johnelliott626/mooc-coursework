#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

//constansts such as size of the buffer,
#define BUFFER_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{

    //define all variables, arrays, types
    int fileCounter = 0;
    bool jpgFound = 0; //false
    BYTE buffer[BUFFER_SIZE];
    FILE *pic = NULL;
    char fileName[8];


    //check command line only enters one argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //tell user of error if file cannot be opened and read correctly
    if (argv[1] == NULL)
    {
        printf("The file cannot be opened and/or read correctly.\n");
        return 1;
    }


    //Open memory card file
    char *infile = argv[1];

    FILE *file = fopen(infile, "r");

    //Repeat until end of card
    while (fread(buffer, BUFFER_SIZE, 1, file) == 1)
    {

        //check if start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //set jpgFound to true
            jpgFound = 1;

            //if first JPEG
            if (fileCounter == 0)
            {
                //start writing new JPG file
                sprintf(fileName, "%03i.jpg", fileCounter);
                pic = fopen(fileName, "w");
                fwrite(buffer, BUFFER_SIZE, 1, pic);
                fileCounter++;
            }

            //else (not first JPEG)
            else
            {
                fclose(pic); //close the current picture
                sprintf(fileName, "%03i.jpg", fileCounter);
                pic = fopen(fileName, "a");
                fwrite(buffer, BUFFER_SIZE, 1, pic);
                fileCounter++;
            }
        }

        else //not start of new jpg
        {
            if (jpgFound == true) //if a JPEG has already been found continue writing
            {
                fwrite(buffer, BUFFER_SIZE * sizeof(BYTE), 1, pic);
            }
        }

    }

    //Close any remaining open files
    fclose(file);
    fclose(pic);

    //return 0, end of program
    return 0;

}
