from pydantic import BaseModel, Field, ConfigDict


class TaskCreateRequest(BaseModel):
    title: str | None = Field(None, json_schema_extra={"example": "A社への連絡"})
    detail: str = Field(
        ...,
        json_schema_extra={
            "example": "12/22までにA社のBさんにアドベントカレンダーを提出する"
        },
    )
    id: str = Field(
        ..., json_schema_extra={"example": "oishi_o_123", "description": "Event.id"}
    )

    model_config = ConfigDict()


class TaskDeteilResponse(BaseModel):
    id: str
    title: str
    detail: str
    administrator_username: str

    model_config = ConfigDict()