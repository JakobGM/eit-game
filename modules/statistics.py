"""
Module responsible for the storage and retrieval of statistics.

In practice, this means that this module is able to save the results of earlier
games to disk and retrieve these results at a later time. It is also responsible
for the analyzis of this data, such as the scoreboard, player rankings and so
on.
"""

import pickle
from pathlib import Path
from typing import List, Optional, Set


DEFAULT_SAVE_PATH = Path(__file__).parents[1] / 'data' / 'savefile'


class Data:
    """Class responsible for storing data related to the statistics module."""

    def __init__(self):
        """
        Construct Data object.

        No parameters are accepted, as the class is intended to be instantiated
        with no data and then mutated with new data that may come in.
        """
        self.all_rankings = []


class Statistics:
    """
    Class for saving and retrieval of statistics.

    This is the main class of this module, and this is considered the public
    API.
    """

    def __init__(self, save_path: Path = DEFAULT_SAVE_PATH) -> None:
        """
        Construct statistics object from save file stored on disk.

        :param save_path: Path to file that contains saved games.
        """
        assert isinstance(save_path, Path)
        self.save_path = save_path
        self._load_data()

    def save(self, ranking: Optional[List[str]] = None) -> None:
        """
        Save new data from a game for later retrieval and analysis.

        :param ranking: A list of strings ordered by whom did best during the
          game in descending order.
          For instance ranking=['gold', 'silver', 'bronze'].
        """
        if ranking:
            assert isinstance(ranking, list)
            assert isinstance(ranking[0], str)
            self.data.all_rankings.append(ranking)
        self._save_data()


    @property
    def all_players(self) -> Set[str]:
        """Return the name of all players that have ever played."""
        return {name for ranking in self.data.all_rankings for name in ranking}

    def _load_data(self) -> None:
        """
        Load the save data stored in the given path.

        If the path does not exist, the save file is created.
        The data is persisted to self.data.

        :param path: Absolute path to savefile.
        """
        assert self.save_path.is_absolute()
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.save_path.exists():
            self.save_path.touch()
            self.data = Data()
            self._save_data()
        else:
            self.data = pickle.loads(self.save_path.read_bytes())

    def _save_data(self) -> None:
        """Save data to path specified by __init__ save_path parameter."""
        self.save_path.write_bytes(
            data=pickle.dumps(self.data, protocol=pickle.HIGHEST_PROTOCOL),
        )
