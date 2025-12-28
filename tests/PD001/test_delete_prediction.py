import unittest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, init_db

client = TestClient(app)


class TestDeletePrediction(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize test database"""
        init_db()
    
    def create_sample_image(self):
        """Load beatles.jpeg test image"""
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'beatles.jpeg')
        with open(image_path, 'rb') as f:
            return BytesIO(f.read())
    
    def create_prediction(self):
        """Create a prediction and return its UID"""
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", self.create_sample_image(), "image/jpeg")}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["prediction_uid"]
    
    def test_delete_prediction(self):
        """Test DELETE /prediction/{uid}"""
        uid = self.create_prediction()
        response = client.delete(f"/prediction/{uid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"uid": uid})
        
        # Verify prediction is deleted
        get_response = client.get(f"/prediction/{uid}")
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_prediction_not_found(self):
        """Test DELETE /prediction/{uid} with non-existent UID"""
        response = client.delete("/prediction/non-existent-uid")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
