from config import settings

from enum import Enum
from datetime import datetime
from typing import Optional
from nocodb.filters.raw_filter import RawFilter
from nocodb.filters.factory import raw_template_filter_class_factory as custom_filter
from nocodb.infra.requests_client import NocoDBRequestsClient
from nocodb.nocodb import APIToken, NocoDBProject
from pydantic import BaseModel, Field


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


class NocoEpisode(BaseModel):
    _complete_filter = RawFilter("(Titel,isnot,null)~and(Beschreibung,isnot,null)")

    noco_id: int = Field(alias="Id")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    title: str = Field(alias="Titel")
    episode_title: str = Field(alias="Folge")
    episode_type: EpisodeTyp = Field(alias="Typ")
    source: str = Field(alias="Medium/Quelle")
    server_index: Optional[str] = Field(alias="Server Index")
    teaser: Optional[str] = Field(alias="Teaser")
    description: str = Field(alias="Beschreibung")
    tags: str = Field(alias="Schlagwörter")
    has_path_error: bool = Field(alias="Pfad Error")
    is_copied: bool = Field(alias="Auf Transcodingrechner")
    is_transcoded: bool = Field(alias="Transcoding abgeschlossen")

    class Config:
        allow_populate_by_field_name = True


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
    
    def update_server_index(self, item_id: int, value: Optional[str]):
        client = nocodb_client()
        project = nocodb_project()
        client.table_row_update(
            project,
            settings.episode_table, # type: ignore
            item_id,
            {"Server Index": value},
        )

    def update_has_path_error(self, item_id: int, value: bool):
        print(f"set has_path_error of item {item_id} to '{value}'")