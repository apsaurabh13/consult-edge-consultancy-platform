from pydantic import BaseModel


class CreateExpertiseCategoryRequest(
    BaseModel
):
    name: str