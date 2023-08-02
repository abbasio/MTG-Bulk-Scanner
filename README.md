# MTG-Bulk-Scanner
A tool for scanning and cataloging trading cards (WIP)

WIP tool for cataloging bulk MTG card collections. 

Scope: Tool should be able to take in a set name and an image of a card from that set, identify the card, and store the card's data in a CSV.

Currently takes in a set name, then retrieves the card information from the scryfall API as a `.json` file. 
It then uses the `image_uri` field from the card's data to pull images for each card from the set and store them in folders.
Those images will be used to generate image datasets for neural networks to train on
