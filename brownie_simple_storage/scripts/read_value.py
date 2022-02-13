from brownie import SimpleStorage, accounts, config


def read_contarct():
    simple_storage = SimpleStorage[-1]
    # go take the index that one less than the length
    # ABI
    # Address
    simple_storage.retrieve()


def main():
    read_contarct()
