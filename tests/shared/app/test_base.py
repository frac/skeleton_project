import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from shared.app import BaseApp


def test_base_app_initialization():
    """Test BaseApp initialization with various parameters."""
    # Test with minimal parameters
    app = BaseApp(title="Test App")
    assert app.app.title == "Test App"
    assert app.app.version == "0.1.0"
    
    # Test with all parameters
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
    
    app = BaseApp(
        title="Full Test App",
        description="Test description",
        version="1.0.0",
        prefix="/api",
        lifespan=lifespan
    )
    assert app.app.title == "Full Test App"
    assert app.app.description == "Test description"
    assert app.app.version == "1.0.0"
    assert app.router.prefix == "/api"


def test_include_router():
    """Test adding a router to the app."""
    app = BaseApp(title="Router Test")
    router = APIRouter()
    
    @router.get("/test")
    def test_route():
        return {"message": "test"}
    
    app.include_router(router, prefix="/api", tags=["test"])
    
    client = TestClient(app.app)
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}


def test_mount_to_app():
    """Test mounting a BaseApp router to another FastAPI app."""
    base_app = BaseApp(title="Base App")
    
    @base_app.router.get("/base")
    def base_route():
        return {"message": "base"}
    
    parent_app = FastAPI()
    base_app.mount_to_app(parent_app, prefix="/mounted", tags=["mounted"])
    
    client = TestClient(parent_app)
    response = client.get("/mounted/base")
    assert response.status_code == 200
    assert response.json() == {"message": "base"}


def test_event_handlers():
    """Test event handlers."""
    app = BaseApp(title="Events Test")
    
    startup_called = False
    shutdown_called = False
    
    def startup():
        nonlocal startup_called
        startup_called = True
    
    def shutdown():
        nonlocal shutdown_called
        shutdown_called = True
    
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    
    # Manually trigger the event handlers
    for handler in app.app.router.on_startup:
        handler()
    
    for handler in app.app.router.on_shutdown:
        handler()
    
    assert startup_called
    assert shutdown_called


def test_create_lifespan():
    """Test create_lifespan static method."""
    startup_called = False
    shutdown_called = False
    
    def startup():
        nonlocal startup_called
        startup_called = True
    
    def shutdown():
        nonlocal shutdown_called
        shutdown_called = True
    
    lifespan = BaseApp.create_lifespan(startup, shutdown_func=shutdown)
    
    # Create a FastAPI app with this lifespan
    app = FastAPI(lifespan=lifespan)
    
    # Use a TestClient to trigger the lifespan events
    with TestClient(app):
        pass
    
    assert startup_called
    assert shutdown_called