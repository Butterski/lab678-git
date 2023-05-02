import sys
import json
import yaml
import xmltodict
import tkinter as tk
from tkinter import filedialog


class FileConverter: 
    def __init__(self, file_name, output_file_format):
        with open(file_name, 'r') as file:
            self.file_data = file.read()
        self.file_name = file_name
        self.file_format = self.detect_file_format(self.file_name)
        self.output_file_format = output_file_format

    def __str__(self) -> str:
        return f'{self.file_name} -> {self.output_file_format}'

    def update_output_file_format(self, output_file_format):
        self.output_file_format = output_file_format

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
        root = {'root': dict_object}
        return xmltodict.unparse(root, pretty=True)

    def dict_to_json(self, dict_object):
        return json.dumps(dict_object, indent=4)

    def dict_to_yaml(self, dict_object):
        return yaml.dump(dict_object)

    def convert(self):
        if (self.file_format == 'json' and self.is_json()):
            if (self.output_file_format == 'XML'):
                return self.dict_to_xml(self.json_object)
            elif (self.output_file_format == 'YAML'):
                return self.dict_to_yaml(self.json_object)
            elif (self.output_file_format == 'JSON'):
                return self.file_data
            else:
                return "Błąd konwersji."
        elif ((self.file_format == 'yaml' or self.file_format == 'yml') and self.is_yml()):
            if (self.output_file_format == 'XML'):
                return self.dict_to_xml(self.yml_object)
            elif (self.output_file_format == 'JSON'):
                return self.dict_to_json(self.yml_object)
            elif (self.output_file_format == 'YAML'):
                return self.file_data
            else:
                return "Błąd konwersji."
        elif (self.file_format == 'xml' and self.is_xml()):
            if (self.output_file_format == 'JSON'):
                return self.dict_to_json(self.xml_object)
            elif (self.output_file_format == 'YAML'):
                return self.dict_to_yaml(self.xml_object)
            elif (self.output_file_format == 'XML'):
                return self.file_data
            else:
                return "Błąd konwersji."
        else:
            return "Błąd konwersji."


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x800")
        self.root.title("File Converter - Miłosz 48755")

        self.label1 = tk.Label(
            self.root, text="Wybierz plik który chcesz zkonwertować:", font=("Arial", 18), pady=20)
        self.label1.pack()

        self.button = tk.Button(self.root, text="Wybierz plik", command=self.open_file_dialog, font=(
            "Arial", 16), border=3, bg="#a0a0a0", padx=20, pady=10)
        self.button.pack()

        self.file_path_text = tk.Label(self.root, text="", font=("Arial", 12))
        self.file_path_text.pack(pady=5)

        self.file_preview = tk.Text(self.root, height=10, width=50, font=(
            "Arial", 12), background="#2f2f2f", fg="#00ff00", borderwidth=5)
        self.file_preview.pack(pady=10)

        self.label2 = tk.Label(
            self.root, text="Wybierz format na który chcesz zamienić plik:", font=("Arial", 18), pady=20)
        self.label2.pack()

        self.selected_option = tk.StringVar()
        self.selected_option.set("JSON")

        self.options = ["JSON", "XML", "YAML"]
        self.option_menu = tk.OptionMenu(
            self.root, self.selected_option, *self.options, command=self.option_changed)
        self.option_menu.config(
            font=("Arial", 16), border=3, bg="#a0a0a0", padx=20, pady=10)
        self.option_menu.pack()

        self.output_preview = tk.Text(self.root, height=10, width=50, font=(
            "Arial", 12), background="#2f2f2f", fg="#00ff00", borderwidth=5)
        self.output_preview.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Zapisz", command=self.save_file_dialog, font=(
            "Arial", 16), border=3, bg="#a0a0a0", padx=20, pady=10)
        self.save_button.pack()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path != '':
            with open(file_path, "r") as file:
                self.file_data = file.read()
                self.file_preview.delete(1.0, tk.END)
                self.file_preview.insert(tk.END, self.file_data)

                self.fileConverter = FileConverter(
                    file_path, self.selected_option.get())
                self.output_preview.delete(1.0, tk.END)
                self.output_preview.insert(
                    tk.END, self.fileConverter.convert())

            self.file_path_text.config(text=file_path)

    def option_changed(self, *args):
        if self.fileConverter:
            self.output_preview.delete(1.0, tk.END)
            self.fileConverter.update_output_file_format(
                self.selected_option.get())
            self.output_preview.insert(tk.END, self.fileConverter.convert())

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=f'.{(self.selected_option.get()).lower()}', filetypes=[(self.selected_option.get(), f'*.{(self.selected_option.get()).lower()}')],
            initialfile='output', title="Zapisz plik"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.output_preview.get("1.0", "end"))


def main():
    root = tk.Tk(screenName="File Converter", baseName="File Converter")
    app = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
