from fastapi import APIRouter
from .base import BaseApp

# Example usage of BaseApp
def create_example_app():
    """Create an example app using BaseApp."""
    
    # Define a lifespan context manager
    @BaseApp.create_lifespan
    def startup_db():
        print("Starting up database connection...")
        
    db_disconnect = lambda: print("Disconnecting from database...")
    
    lifespan = BaseApp.create_lifespan(startup_db, db_disconnect=db_disconnect)
    
    app = BaseApp(
        title="Example API",
        description="Example API using BaseApp",
        prefix="/api",
        lifespan=lifespan
    )
    
    # Create a router
    router = APIRouter()
    
    @router.get("/hello")
    async def hello():
        return {"message": "Hello from example app!"}
    
    ## Include the router in the app
    app.include_router(router, tags=["example"])
    
    return app