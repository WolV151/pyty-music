from mus_auth import Authentiactor
from mus_callback import SearchInputThread, SearchResultThread
from ytmusicapi import YTMusic
from time import sleep
from pick import pick
from time import sleep

import curses
import os
import pafy
import vlc
import configparser

config = configparser.ConfigParser()
config.read("mus_conf.ini")

class MainPlayer():
    def __init__(self):
        self._run_init()

    def _run_init(self) -> None:
        try:  # try to log in, if setup json does not exist, set it up
            self.yt: YTMusic = YTMusic(auth="headers_auth.json")
        except (AttributeError, FileNotFoundError):
            Authentiactor().authenticate()
            self.yt: YTMusic = YTMusic(auth="headers_auth.json")

        self.serch_string: str = ""
        self.results: list = []
        self.vlc_instance: vlc.Instance = vlc.Instance()
        self.playlist_mix: vlc.MediaList = self.vlc_instance.media_list_new()
        self.media_player: vlc.MediaListPlayer = self.vlc_instance.media_list_player_new()
        self.song_index: int = -1
        self.kb_thread: Thread = SearchInputThread(self._input_callback)
        self.select_thread: Thread = None
        self.video: vlc.Media = None
        self.volume: int = int(config['VARS']['default_volume'])

        self.input_mode: bool = 0  # 0 for search mode, 1 for song/playlist control mode

        self.media_player.get_media_player().audio_set_volume(
            self.volume)  # set default volume

    def _media_player_set_media(self, media: vlc.MediaList) -> None:
        self.media_player.set_media_list(media)

        if not self.media_player.is_playing():
            self.media_player.play()

    def _yt_search_handle(self, search_keyword: str) -> None:
        self.results = self.yt.search(search_keyword)
        print(self.results)
        self.select_thread = SearchResultThread(self._pick_result_callback)
        self.select_thread.join()
        related_track_list: dict = self.yt.get_watch_playlist(
            videoId=self.results[self.song_index]["videoId"])["tracks"]  # gives the dict of the object
        self.video = pafy.new(
            self.results[self.song_index]["videoId"]).getbest()
        # self.playlist_mix.add_media(self.video.url)

        for track in related_track_list:
            self.playlist_mix.add_media(
                pafy.new(track["videoId"]).getbest().url)

        print(len(self.playlist_mix))
        self._media_player_set_media(self.playlist_mix)

    def _input_callback(self, inp: str) -> None:
        if inp == str(config['CONTROL']['quit_app']):
            self.media_player.stop()
            exit()

        if inp == str(config['CONTROL']['enter_control']):
            self.input_mode = 1

        if self.input_mode == 0:
            self.search_string = inp
            self._yt_search_handle(self.search_string)
        else:
            if self.video is None or self.media_player.get_media_player().get_media() is None:
                print("No media is playing to be controlled.")
                sleep(1.5)
                self.input_mode = 0
            else:
                curses.wrapper(self._process_key_stroke)

    def _pick_result_callback(self) -> None:
        titles: list[str] = []
        indecies: list[int] = []
        index: int = 0
        heading: str = "Pick a search result: "

        for song in self.results:
            if song["resultType"] == "song" or song["resultType"] == "video":
                titles.append(f"{song['title']} - {song['resultType']}")
                indecies.append(index)
            index += 1

        selection, index_selection = pick(
            titles, heading, indicator='=>', default_index=0)
        self.song_index = indecies[index_selection]

    def _process_key_stroke(self, win) -> None:
        win.nodelay(True)
        key = ""
        win.clear()
        while ...:
            try:
                key = win.getkey()
                win.clear()
                # win.addstr("Time: " + str(self.convert_millis(self.media_player.get_media_player().get_time()) + "/" + str(self.convert_millis(self.media_player().get_media_player().get_length()))))
                win.addstr(str(key))
                if str(key).lower() == config['CONTROL']['exit_control']:
                    self.input_mode = 0
                    break
                elif str(key) == config['CONTROL']['volume_up']:
                    self.media_player.get_media_player().audio_set_volume(
                        self.volume + int(config['VARS']['volume_increase']))

                    self.volume += int(config['VARS']['volume_increase'])
                elif str(key) == config['CONTROL']['volume_down']:
                    self.media_player.get_media_player().audio_set_volume(
                        self.volume - int(config['VARS']['volume_increase']))

                    self.volume -= int(config['VARS']['volume_increase'])
                elif str(key).lower() == config['CONTROL']['pos_up']:
                    self.media_player.get_media_player().set_position(
                        self.media_player.get_media_player().get_position() - 0.1)
                    win.addstr(str(key))
                elif str(key).lower() == config['CONTROL']['pos_down']:
                    self.media_player.get_media_player().set_position(
                        self.media_player.get_media_player().get_position() + 0.1)
                elif str(key) == config['CONTROL']['next_media']:
                    self.media_player.previous()
                elif str(key) == config['CONTROL']['prev_media']:
                    self.media_player.next()
                elif str(key) == config['CONTROL']['pause_media']:
                    self.media_player.pause()
                elif str(key) == config['CONTROL']['last_media']:
                    self.media_player.play_item_at_index(
                        len(self.playlist_mix) - 1)

            except Exception:
                pass

# unused for now, I would like to add a progress bar for the media
    def convert_millis(self, millis):
        seconds = (millis/1000) % 60
        minutes = (millis/(1000*60)) % 60
        hours = (millis/(1000*60*60)) % 24
        return seconds, minutes, hours
