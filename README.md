# MTG-Bulk-Scanner
A tool for scanning and cataloging trading cards (WIP)

Tool for cataloging bulk MTG card collections. 

Scope: Tool should be able to take in a set name and an image of a card from that set, identify the card, and store the card's data in a CSV. If the card already exists, increment the count by 1 to track collection.

Currently takes in a set name, then retrieves the card information from the scryfall API as a `.json` file. 
It then uses the `image_uri` field from the card's data to pull images for each card from the set and store them in folders.
The images are then fed through a function that generates training data for a neural network. Training data images are distorted and adjusted to increase accuracy in real-world scenarios
