from pydantic import BaseModel


class ConsultantOnlineStatusRequest(
    BaseModel
):
    is_online: bool