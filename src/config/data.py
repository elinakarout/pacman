from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError
from typing import Self


class Level(BaseModel):
    width: int = 21
    height: int = 21
    seed: int | None = None
    level_max_time: int = 90

    @model_validator(mode='after')
    def verify_values(self) -> Self:
        if self.width <= 0:
            raise PydanticCustomError(
                "ValueError",
                "Width should be strictly positive"
            )
        elif self.height <= 0:
            raise PydanticCustomError(
                "ValueError",
                "Height should be strictly positive"
            )
        elif self.level_max_time <= 15:
            raise PydanticCustomError(
                "ValueError",
                "level_max_time should be greater than 15"
            )
        return self


class Config(BaseModel):
    highscore_filename: str
    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    levels: list[Level]

    @model_validator(mode='after')
    def verify_values(self) -> Self:
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
        return self
