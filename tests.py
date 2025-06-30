import unittest

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_python import run_python_file
from config import MAX_CHARS

class TestGetFilesInfo(unittest.TestCase):
    
    def test_current_dir(self):
        result = get_files_info("calculator", ".")
        print("Results for current directory:")
        print(result)

    def test_valid_dir(self):
        result = get_files_info("calculator", "pkg")
        print("Results for 'pkg' directory:")
        print(result)

    def test_invalid_dir(self):
        result = get_files_info("calculator", "main.py")
        print("Results for 'main.py' file:")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")

    def test_unallowed_dir(self):
        result = get_files_info("calculator", "/bin")
        print("Results for '/bin' directory:")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")

    def test_unallowed_dir2(self):
        result = get_files_info("calculator", "../")
        print("Results for '../ directory:")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")

class TestGetFileContent(unittest.TestCase):
    
    def test_truncation(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertTrue(
            result.endswith(f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'),
            f"Should limit to {MAX_CHARS} chars"
        )
        self.assertLessEqual(
            len(result.strip(f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]')),
            MAX_CHARS
        )

    def test_normal_files(self):
        result = get_file_content("calculator", "main.py")
        print("Results for current 'main.py':")
        print(result)

        result = get_file_content("calculator", "pkg/calculator.py")
        print("Results for current 'pkg/calculator.py':")
        print(result)

    def test_unallowed_file(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")

class TestWriteFile(unittest.TestCase):
    
    def test_write_file(self):
        result = write_file("calculator", "lorem2.txt", "wait, this isn't lorem ipsum")
        print(result)
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)

    def test_unallowed_file(self):
        result = write_file("calculator", "/tmp/temp.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")
    
    def test_non_file(self):
        result = write_file("calculator", "pkg/", "lorem ipsum dolor sit amet")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")

class TestRunPython(unittest.TestCase):
    
    def test_run_file(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        result = run_python_file("calculator", "tests.py")
        print(result)

    def test_unallowed_file(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")
    
    def test_non_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertTrue(result.startswith("Error:"), "Should return error")


if __name__ == "__main__":
    unittest.main()