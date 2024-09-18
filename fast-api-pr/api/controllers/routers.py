from ..controllers.Users import Users
from ..controllers.Todos import Todos
from ..controllers.TokenManager import TokenManager

user_router = Users().router
todo_router = Todos().router
token_router = TokenManager().router

routes_list = [
    user_router,
    todo_router,
    token_router
]
