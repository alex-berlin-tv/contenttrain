from ntpath import join
from config import settings

import unicodedata
from enum import Enum
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from nocodb.filters import EqFilter
from nocodb.filters.raw_filter import RawFilter
from nocodb.infra.requests_client import NocoDBRequestsClient
from nocodb.nocodb import APIToken, NocoDBProject, WhereFilter
from pydantic import BaseModel, Field


def nocodb_client() -> NocoDBRequestsClient:
    return NocoDBRequestsClient(
        APIToken(settings.nocodb_api_token), # type: ignore
        settings.nocodb_url # type: ignore
    )


def nocodb_project() -> NocoDBProject:
    return NocoDBProject("noco", settings.project) # type: ignore


class EpisodeTyp(str, Enum):
    EVENT = "Event"
    MUSIC = "Musik"
    SHOW = "Sendung"


class SourceState(str, Enum):
    UNKNOWN = "Unklar"
    INDEX_NOT_FOUND = "Index nicht auf Server"
    DISA_SERVER = "Sendeserver"
    YOUTUBE = "YouTube"


class FileState(str, Enum):
    MISSING = "Fehlt"
    EXISTS = "Vorhanden"
    DONE = "Abgeschlossen & Gelöscht"


class NocoEpisode(BaseModel):
    # _complete_filter = RawFilter("(Titel,isnot,null)~and(Beschreibung,isnot,null)")
    _complete_filter = RawFilter("(Titel,isnot,null)")

    noco_id: int = Field(alias="Id")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    title: str = Field(alias="Titel")
    episode_title: str = Field(alias="Folge")
    episode_type: EpisodeTyp = Field(alias="Typ")
    source: Optional[str] = Field(alias="Medium/Quelle")
    server_index: Optional[str] = Field(alias="Server Index")
    youtube_url: Optional[str] = Field(alias="YouTube URL")
    teaser: Optional[str] = Field(alias="Teaser")
    description: Optional[str] = Field(alias="Beschreibung")
    tags: Optional[str] = Field(alias="Schlagwörter")
    source_state: Optional[SourceState] = Field(alias="Status Quelle")
    file_on_edit_state: Optional[FileState] = Field(alias="Status Datei auf Edit")
    is_transcoded: bool = Field(alias="Transcoding abgeschlossen")
    source_file: Optional[str] = Field(alias="Source File")

    class Config:
        allow_populate_by_field_name = True

    def file_name(self) -> str:
        title = self.title.lower()
        to_replace = {
            ord('ä'): 'ae',
            ord('ü'): 'ue',
            ord('ö'): 'oe',
            ord('ß'): 'ss',
            ord(" "): '-',
            ord("."): '-',
            ord(","): '-',
            ord(":"): '-',
            ord("_"): '-',
            ord("/"): '-',
            ord("'"): '',
            ord("\""): '',
            ord("|"): '',
            ord("?"): '',
            ord("!"): '',
        }
        title = title.translate(to_replace)
        title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')

        rsl = ""
        last_char = ""
        for char in title:
            if char != "-" or last_char != "-":
                rsl += char
            last_char = char
        return f"e-{self.noco_id:04d}_{rsl}"
    
    def local_server_source_path(self) -> Optional[Path]:
        if not self.server_index:
            print("error: server index is null")
            return None
        path = self.server_index.replace(settings.crop_path_prefix, "", 1) # type: ignore
        path = path.replace("\\", "/")
        return Path(settings.file_server_location) / Path(path) # type: ignore


class NocoEpisodes(BaseModel):
    __root__: list[NocoEpisode]

    @classmethod
    def from_nocodb(cls):
        client = nocodb_client()
        project = nocodb_project()
        data_raw = client.table_row_list(
            project,
            settings.episode_table, # type: ignore
            filter_obj=NocoEpisode._complete_filter,
            params={"limit": settings.query_limit},
        )
        return cls.parse_obj(data_raw["list"])

    def __update(self, episode: NocoEpisode, key: str, value: Any):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            episode.noco_id,
            {key: value},
        )
    
    def __count(self, filter_obj: WhereFilter) -> int:
        client = nocodb_client()
        project = nocodb_project()
        data = client.table_count(
            project,
            settings.episode_table, # type: ignore
            filter_obj=filter_obj
        )
        return data["count"]
    
    def update_server_index(self, episode: NocoEpisode, value: Optional[str]):
        self.__update(episode, "Server Index", value)

    def update_source_state(self, episode: NocoEpisode, value: SourceState):
        self.__update(episode, "Status Quelle", value)

    def update_has_path_error(self, episode: NocoEpisode, value: bool):
        self.__update(episode, "Pfad Error", value)

    def update_file_on_edit_state(self, episode: NocoEpisode, value: FileState):
        self.__update(episode, "Status Datei auf Edit", value)

    def update_is_transcoded(self, episode: NocoEpisode, value: bool):
        self.__update(episode, "Transcoding abgeschlossen", value)

    def update_source_file(self, episode: NocoEpisode, value: str):
        self.__update(episode, "Source File", value)

    def count_by_source_state(self, state: SourceState) -> int:
        return self.__count(EqFilter("Status Quelle", state.value))
    
    def count_by_file_state(self, state: FileState) -> int:
        return self.__count(EqFilter("Status Datei auf Edit", state.value))
    
    def count_by_is_transcoded(self, value: bool) -> int:
        return self.__count(EqFilter("Transcoding abgeschlossen", value))

