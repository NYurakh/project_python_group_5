"""Save and load application state via pickle."""

import pickle

from app_context import AppContext
from books.address_book import AddressBook


def save_data(context: AppContext, filename: str = "addressbook.pkl") -> None:
    with open(filename, "wb") as file:
        pickle.dump(context, file)


def load_data(filename: str = "addressbook.pkl") -> AppContext:
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        return AppContext()

    if isinstance(data, AppContext):
        return data
    if isinstance(data, AddressBook):
        return AppContext(address_book=data)

    raise TypeError(f"Unsupported data type in {filename}: {type(data).__name__}")

