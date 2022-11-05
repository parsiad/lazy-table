"""_artist.py"""

from abc import ABC
from typing import Optional
import abc


class Artist(ABC):
    """Abstract artist class used to render tables."""

    @abc.abstractmethod
    def render(self, result: str) -> None:
        """Render."""

    @abc.abstractmethod
    def init(self, n_rows: Optional[int]) -> None:
        """Initialize."""
