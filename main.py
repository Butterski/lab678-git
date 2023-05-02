import sys

def detect_file_format(file_name):
    if file_name.endswith(".xml"):
        return 'xml'
    elif file_name.endswith(".json"):
        return 'json'
    elif file_name.endswith(".yml") or file_name.endswith(".yaml"):
        return 'yaml'
    else:
        return "Nieprawidłowy format pliku."

def main():
    if len(sys.argv) < 3:
        print("Podaj nazwę pliku wejściowego i wyjściowego.")
        sys.exit(1)
    elif(len(sys.argv) == 3):
        print(f'Format twojego pliku wejsciowego to - {detect_file_format(sys.argv[1])}')
        print(f'Format twojego pliku wyjsciowego to - {detect_file_format(sys.argv[2])}')
    else:
        print("Podano za dużo argumentów.")
        sys.exit(1)
    

if __name__ == "__main__":
    main()