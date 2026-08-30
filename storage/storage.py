"""Save and load application state via pickle."""

import pickle
from pathlib import Path

from app_context import AppContext
from books.address_book import AddressBook


DATA_DIR = Path(__file__).resolve().parent.parent / "userdata"
DATA_FILE = DATA_DIR / "assistant_data.pkl"


def save_data(
    context: AppContext,
    filename: Path = DATA_FILE,
) -> None:
    """Save application state to a pickle file."""

    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "wb") as file:
        pickle.dump(context, file)


def load_data(
    filename: Path = DATA_FILE,
) -> AppContext:
    """Load application state from a pickle file."""

    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

    except FileNotFoundError:
        return AppContext()

    if isinstance(data, AppContext):
        return data

    if isinstance(data, AddressBook):
        return AppContext(address_book=data)

    raise TypeError(
        f"Unsupported data type in {filename}: "
        f"{type(data).__name__}"
    )
