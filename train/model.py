from config import settings

from enum import Enum
from datetime import datetime
from typing import Optional
from nocodb.filters import EqFilter
from nocodb.filters.raw_filter import RawFilter
from nocodb.filters.factory import raw_template_filter_class_factory as custom_filter
from nocodb.infra.requests_client import NocoDBRequestsClient
from nocodb.nocodb import APIToken, NocoDBProject
from pydantic import BaseModel, Field
import unicodedata


def nocodb_client() -> NocoDBRequestsClient:
    return NocoDBRequestsClient(
        APIToken(settings.nocodb_api_token), # type: ignore
        settings.nocodb_url # type: ignore
    )


def nocodb_project() -> NocoDBProject:
    return NocoDBProject("noco", settings.project) # type: ignore


class EpisodeTyp(str, Enum):
    event = "Event"
    music = "Musik"
    show = "Sendung"


class SourceState(str, Enum):
    unknown = "Unklar"
    index_not_found = "Index nicht auf Server"
    disa_server = "Sendeserver"
    youtube = "YouTube"


class NocoEpisode(BaseModel):
    _complete_filter = RawFilter("(Titel,isnot,null)~and(Beschreibung,isnot,null)")
    # _complete_filter = RawFilter("(Titel,isnot,null)")

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
    is_copied: bool = Field(alias="Auf Transcodingrechner")
    is_transcoded: bool = Field(alias="Transcoding abgeschlossen")

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
    
    def local_server_source_path(self) -> Path:



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
    
    def update_server_index(self, episode: NocoEpisode, value: Optional[str]):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            episode.noco_id,
            {"Server Index": value},
        )

    def update_source_state(self, episode: NocoEpisode, value: SourceState):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            episode.noco_id,
            {"Status Quelle": value.value},
        )

    def update_has_path_error(self, episode: NocoEpisode, value: bool):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            episode.noco_id,
            {"Pfad Error": value},
        )

    def update_is_copied(self, episode: NocoEpisode, value: bool):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            episode.noco_id,
            {"Auf Transcodingrechner": value},
        )

    def count_by_source_state(self, state: SourceState) -> int:
        client = nocodb_client()
        project = nocodb_project()
        data = client.table_count(
            project,
            settings.episode_table, # type: ignore
            filter_obj=EqFilter("Status Quelle", state.value)
        )
        return data["count"]
