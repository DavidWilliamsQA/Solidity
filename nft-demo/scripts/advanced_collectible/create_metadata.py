import json
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from scripts.upload_to_pinata import upload_to_pinata
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import os

breed_to_image_uri = {
    "RED": "https://ipfs.io/ipfs/QmYsimP59G64kUyNrkckFjYBJZP1mhZd7Nn1SSKX6p5ffY?filename=RED.png",
    "BLUE": "https://ipfs.io/ipfs/QmWbbwMSySdJmoAwWkcfUmpKD6XX89J6YzZr9oYVYJ5fKX?filename=BLUE.png",
    "BLACK": "https://ipfs.io/ipfs/QmbHGpzqwtpZ8hAJT9WXCPKEGKSxyHWyq6vPZxBvMjxmKR?filename=BLACK.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        print(metadata_file_name)
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"A fierce {breed} dragon"

            image_path = "./img/" + breed + ".png"

            image_uri = None

            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
            print(collectible_metadata)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        ipfs_hash, filename = upload_to_pinata(filepath)
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
