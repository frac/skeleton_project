from fastapi import FastAPI, APIRouter
from typing import Optional, List, Dict, Any, Union, Callable
from contextlib import asynccontextmanager
import asyncio


class BaseApp:
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        version: str = "0.1.0",
        prefix: Optional[str] = None,
        lifespan: Optional[Callable] = None,
    ):
        """Initialize a base FastAPI application.
        
        Args:
            title: Name of the application
            description: Optional description for the app
            version: API version
            prefix: Optional URL prefix for all routes
            lifespan: Optional lifespan context manager
        """
        if lifespan:
            self.app = FastAPI(
                title=title,
                description=description,
                version=version,
                lifespan=lifespan,
            )
        else:
            self.app = FastAPI(
                title=title,
                description=description,
                version=version,
            )
        self.router = APIRouter(prefix=prefix) if prefix else APIRouter()
        
    def include_router(self, router: APIRouter, prefix: Optional[str] = None, tags: Optional[List[str]] = None):
        # FastAPI is a bit weird with the prefix
        # if prefix parameter is passed to the include_router method it will be used even if None
        if prefix:
            self.app.include_router(router, prefix=prefix, tags=tags)
        else:
            self.app.include_router(router, tags=tags)
    
    def mount_to_app(self, app: FastAPI, prefix: Optional[str] = None, tags: Optional[List[str]] = None):
        app.include_router(self.router, prefix=prefix, tags=tags)
    
    def add_middleware(self, middleware_class, **options):
        self.app.add_middleware(middleware_class, **options)
    
    def add_event_handler(self, event_type: str, func: Callable):
        """Add an event handler.
        
        Args:
            event_type: Event type ("startup" or "shutdown")
            func: Function to call on the event
        """
        self.app.add_event_handler(event_type, func)
        
    @staticmethod
    def create_lifespan(*startup_funcs, **shutdown_funcs):
        """Create a lifespan context manager with startup and shutdown functions.
        
        Args:
            *startup_funcs: Functions to call on startup
            **shutdown_funcs: Functions to call on shutdown, keyed by name
            
        Returns:
            A lifespan context manager
        """
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup
            for func in startup_funcs:
                await func() if asyncio.iscoroutinefunction(func) else func()
                
            yield
            
            # Shutdown
            for name, func in shutdown_funcs.items():
                await func() if asyncio.iscoroutinefunction(func) else func()
                
        return lifespan