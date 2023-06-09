import json
import os
from src.memorybuffer import MemoryBuffer
from src.text import Text
from src.cipher import Cipher
from src.enums.messages import Messages, FileMessages


class FileHandler:
    @staticmethod
    def save(file_name: str, memory_buffer: MemoryBuffer) -> None:
        """
        Method create json file

        """
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(memory_buffer.memory_buffer_to_dict(), file, ensure_ascii=False)

    @staticmethod
    def open(file_name: str) -> list:
        """
        Method open json file and save data to list

        """

        result = []
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        for i in data:
            if len(i.keys()) == 1:
                return i["txt"]
            else:
                text_obj = Text(i["txt"], i["rot_type"], i["status"])
                result.append(text_obj)
        return result

    @staticmethod
    def prepare_save(memory_buffer: MemoryBuffer) -> None:
        """
        Method which prepare data to save:
        1. Get the file name from the user
        2. Check if filename is not empty
        3. Check if filename exist
        4. Display what should be converted
        5. Save to file
        6. Clear memory_buffer

        """
        file_name = input(Messages.NAME_OF_FILE.value)
        if file_name == "":
            print(FileMessages.EMPTY_FILE_NAME.value)
            FileHandler.prepare_save(memory_buffer)
        file_name += ".json"
        file_exist: bool = FileHandler.check_file(file_name)
        if file_exist:
            FileHandler.override_file(file_name, memory_buffer)
        print(Messages.WHAT_TO_CONVERT.value)
        convert_option = input(Messages.CHOOSE_OPTION.value)
        Cipher.convert(memory_buffer, convert_option)
        FileHandler.save(file_name, memory_buffer)

    @staticmethod
    def check_file(file_name: str) -> bool:
        """
        Method which check did file exist

        """
        return os.path.isfile(file_name)

    @staticmethod
    def override_file(file_name: str, memory_buffer: MemoryBuffer) -> MemoryBuffer:
        """
        Method which call when filename exist in directory.
        When user want to add file into memory_buffer need to type 't'.
        Otherwise data of this file will override (file will be cleared) and memory_buffer will be added to created file.

        """
        choice = input(FileMessages.FILE_EXIST.value)
        if choice == "t":
            memory_buffer = FileHandler.append(file_name, memory_buffer)
        return memory_buffer

    @staticmethod
    def append(file_name: str, memory_buffer: MemoryBuffer) -> MemoryBuffer:
        """
        Method which add Text object into memory_buffer

        """
        data = FileHandler.open(file_name)
        for key, value in enumerate(data):
            memory_buffer.insert_to_memory_buffer(value, key)
        return memory_buffer
