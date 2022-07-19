from typing import TypedDict

import arrow
import boto3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


class OldAccessKeyUser(TypedDict):
    username: str
    access_key_id: str
    created_date: str


@app.get("/find")
async def find(age_hours: int):
    iam = boto3.resource('iam')
    user_iterator = iam.users.all()
    requested_at_utc_now = arrow.utcnow()
    expired_key_list = []

    for user in user_iterator:
        access_key_iterator = user.access_keys.all()
        for key in access_key_iterator:
            created_at_utc = arrow.get(key.create_date).to('utc')
            created_at_utc_plus_past_time = created_at_utc.shift(hours=age_hours)
            if created_at_utc_plus_past_time <= requested_at_utc_now:
                expired_key_list.append(
                    OldAccessKeyUser(username=key.user_name,
                                     access_key_id=key.access_key_id,
                                     created_date=key.create_date.isoformat())
                )
    return JSONResponse(dict(result=expired_key_list))
