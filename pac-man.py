import sys
from src.config import Parser
from pydantic import ValidationError
from pprint import pprint


def pac_man() -> None:
    config_file = sys.argv[1]
    p = Parser(config_file)
    pprint(p.data)


if __name__ == "__main__":
    try:
        pac_man()
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
