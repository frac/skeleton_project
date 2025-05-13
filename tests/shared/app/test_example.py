import pytest
from fastapi.testclient import TestClient
from shared.app.example import create_example_app


def test_example_app_creation():
    """Test that the example app can be created correctly."""
    app = create_example_app()
    assert app.app.title == "Example API"
    assert app.app.description == "Example API using BaseApp"


def test_example_app_hello_endpoint():
    """Test the hello endpoint in the example app."""
    app = create_example_app()
    client = TestClient(app.app)
    
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from example app!"}


def test_example_app_openapi():
    """Test that the OpenAPI schema is generated correctly."""
    app = create_example_app()
    client = TestClient(app.app)
    
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert schema["info"]["title"] == "Example API"
    assert schema["info"]["description"] == "Example API using BaseApp"
    assert "/hello" in schema["paths"]