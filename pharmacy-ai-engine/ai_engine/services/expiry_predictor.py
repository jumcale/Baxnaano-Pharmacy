from __future__ import annotations

from typing import Dict, List


class ExpiryPredictionService:
    def evaluate_batches(self, medicine: str, batches: List[Dict]) -> Dict:
        risk_score = 0
        for batch in batches:
            quantity = batch.get("quantity", 0)
            days_to_expiry = batch.get("days_to_expiry", 0)
            if days_to_expiry <= 0:
                risk_score += quantity * 2
            elif days_to_expiry <= 30:
                risk_score += quantity

        if risk_score > 200:
            risk = "high"
            confidence = 0.9
        elif risk_score > 100:
            risk = "medium"
            confidence = 0.75
        else:
            risk = "low"
            confidence = 0.6

        return {"medicine": medicine, "expiry_risk": risk, "confidence": confidence, "batches": batches}
