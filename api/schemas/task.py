from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str | None = Field(None, example="A社への連絡")
    detail: str = Field(..., example="12/22までにA社のBさんにアドベントカレンダーを提出する")
    administrator_username: str = Field(..., example="admin")
    id: str = Field(..., example="oishi_o_123", description="Event.id")

    class Config:
        from_attributes = True
        
class TaskDeteilResponse(BaseModel):
    id: str
    title: str
    detail: str
    administrator_username: str

    class Config:
        from_attributes = True