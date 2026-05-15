import json
import time
import random
import threading

class HyveyeshGateway:
    def __init__(self):
        self.active_shards = {}
        self.is_healthy = True
        self.node_states = {}

    def start_self_healing_loop(self):
        """Background thread to monitor node heartbeat."""
        def monitor():
            while self.is_healthy:
                print("\n[🩺] Swarm Health Check...")
                for node_id in list(self.node_states.keys()):
                    # Simulate a 5% chance of node failure for demo/testing
                    if random.random() < 0.05:
                        print(f"[🚨] NODE FAILURE DETECTED: {node_id}")
                        self.trigger_emergency_reshard(node_id)
                time.sleep(10)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def trigger_emergency_reshard(self, failed_node):
        """Logic to migrate sharded layers to healthy nodes."""
        print(f"[🛠] SELF-HEALING: Migrating layers from {failed_node} to available nodes...")
        # In a real scenario, this calls Stage 5 distributor.shard_model()
        time.sleep(2)
        print(f"[✅] SWARM RE-STABILIZED. All sharded layers accounted for.")

    def unified_inference(self, prompt):
        """Simulates the FastAPI endpoint call to the distributed swarm."""
        print(f"\n[🧠] SWARM THINKING: {prompt}")
        print(f"[📡] Sharding request to {len(self.node_states)} nodes...")
        time.sleep(1)
        return "This is a simulated response from the sharded Hyveyesh swarm (Llama-3.1 405B)."

    def register_node(self, node_id, status="ONLINE"):
        self.node_states[node_id] = status
        print(f"[+] Node {node_id} added to the Hive Gateway.")

if __name__ == "__main__":
    print("--- Hyveyesh Stage 6: Exit Gateway & Self-Healing ---")
    gateway = HyveyeshGateway()
    
    # Register some dummy nodes
    gateway.register_node("LAB-NODE-01")
    gateway.register_node("LAB-NODE-02")
    gateway.register_node("LAB-NODE-03")
    
    gateway.start_self_healing_loop()
    
    # Test Inference
    response = gateway.unified_inference("What is the meaning of life, the universe, and everything?")
    print(f"\n[Output] > {response}")
    
    # Keep alive for healing demo
    print("\n[!] Self-healing loop active. Monitoring nodes... (Press Ctrl+C to exit)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGateway shutting down.")
