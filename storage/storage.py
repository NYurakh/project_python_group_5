"""Save and load the address book to disk via pickle."""

# TODO: add logic of saving notes as well.

import pickle

from books.address_book import AddressBook


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()

