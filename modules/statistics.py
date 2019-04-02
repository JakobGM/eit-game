"""
Module responsible for the storage and retrieval of statistics.

In practice, this means that this module is able to save the results of earlier
games to disk and retrieve these results at a later time. It is also responsible
for the analyzis of this data, such as the scoreboard, player rankings and so
on.
"""

import pickle
from pathlib import Path
from typing import Dict, List, Optional, Set

from trueskill import TrueSkill, Rating, backends, rate


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

        # Use the same TrueSkill parameters in the entire class
        self.env = TrueSkill()

        # Enable the scipy backend of TrueSkill
        backends.choose_backend('scipy')


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


    def true_skill(self) -> Dict[str, Rating]:
        """
        Return TrueSkill Rating object for each player.

        A TrueSkill rating is a normal distribution with a given mean and
        variance. High means are indicative of good players, that way you
        can compare players.
        """
        # First create rating objects for each player, assuming no prior skill
        rankings = {
            name: self.env.create_rating()
            for name
            in self.all_players
        }

        # Iterate over all the saved games we have in our catalogue
        for game in self.data.all_rankings:
            # We have a free-for-all, so each player are placed in their own
            # teams.
            rating_groups = [[rankings[name]] for name in game]

            # The rank of the players are stored from best to worse.
            # TrueSkill uses the opposite order.
            ranks = list(reversed(range(len(game))))

            # Update the rating for each player
            ratings = self.env.rate(rating_groups=rating_groups, ranks=ranks)
            for name, ranking in zip(game, ratings):
                rankings[name] = ranking[0]

        # Sort the dictionary by player rating before returning it
        sorted_rankings = sorted(
            rankings.items(),
            key=lambda r: self.env.expose(r[1])
        )
        return dict(sorted_rankings)


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
