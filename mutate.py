import os
from pathlib import Path
import shutil
import time
import subprocess


class Mutation:
    def __init__(self, file_path: str, temp_directory: str):
        self._check_file_existence(file_path=file_path)
        self._check_dir_existence(dir_path=temp_directory)

        self._file_path = file_path
        self._base_file_name = os.path.basename(self.file_path)

        self._temp_directory = temp_directory
        self._temp_file_name = None

    @property
    def file_path(self):
        return self._file_path

    @property
    def temp_directory(self):
        return self._temp_directory

    @property
    def temp_file_name(self):
        if self._temp_file_name is not None:
            return self._temp_file_name

        current_time = int(time.time() * 1000)
        self._temp_file_name = f"{current_time}_{self._base_file_name}"
        return self._temp_file_name

    def _check_file_existence(self, file_path, raise_exception=True):
        file = Path(file_path)
        if not file.is_file():
            if raise_exception:
                raise FileNotFoundError("Invalid file path.")
            else:
                return False
        return True

    def _check_dir_existence(self, dir_path, raise_exception=True):
        file = Path(dir_path)
        if not file.is_dir():
            if raise_exception:
                raise NotADirectoryError("Invalid directory path.")
            else:
                return False
        return True

    def _copy_a_file(self, origin_path, destination_dir, file_name):
        self._check_file_existence(file_path=origin_path)
        self._check_dir_existence(destination_dir)
        final_path = str(Path(destination_dir) / file_name)
        if self._check_file_existence(final_path, raise_exception=False):
            raise FileExistsError("The destination file is already exists.")

        shutil.copy2(origin_path, final_path)

    def _remove_a_file(self, file_path):
        self._check_file_existence(file_path=file_path)
        os.remove(file_path)

    def apply_mutation(
            self, start_line_number: int, start_index: int, end_line_number: int, end_index: int, replace_with: str
    ):
        """start_line_number and end_line_number are zero indexed."""
        if not start_line_number <= end_line_number:
            raise ValueError("")
        self._copy_a_file(
            origin_path=self.file_path, destination_dir=self.temp_directory, file_name=self.temp_file_name
        )

        with open(self.file_path, 'r') as file:
            file_contents = file.readlines()

        new_contents = []
        for i in range(len(file_contents)):
            if i < start_line_number or i > end_line_number:
                new_contents.append(file_contents[i])

            if i == start_line_number:
                start_line = file_contents[i][:start_index]
                start_line += replace_with
                new_contents.append(start_line)

            if i == end_line_number:
                end_line = file_contents[i][end_index:]
                new_contents.append(end_line)

        with open(self.file_path, 'w') as file:
            file.writelines(new_contents)

    def check_if_compilable(self, build_path):
        self._check_dir_existence(dir_path=build_path)
        command = f"make -C {build_path}"
        result = subprocess.run(command, shell=True)
        return True if result.returncode == 0 else False

    def undo_mutation(self):
        self._remove_a_file(self.file_path)
        temp_file_path = str(Path(self.temp_directory) / self.temp_file_name)
        self._copy_a_file(
            origin_path=temp_file_path, destination_dir=os.path.dirname(self.file_path), file_name=self._base_file_name
        )
        self._remove_a_file(file_path=temp_file_path)


if __name__ == "__main__":
    m = Mutation(
        file_path="/tmp/test/cmake-gtest-coverage-example/vendor/simple_vendor.cpp",
        temp_directory="/tmp/test/software_testing/tmp"
    )
    m.apply_mutation(
        start_line_number=14,
        start_index=24,
        end_line_number=14,
        end_index=26,
        replace_with='&&'
    )
    print(m.check_if_compilable("/tmp/test/cmake-gtest-coverage-example/build"))
    m.undo_mutation()
