import os
import sys
import time
import json
import matchmaker # Import Stage 4

# --- ANSI Color Codes ---
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    CLEAR = '\033[H\033[J'

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    __  __  _                           _      
   / / / / (_) _   __ ___   ___   _____| |__   
  / /_/ / / / | | / // _ \ / _ \ / ___/| '_ \  
 / __  / / /  | |/ //  __//  __/(__  ) | | | | 
/_/ /_/ /_/   |___/ \___/ \___//____/  |_| |_| 
                                               
      "THE SWARM IS READY TO COMPREHEND"
{Colors.END}
"""
    print(Colors.CLEAR + banner)

def get_cluster_stats():
    stats = {"nodes": 0, "capacity": 0.0, "status": "DORMANT"}
    if os.path.exists("node_profile.json"):
        with open("node_profile.json", "r") as f:
            p = json.load(f)
            stats["nodes"] = 1 # Simulation
            stats["capacity"] = p["net_capacity_gb"]
            stats["status"] = "AWAKE"
    return stats

def dashboard():
    s = get_cluster_stats()
    print(f"{Colors.BOLD}--- SWARM NERVOUS SYSTEM ---{Colors.END}")
    print(f"Nodes Synchronized : {Colors.GREEN}{s['nodes']}{Colors.END}")
    print(f"Collective Memory  : {Colors.CYAN}{s['capacity']} GB{Colors.END}")
    print(f"Cluster State      : {Colors.YELLOW}{s['status']}{Colors.END}")
    print("-" * 40)

def capture_intent():
    print(f"\n{Colors.BOLD}How should the swarm serve you?{Colors.END}")
    
    questions = [
        ("1", "Do you want me to reason with you?", "Reasoning"),
        ("2", "Do you want me to see for you?", "Vision"),
        ("3", "Do you want me to hear you?", "Audio"),
        ("4", "Do you want me to create for you?", "Creative"),
        ("Q", "Put the swarm to sleep.", "Quit")
    ]
    
    for key, q, desc in questions:
        print(f" [{Colors.YELLOW}{key}{Colors.END}] {Colors.BOLD}{q}{Colors.END}")
        print(f"     {Colors.CYAN}Capability: {desc}{Colors.END}")
    
    choice = input(f"\n{Colors.BOLD}Your command > {Colors.END}").upper()
    return choice

def main():
    while True:
        print_banner()
        dashboard()
        choice = capture_intent()
        
        if choice == 'Q':
            print(f"\n{Colors.YELLOW}The swarm recedes into the shadows...{Colors.END}")
            break
        elif choice in ['1', '2', '3', '4']:
            intents = {'1': "Reasoning", '2': "Vision", '3': "Audio", '4': "Creative"}
            intent = intents[choice]
            
            print(f"\n{Colors.GREEN}Searching for the largest possible intelligence...{Colors.END}")
            time.sleep(1)
            
            res = matchmaker.run_matchmaker(intent)
            if res and "error" not in res:
                print(f"\n{Colors.CYAN}{Colors.BOLD}MAXIMALIST RECOMMENDATION:{Colors.END}")
                print(f" {Colors.WHITE}Model       : {res['model']} ({res['params']}){Colors.END}")
                print(f" {Colors.WHITE}Quantization: {res['quant']}{Colors.END}")
                print(f" {Colors.WHITE}Memory Used : {res['ram_used']} GB{Colors.END}")
                print(f" {Colors.WHITE}Headroom    : {res['headroom']} GB{Colors.END}")
                
                confirm = input(f"\n{Colors.BOLD}Should I manifest this intelligence? (Y/N): {Colors.END}").upper()
                if confirm == 'Y':
                    print(f"\n{Colors.GREEN}Initiating Stage 5: Distributed Deployment...{Colors.END}")
                    time.sleep(2)
            else:
                print(f"{Colors.RED}No frontier models fit the current cluster capacity.{Colors.END}")
            
            input("\nPress Enter to return to the Hive...")
        else:
            print(f"{Colors.RED}The swarm does not understand that command.{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbruptly disconnecting...")
