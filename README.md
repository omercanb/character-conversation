# Character Conversation
Speak with any movie character.

This repo currently includes the code for a scraping script that scrapes data from the online movie database.
The scraped script data is classified as screen directions vs dialog by some parsing rules.
Some scripts can't be parsed easily. For those scripts, a CNN was trained using the parsed data to classify a line as dialog or screen directions. The CNN was used to classify the rest of the data.
Then, a GPT2 model was fine-tuned on the dialog data to create a model that generated movie dialogue-like text.
The "speaking with any character of choice" tagline is not yet implemented.
