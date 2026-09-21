from .data import Config
import json


class Parser():
    highscore_filename: str
    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    width: int
    height: int
    seed: int

    def __init__(self, config_file: str) -> None:
        print(f"Reading file: {config_file}")
        self.config_data = self.get_config_data(config_file)
        self.parse_args()
        # self.parse_level_args()
        self.data = self.create_config()

    @staticmethod
    def get_config_data(config_file: str) -> dict:
        content = ""
        with open(config_file, 'r') as fd:
            for line in fd:
                if not line.strip().startswith("#"):
                    content += line
        try:
            config_data = json.loads(content)
        except Exception:
            raise ValueError(
                f"{config_file} Error: Invalid json, cannot parse"
            )
        if not isinstance(config_data, dict):
            raise ValueError(
                f"{config_file} Error: expected a JSON object at top "
                f"level, got {type(config_data).__name__}"
            )
        return config_data

    @staticmethod
    def default_levels(count: int = 3) -> list[dict]:
        width, height, level_max_time = 21, 21, 90
        levels = []
        for _ in range(count):
            levels.append({
                "width": width,
                "height": height,
                "seed": None,
                "level_max_time": level_max_time,
            })
            width += 2
            height += 2
            level_max_time -= 10
        return levels

    def parse_args(self) -> None:
        config_data = self.config_data
        defaults = {
            "highscore_filename": "highscore.json",
            "lives": 3,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "width": 21,
            "height": 21,
            "seed": 42
        }
        for key, default in defaults.items():
            try:
                config_data[key]
            except KeyError:
                print(
                    f"{key} not specified,",
                    f"resulting to default value: {default}"
                )
            setattr(self, key, config_data.get(key, default))

    def create_config(self) -> Config:
        print("Configurations set")
        return Config(
            highscore_filename=self.highscore_filename,
            lives=self.lives,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            width=self.width,
            height=self.height,
            seed=self.seed
        )
