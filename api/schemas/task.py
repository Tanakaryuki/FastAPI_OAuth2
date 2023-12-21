from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str | None = Field(None, example="抽選で10名様に美食ツアーをプレゼント")
    detail: str = Field(..., example="抽選で10名の幸運な参加者に、豪華な美食ツアーをプレゼントします!!")
    administrator_id: str = Field(..., example="admin")
    id: str = Field(..., example="oishi_o_123", description="Event.id")

    class Config:
        from_attributes = True
        
class TaskDeteilResponse(BaseModel):
    id: str
    title: str
    administrator_id: str

    class Config:
        from_attributes = True