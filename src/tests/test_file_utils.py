import unittest
from pathlib import Path
import tempfile
import json
from src.modules.file_utils import read_json_file, write_json_file, ensure_directory_exists, get_json_files_in_directory, increment_json_field

class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def test_read_write_json_file(self):
        test_data = {"key": "value"}
        file_path = self.temp_path / "test.json"
        write_json_file(file_path, test_data)
        read_data = read_json_file(file_path)
        self.assertEqual(test_data, read_data)

    def test_ensure_directory_exists(self):
        new_dir = self.temp_path / "new_dir"
        ensure_directory_exists(new_dir)
        self.assertTrue(new_dir.is_dir())

    def test_get_json_files_in_directory(self):
        write_json_file(self.temp_path / "file1.json", {})
        write_json_file(self.temp_path / "file2.json", {})
        write_json_file(self.temp_path / "file3.txt", {})
        json_files = get_json_files_in_directory(self.temp_path)
        self.assertEqual(len(json_files), 2)
        self.assertTrue(all(f.suffix == '.json' for f in json_files))

    def test_increment_json_field(self):
        file_path = self.temp_path / "counter.json"
        write_json_file(file_path, {"count": 0})
        updated_data = increment_json_field(file_path, "count")
        self.assertEqual(updated_data["count"], 1)
        updated_data = increment_json_field(file_path, "count", 2)
        self.assertEqual(updated_data["count"], 3)

if __name__ == '__main__':
    unittest.main()
