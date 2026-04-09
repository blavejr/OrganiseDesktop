import os
from environment import setup_environment
from organise_desktop.Clean import clean_desktop


def main():
    print("--- Desktop Organiser Starting ---")

    # 1. Prepare the environment (Create folders, etc.)
    try:
        setup_environment()
        print("Environment check: OK")
    except Exception as exception:
        print(f"Warning: Setup encountered an issue: {exception}")

    # 2. Launch the GUI
    print("Launching interface...")
    clean_desktop()


if __name__ == "__main__":
    main()
