import context
from document.document import SUPPORTED_DOCUMENTS

def test_supported_documents():
    assert '.jpg' in SUPPORTED_DOCUMENTS
    assert '.png' in SUPPORTED_DOCUMENTS