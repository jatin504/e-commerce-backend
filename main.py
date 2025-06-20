import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import get_hashed_password

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


@post_save(User)
async def create_business(
        sender: "Type[User]",
        instance: User,
        created: bool,
        using_db: "Optional[BaseDBAsyncClient]",
        update_fields: List[str]
) -> None:
    if created:
        business_obj = await Business.create(
            business_name=instance.username, owner=instance
        )
        await business_pydqantic.from_tortoise_orm(business_obj)
        # send the email


@app.get("/")
async def index():
    return {"Hello world"}


@app.post("/registration")
async def user_regestration(user: user_pydanticIn):
    user_info = user.model_dump(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydentic.from_tortoise_orm(user_obj)

    return {"status": "ok",
            "data": f"hello{new_user.username} thnx for choosing services please check your email inbox and click on"
                    f" the link to confirm your registraion."
            }


if __name__ == "__main__":
    uvicorn.run(app)
