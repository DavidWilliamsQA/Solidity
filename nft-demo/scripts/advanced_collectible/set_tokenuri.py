from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_breed

dragon_metadata_dic = {
    "RED": "https://ipfs.io/ipfs/QmXUNgqaAygcspQDGch1nPHYoAJPvXc6vtvFBsWM9CDLyj?filename=0-RED.json",
    "BLUE": "https://ipfs.io/ipfs/QmWBTQHgTyRqg9EbHHohLsxaRRrZKmAiNRhDtMtd5xMJfg?filename=0-BLUE.json",
    "BLACK": "https://ipfs.io/ipfs/QmRyo7EVWbW9stfqD1P1UTPqRgRHh3EBquEPQAn6xT9kRf?filename=1-BLACK.json",
}


def main():
    print(f"working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")

    for tokenId in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        if not advanced_collectible.tokenURI(tokenId).startswith("https://"):
            print(f"Setting Token URI of {tokenId}")
            set_tokenURI(tokenId, advanced_collectible, dragon_metadata_dic[breed])


def set_tokenURI(tokenId, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(tokenId, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT AT {OPENSEA_URL.format(nft_contract.address, tokenId)}"
    )
    print("Please wait up to 20 minutes and hit the refresh metadata button")
