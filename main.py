import sys
import json
import yaml
import xmltodict


class FileConverter:
    def __init__(self, file_name, output_file_name):
        with open(sys.argv[1], 'r') as file:
            self.file_data = file.read()
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.file_format = self.detect_file_format(self.file_name)
        self.output_file_format = self.detect_file_format(
            self.output_file_name)

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
            self.json_object = json.loads(self.file_data)
        except ValueError as e:
            return False
        return True

    def is_yml(self) -> bool:
        try:
            self.yml_object = yaml.load(self.file_data, Loader=yaml.SafeLoader)
        except ValueError as e:
            return False
        return True

    def is_xml(self) -> bool:
        try:
            self.xml_object = xmltodict.parse(self.file_data)
        except:
            return False
        return True

    def dict_to_xml(self, dict_object):
        return xmltodict.unparse(dict_object, pretty=True)

    def dict_to_json(self, dict_object):
        return json.dumps(dict_object, indent=4)

    def dict_to_yaml(self, dict_object):
        return yaml.dump(dict_object)

    def convert(self):
        output_file = open(self.output_file_name, "w")

        if (self.file_format == 'json' and self.is_json()):
            print(self.json_object)
            if (self.output_file_format == 'xml'):
                output_file.write(self.dict_to_xml(self.json_object))
            elif (self.output_file_format == 'yaml'):
                output_file.write(self.dict_to_yaml(self.json_object))
            else:
                print("Nieprawidłowy format pliku wyjściowego.")
                sys.exit(1)
        elif ((self.file_format == 'yaml' or self.file_format == 'yml') and self.is_yml()):
            print(self.yml_object)
            if (self.output_file_format == 'xml'):
                output_file.write(self.dict_to_xml(self.yml_object))
            elif (self.output_file_format == 'json'):
                output_file.write(self.dict_to_json(self.yml_object))
            else:
                print("Nieprawidłowy format pliku wyjściowego.")
                sys.exit(1)
        elif (self.file_format == 'xml' and self.is_xml()):
            print(self.xml_object)
            if (self.output_file_format == 'json'):
                output_file.write(self.dict_to_json(self.xml_object))
            elif (self.output_file_format == 'yaml'):
                output_file.write(self.dict_to_yaml(self.xml_object))
            else:
                print("Nieprawidłowy format pliku wyjściowego.")
                sys.exit(1)
        else:
            print("Nieprawidłowy format pliku wejściowego.")
            sys.exit(1)
        output_file.close()


def main():
    if len(sys.argv) < 3:
        print("Podaj nazwę pliku wejściowego i wyjściowego.")
        sys.exit(1)
    elif (len(sys.argv) == 3):
        fileConverter = FileConverter(sys.argv[1], sys.argv[2])
        fileConverter.convert()
    else:
        print("Podano za dużo argumentów.")
        sys.exit(1)


if __name__ == "__main__":
    main()
