import re

def extract_scripts_from_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Read the binary 
            binary_content = file.read()
            
            # Decode the binary content into a string (assuming UTF-8 encoding)
            html_content = binary_content.decode('utf-8', errors='ignore')
            
            # Find between <script> and </script>
            script_pattern = r'<script.*?>(.*?)</script>'
            
            # Find all matches
            scripts = re.findall(script_pattern, html_content, re.DOTALL)
            
            return scripts
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Get file path 
file_path = input("Please enter the path to the HTML file: ")

# Extract 
scripts = extract_scripts_from_file(file_path)

if scripts:
    for i, script in enumerate(scripts, 1):
        print(f"Script {i}:")
        print(script)
        print("---------")
else:
    print("No scripts found.")
