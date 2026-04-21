import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestNutriQuest(unittest.TestCase):
    def test_high_score_healthy_choice(self):
        # Morning, Low Cognitive Load, Fasted
        response = client.post("/optimize-meal", json={
            "craving": "fried chicken",
            "circadian_rhythm": "morning",
            "cognitive_load": "low",
            "metabolic_state": "fasted"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_healthy"])
        self.assertGreater(data["score"], 80)
        self.assertEqual(data["original_craving"], "fried chicken")

    def test_low_score_risky_choice(self):
        # Late Night, High Cognitive Load, Recent Heavy Meal -> Donut
        response = client.post("/optimize-meal", json={
            "craving": "donut",
            "circadian_rhythm": "late_night",
            "cognitive_load": "high",
            "metabolic_state": "recent_heavy_meal"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_healthy"])
        self.assertLessEqual(data["score"], 80)
        self.assertIn("score", data)

    def test_unknown_craving(self):
        response = client.post("/optimize-meal", json={
            "craving": "something random",
            "circadian_rhythm": "morning",
            "cognitive_load": "low",
            "metabolic_state": "optimal"
        })
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "I'm not aware of this craving yet, but I'll look into it and update my database!")

if __name__ == "__main__":
    unittest.main()
