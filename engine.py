# =====================================================================
# Copyright (c) 2026 TheFuturistsStrategyCone. All rights reserved.
# Proprietary Framework - Protected under International Copyright Laws.
# For educational and research use only. Commercial use is prohibited.
# =====================================================================

import json
import os
import sys

class FuturistsStrategyConeEngine:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config_data = self.load_configuration()
        print("[INIT] The Futurist's Strategy Cone Framework Initialized successfully.")

    def load_configuration(self):
        """Loads and parses the framework parameter profiles from JSON."""
        if not os.path.exists(self.config_path):
            print(f"[ERROR] Strategy config file missing at: {self.config_path}")
            sys.exit(1)
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as err:
            print(f"[ERROR] Invalid strategy JSON schema syntax: {err}")
            sys.exit(1)

    def validate_agent_action(self, action_type, asset_class, amount_usd):
        """
        Enforces Strategy Cone boundaries before any action can reach execution stage.
        Returns a dictionary containing authorization status and required workflows.
        """
        boundaries = self.config_data.get("decision_boundaries", {})
        controls = self.config_data.get("execution_controls", {})
        
        print(f"\n[EVALUATING ACTION] Intended Action: {action_type} | Asset: {asset_class} | Value: ${amount_usd}")

        # 1. Rule Check: Allowed Asset Classes
        if asset_class not in boundaries.get("allowable_asset_classes", []):
            return {
                "status": "REJECTED",
                "reason": f"Asset class '{asset_class}' falls outside the Strategy Cone allowed boundaries."
            }

        # 2. Rule Check: Absolute Hard Transaction Caps
        if amount_usd > boundaries.get("max_transaction_limit_usd", 0):
            return {
                "status": "REJECTED",
                "reason": f"Transaction amount ${amount_usd} violates maximum strategy cap of ${boundaries.get('max_transaction_limit_usd')}."
            }

        # 3. Control Check: Human In The Loop (HITL) Threshold
        if controls.get("human_in_the_loop_required", True):
            if amount_usd >= controls.get("hitl_trigger_threshold_usd", 0):
                return {
                    "status": "PENDING_APPROVAL",
                    "reason": f"Requires manual administrator overview. Value exceeds Human-in-the-Loop limit of ${controls.get('hitl_trigger_threshold_usd')}."
                }

        return {
            "status": "APPROVED",
            "reason": "Action fully aligns with core Strategic Operating Model parameters."
        }

# --- Quick Execution Framework Demonstration ---
if __name__ == "__main__":
    # Engine instantiation
    engine = FuturistsStrategyConeEngine()

    # Scenario A: Passing Case (Within limits)
    case_a = engine.validate_agent_action("BUY", "ETFs", 1200.00)
    print(f"Result Case A: {case_a['status']} -> {case_a['reason']}")

    # Scenario B: Human Over-rule Verification Pending Case
    case_b = engine.validate_agent_action("BUY", "Treasury_Bonds", 3100.00)
    print(f"Result Case B: {case_b['status']} -> {case_b['reason']}")

    # Scenario C: Strictly Blocked Violation Case
    case_c = engine.validate_agent_action("BUY", "High_Leverage_Crypto", 4500.00)
    print(f"Result Case C: {case_c['status']} -> {case_c['reason']}")
