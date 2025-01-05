import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import io
from datetime import timedelta

from app.backend.routes.document import router
from app.backend.auth.utils import create_access_token
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_user():
    return Mock(
        id=1,
        email="test@example.com",
        username="testuser"
    )

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def auth_token():
    # Create a real token
    token_data = {"sub": 1}  # user_id = 1
    token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {token}"}

def test_upload_document(mock_user, mock_db, auth_token):
    """Test document upload"""
    mock_workspace = Mock(
        id=1,
        name="test_workspace",
        creator_id=1,
        collection_name="test_collection"
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_workspace

    with patch('app.backend.auth.utils.get_current_user', return_value=mock_user), \
         patch('app.backend.database.db.get_db', return_value=mock_db), \
         patch('app.backend.aws.s3.s3_wrapper.S3Wrapper') as mock_s3, \
         patch('app.backend.documents.utils.check_existing_document', return_value=False), \
         patch('PyPDF2.PdfReader'), \
         patch('app.backend.database.vector_db.get_doc_store'), \
         patch('app.backend.pipelines.retrieval_pipeline.Indexing'):

        mock_s3_instance = mock_s3.return_value
        mock_s3_instance.get_s3_object.return_value.read.return_value = b"test content"
        mock_s3_instance.upload_file.return_value = True

        test_file = io.BytesIO(b"test content")
        response = client.post(
            "/send_document",
            files={"doc": ("test.pdf", test_file)},
            params={"workspace_name": "test_workspace"},
            headers=auth_token
        )

    print("Response:", response.json())  # Debug print
    assert response.status_code == 200

def test_get_all_documents(mock_user, mock_db, auth_token):
    """Test getting all documents"""
    mock_docs = [
        Mock(
            filename="test.pdf",
            id=1,
            owner=mock_user,
            workspace=Mock(name="test_workspace")
        )
    ]
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = mock_docs

    with patch('app.backend.auth.utils.get_current_user', return_value=mock_user), \
         patch('app.backend.database.db.get_db', return_value=mock_db):

        response = client.get("/get_all", headers=auth_token)

    print("Response:", response.json())  # Debug print
    assert response.status_code == 200
    assert len(response.json()["documents"]) == 1

def test_get_document_by_id(mock_user, mock_db, auth_token):
    """Test getting document by ID"""
    mock_doc = Mock(file_path="test/path")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_doc

    with patch('app.backend.auth.utils.get_current_user', return_value=mock_user), \
         patch('app.backend.database.db.get_db', return_value=mock_db), \
         patch('app.backend.aws.s3.s3_wrapper.S3Wrapper') as mock_s3:
        mock_s3_instance = mock_s3.return_value
        mock_s3_instance.get_s3_object.return_value = b"test content"

        response = client.get("/get_document/1", headers=auth_token)

    print("Response:", response.json())  # Debug print
    assert response.status_code == 200
