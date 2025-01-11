# Analysis

## Layer 7, Head 9

This attention head evaluates each word's relationshp with how close it is to the end of the sentence. It appears to have learned the context of the word with a higher attention score, the closer it is to the end of the sentenc.

Example Sentences:

-   I bounced the [MASK] up and down.
-   I [MASK] to the store.

## Layer 1, Head 6

This attention head evaluates the relationship between the mask and its position in the sentence. It appears to be paying attention to the start and end position of the sentence for the masked word. Recognizing the mask's context as in its placement in the sentence helps to determine what the word is.

Example Sentences:

-   What in the [MASK] are you doing.
-   Text: How do you [MASK] like that.
