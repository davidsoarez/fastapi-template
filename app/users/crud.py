from app.db.crud import CrudBase
from app.users.models import User


class UserCrud(CrudBase):
    pass


user = UserCrud(User)
