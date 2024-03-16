import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

class XMLCache:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.xml_data = {}  # Stores valid XML data keyed by filename
        self.failed_files = []  # Stores filenames of XMLs that failed to load
        
        self._load_xml_files()

    def _load_xml_files(self):
        """Load and validate all XML files in the specified directory."""
        for filename in os.listdir(self.directory_path):
            if not filename.endswith('.xml'):
                continue
            
            file_path = os.path.join(self.directory_path, filename)
            try:
                # Attempt to parse the XML file (simple syntax validation)
                tree = ET.parse(file_path)
                # If parsing succeeds, store the XML data
                self.xml_data[filename.split('.')[0]] = ET.tostring(tree.getroot(), encoding='unicode')
                print(f"Loaded XML file successfully: {filename}")
            except ET.ParseError as e:
                print(f"Failed to load XML file: {filename} - Error: {e}")
                self.failed_files.append(filename)

    def get_xml_string(self, filename: str) -> Optional[str]:
        """Return the XML string for a given filename, if it exists and is valid."""
        return self.xml_data.get(filename)

    def list_failed_files(self) -> List[str]:
        """List filenames of all XML files that could not be loaded."""
        return self.failed_files

cache = XMLCache(f'{os.getcwd()}/../templates')

if __name__ == "__main__":
    # Example Usage
    # Initialize the XMLCache with the path to the directory containing your XML files.
    xml_cache = XMLCache("templates/")

    # Retrieve an XML string by filename (if it was loaded successfully)
    xml_string = xml_cache.get_xml_string("example.xml")
    if xml_string:
        print(xml_string)
    else:
        print("XML file not found or failed to load.")

    # List the names of all files that failed to load
    failed_files = xml_cache.list_failed_files()
    print("Failed files:", failed_files)
