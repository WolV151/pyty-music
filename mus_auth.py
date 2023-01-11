from ytmusicapi import YTMusic


class Authentiactor():
    def __init__(self):

        # your authenticated request headers go here
        self.auth_head: str = """
        """

    def _authenticate(self) -> None:
        YTMusic.setup(filepath="headers_auth.json", headers_raw=self.auth_head)
