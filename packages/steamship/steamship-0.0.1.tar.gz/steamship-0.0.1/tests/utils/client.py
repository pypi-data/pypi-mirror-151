from steamship import Steamship


def get_steamship_client() -> Steamship:
    # TODO: This should automatically pick up variables from the environment.
    return Steamship(profile="test")
