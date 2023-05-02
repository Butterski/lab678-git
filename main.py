import sys
import json
import yaml

class FileConverter:
    def __init__(self, file_name, output_file_name):
        with open(sys.argv[1], 'r') as file:
            self.file_data = file.read()
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.file_format = self.detect_file_format(self.file_name)
        self.output_file_format = self.detect_file_format(self.output_file_name)
    
    def __str__(self) -> str:
        return f'{self.file_name} -> {self.output_file_name}'

    def detect_file_format(self, filename):
        if filename.endswith(".xml"):
            return 'xml'
        elif filename.endswith(".json"):
            return 'json'
        elif filename.endswith(".yml") or filename.endswith(".yaml"):
            return 'yaml'
        else:
            return "Nieprawidłowy format pliku."

    def is_json(self) -> bool:
        try:
            json_object = json.loads(self.file_data)
        except ValueError as e:
            return False
        return True
    
    def is_yml(self) -> bool:
        try:
            yml_object = yaml.load(self.file_data, Loader=yaml.SafeLoader)
        except ValueError as e:
            return False
        return True
    
    def convert(self):
        print('bip bop converting')

def main():
    if len(sys.argv) < 3:
        print("Podaj nazwę pliku wejściowego i wyjściowego.")
        sys.exit(1)
    elif(len(sys.argv) == 3):
        fileConverter = FileConverter(sys.argv[1], sys.argv[2])
        print(fileConverter.is_yml())
    else:
        print("Podano za dużo argumentów.")
        sys.exit(1)
    

if __name__ == "__main__":
    main()