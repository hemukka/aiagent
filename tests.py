import unittest

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
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


if __name__ == "__main__":
    unittest.main()