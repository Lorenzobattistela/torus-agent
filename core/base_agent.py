from fastapi import APIRouter, FastAPI

class BaseAgent:
    def __init__(self, name: str, prefix: str = ""):
        """
        Base class for defining an agent.

        :param name: The name of the agent.
        :param prefix: The API route prefix for the agent.
        """
        self.name = name
        self.prefix = prefix
        self.router = APIRouter(prefix=prefix)
    
    def register_routes(self, app: FastAPI):
        """
        Registers the agent's API routes with the FastAPI app.

        :param app: The FastAPI instance to attach the router to.
        """
        app.include_router(self.router)

    def route(self, path: str, **kwargs):
        """
        Decorator for adding routes to the agent.

        :param path: The API endpoint path (relative to the agent's prefix).
        """
        def decorator(func):
            self.router.add_api_route(path, func, **kwargs)
            return func
        return decorator
    
