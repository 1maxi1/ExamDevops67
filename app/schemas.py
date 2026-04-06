from pydantic import BaseModel, ConfigDict, Field


class MetroChangeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    affected_line: str


class BalanceRequest(BaseModel):
    phone: str = Field(min_length=5, max_length=20)
    sms_code: str = Field(min_length=1, max_length=10)


class BalanceResponse(BaseModel):
    ticket_id: int
    phone: str
    balance: int
    last_entry_station: str
