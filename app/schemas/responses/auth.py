from pydantic import BaseModel
from typing import Union


class TokenResponse(BaseModel):
    access_token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "fon23f92h39f29f19h3",
                }
            ]
        }
    }


class LoginResponse(BaseModel):
    refresh_token: Union[str, None] = None
    access_token: Union[str, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "fon23f92h39f29f19h3",
                    "refresh_token": "02f209j02f39h120f101h0f1h0"
                }
            ]
        }
    }
