from fastapi import Depends

from models.user import User
from utils import get_current_user

UserDepends: User = Depends(get_current_user)
