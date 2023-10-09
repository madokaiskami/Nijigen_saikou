import re
import csv

def extract_user_and_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+the name of your groupchat \s+接收\s+(\w+):(.+)' # remember to modify this
        result = []
        for line in lines:
            match = re.match(pattern, line)
            if match:
                username = match.group(1)
                message = match.group(2)
                result.append((username, message))
        return result

def save_to_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Message'])
        for username, message in data:
            writer.writerow([username, message])

file_path = 'path_to_the_txt_file'  # replace it as the txt file you have exported
user_messages = extract_user_and_message(file_path)
csv_file_path = '../output'  # or any path you are intended
save_to_csv(user_messages, csv_file_path)
