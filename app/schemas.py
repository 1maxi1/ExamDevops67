from pydantic import BaseModel, ConfigDict, Field


class WorkshopClassResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int


class RegistrationRequest(BaseModel):
    sms_code: str = Field(min_length=1, max_length=10)


class RegistrationResponse(BaseModel):
    registration_id: int
    sms_code: str
    workshop_name: str
    registration_time: str
