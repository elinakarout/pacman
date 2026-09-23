from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError
from typing import Self


CHEATS = {
    "cheater": False,
    "invincible_mode": False,
    "always_edible": False,
    "ghost_freeze": False,
    "skip_level": False,
    "slow_ghost_speed": False,
    "extra_life": False,
    "increase_player_speed": False,
    "add_ghost": False
}


class Config(BaseModel):
    """Config main class."""

    highscore_filename: str
    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    width: int = 21
    height: int = 21
    seed: int = 42

    @model_validator(mode='after')
    def verify_values(self) -> Self:
        """Validate values."""

        if self.lives <= 0:
            raise PydanticCustomError(
                "ValueError",
                "Lives should be strictly positive"
            )
        elif self.points_per_pacgum <= 0:
            raise PydanticCustomError(
                "ValueError",
                "points_per_pacgum should be strictly positive"
            )
        elif self.points_per_super_pacgum <= 0:
            raise PydanticCustomError(
                "ValueError",
                "points_per_super_pacgum should be strictly positive"
            )
        elif self.points_per_ghost <= 0:
            raise PydanticCustomError(
                "ValueError",
                "points_per_ghost should be strictly positive"
            )
        elif self.width <= 0:
            raise PydanticCustomError(
                "ValueError",
                "Width should be strictly positive"
            )
        elif self.height <= 0:
            raise PydanticCustomError(
                "ValueError",
                "Height should be strictly positive"
            )
        return self
