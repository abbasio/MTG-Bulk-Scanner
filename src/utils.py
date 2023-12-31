import os

items_to_clean = [
    "object",
    "oracle_id",
    "multiverse_ids",
    "mtgo_id",
    "mtgo_foil_id",
    "tcgplayer_id",
    "cardmarket_id",
    "lang",
    "uri",
    "scryfall_uri",
    "layout",
    "highres_image",
    "image_status",
    "games",
    "foil",
    "nonfoil",
    "finishes",
    "oversized",
    "promo",
    "variation",
    "set_type",
    "set_uri",
    "set_search_uri",
    "scryfall_set_uri",
    "rulings_uri",
    "prints_search_uri",
    "digital",
    "card_back_id",
    "illustration_id",
    "story_spotlight",
    "booster",
    "edhrec_rank",
    "penny_rank",
    "related_uris",
    "purchase_uris",
    "security_stamp",
    "full_art",
    "textless",
    "prices",
    "reprint",
]


def make_dirs(paths: list):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def filter_lands(card):
    basic_lands = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
    if card["name"] in basic_lands:
        return False
    else:
        return True
