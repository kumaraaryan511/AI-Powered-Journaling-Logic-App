from score import score

def main():
    print("Give me some text!  (Press Ctrl+C to exit)")
    while True:
        try:
            text = input("> ").strip()
            if not text:
                continue
            result = score(text)
            if result > 0.8:
                print("Very Happy")
            elif result > 0.5:
                print("Happy")
            elif result > 0.2:
                print("Moderately Happy")
            elif result > 0:
                print("Neutral / A little happy")
            elif result > -0.2:
                print("Neutral / A little Sad")
            elif result > -0.5:
                print("Moderately Sad")
            elif result > -0.8:
                print("Sad")
            else:
                print("Really Sad")
            #print(result)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
