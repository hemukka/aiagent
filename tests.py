import unittest

from functions.get_files_info import get_files_info

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
        

if __name__ == "__main__":
    unittest.main()