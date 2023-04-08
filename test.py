file_path = r"\\192.168.0.9\Snort\rules\user.rules"
content = ''

try:
    with open(file_path, 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found. Please check the file path and ensure the network drive is connected.")

print(content)