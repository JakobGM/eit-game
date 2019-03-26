"""
Module responsible for the storage and retrieval of statistics.

In practice, this means that this module is able to save the results of earlier
games to disk and retrieve these results at a later time. It is also responsible
for the analyzis of this data, such as the scoreboard, player rankings and so
on.
"""

from pathlib import Path


DEFAULT_SAVE_PATH = Path(__file__).parents[1] / 'data' / 'savefile'


class Statistics:
    """
    Class for saving and retrieval of statistics.

    This is the main class of this module, and this is considered the public
    API.
    """

    def __init__(self, save_path: Path = DEFAULT_SAVE_PATH) -> bool:
        """
        Construct statistics object from save file stored on disk.

        :param save_path: Path to file that contains saved games.
        """
        self.save_path = save_path
        self.load_save_file(save_path)

    @staticmethod
    def load_save_file(path: Path) -> bool:
        """
        Load the save data stored in the given path.

        If the path does not exist, the save file is created.

        :param path: Absolute path to savefile.
        :return: Returns True if the savefile already exists, False otherwise.
        """
        assert path.is_absolute()
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()
            return False
        else:
            return True
