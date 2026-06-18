from pydantic import BaseModel


class AddExpertiseRequest(
    BaseModel
):
    category_ids: list[int]