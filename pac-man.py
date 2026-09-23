def pac_man() -> None:
    if len(sys.argv) == 1:
        raise ValueError(
            "Please specify the configurations json as argument."
            "\n[uv run pac-man.py config.json]"
        )
    config_file = sys.argv[1]
    p = Parser(config_file)
    g = Game(p.data)
    g.start()


if __name__ == "__main__":
    try:
        import sys
        from pydantic import ValidationError
        from src.config import Parser
        from src.rendering import Game

        pac_man()
    except KeyboardInterrupt:
        print("exited")
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
    finally:
        print("Thank you for checking our project :)")
