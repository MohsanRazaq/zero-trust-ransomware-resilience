import os
import time


PROTECTED_PATH = "protected"


def simulate_mass_modification():

    print("[TEST] Starting mass modification simulation")

    test_file = os.path.join(PROTECTED_PATH, "test.txt")

    # Create file if missing
    with open(test_file, "w") as f:
        f.write("Initial content\n")

    # Simulate ransomware-like rapid modifications
    for i in range(10):

        try:

            with open(test_file, "a") as f:
                f.write(f"Encrypted block {i}\n")

            print(f"[TEST] Modified file iteration {i}")

            time.sleep(0.2)

        except PermissionError:

            print("[TEST] Attack blocked by ransomware resilience system")

            break

    print("[TEST] Mass modification simulation completed")


def simulate_extension_attack():

    print("[TEST] Starting extension attack simulation")

    original_file = os.path.join(PROTECTED_PATH, "victim.txt")

    locked_file = os.path.join(PROTECTED_PATH, "victim.txt.locked")

    # Create test file
    with open(original_file, "w") as f:
        f.write("Sensitive data")

    time.sleep(1)

    # Simulate ransomware rename
    os.rename(original_file, locked_file)

    print("[TEST] File renamed to suspicious extension")


if __name__ == "__main__":

    print("\n=== Attack Simulation Menu ===")
    print("1. Mass Modification Attack")
    print("2. Suspicious Extension Attack")

    choice = input("Select test: ")

    if choice == "1":

        simulate_mass_modification()

    elif choice == "2":

        simulate_extension_attack()

    else:

        print("[ERROR] Invalid selection")