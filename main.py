from src.assistant import PersonalAI

if __name__ == "__main__":
    try:
        PersonalAI().run()
    except KeyboardInterrupt:
        print("Interrupted by user")
