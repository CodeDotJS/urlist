import json

file_path = "output.json"
output_file_path = "output.txt"

with open(file_path, "r") as file:
    data = json.load(file)

# Extract URLs from the data
urls = []
for website_data in data:
    urls.extend(website_data["urls"])

# Save URLs to a text file
with open(output_file_path, "w") as output_file:
    for url in urls:
        output_file.write(url + "\n")

print("URLs saved to:", output_file_path)
