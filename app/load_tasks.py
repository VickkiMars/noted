import re

pattern = re.compile(
    r'^(?P<task>.+?)\s+for\s+(?P<duration>\d+(?:\.\d+)?)\s*(?P<unit>min(?:s|utes)?|hr(?:s)?|hour(?:s)?)$',
    re.IGNORECASE
)

def parse_task(sentence):
    match = pattern.match(sentence.strip())
    if not match:
        print("The file content did not match the expected pattern. try --help for more information")
    
    task = match.group('task').strip()
    duration = float(match.group('duration'))
    unit = match.group('unit').lower()
    
    # convert to minutes
    if unit.startswith('hr') or unit.startswith('hour'):
        duration *= 60
    
    # return formatted string
    return [task, int(duration)]

def load_file(path):
    tasklist = []
    break_minutes = 1
    try:
        file = open(path, "r", encoding="utf-8")
    except FileNotFoundError as e:
        print(f"File Not Found, Please check the file path again")
    for line in file.readlines():
        line = line.strip()
        if line.lower().startswith("break="):
            try:
                break_minutes = int(line.split("=")[1])
            except Exception:
                pass
            continue
        line = line[alpha_pos(line):]
        print(line)
        if "an hour" in line:
            line = line.replace("an hour", "1 hour")
        task, duration = parse_task(line)
        tasklist.append((task, duration))

    return tasklist, break_minutes

def alpha_pos(string:str):
    for letter in string:
        if letter.isalpha():
            return string.index(letter)

if __name__ == "__main__":
    print(load_file("/home/kami/Desktop/codebase/noted/test.txt"))