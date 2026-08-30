"""Save and load application state via pickle."""

import pickle
import warnings
from datetime import datetime
from pathlib import Path

from app_context import AppContext
from books.address_book import AddressBook

DATA_DIR = Path(__file__).resolve().parent.parent / "userdata"
DATA_FILE = DATA_DIR / "assistant_data.pkl"


class StorageRecoveryWarning(UserWarning):
    """Warns that unreadable persisted data was backed up and reset."""


def _backup_corrupt_file(filename: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = filename.with_name(
        f"{filename.stem}.corrupt-{timestamp}{filename.suffix}"
    )
    filename.replace(backup)
    return backup


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
    except (EOFError, pickle.UnpicklingError) as exc:
        backup = _backup_corrupt_file(filename)
        warnings.warn(
            f"Could not load saved data ({exc}). "
            f"The unreadable file was moved to {backup}.",
            StorageRecoveryWarning,
            stacklevel=2,
        )
        return AppContext()

    if isinstance(data, AppContext):
        return data

    if isinstance(data, AddressBook):
        return AppContext(address_book=data)

    raise TypeError(f"Unsupported data type in {filename}: {type(data).__name__}")
