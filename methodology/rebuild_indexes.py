import os
import re

FOLDERS = {
    "meta": "Meta index",
    "Bible": "Bible index",
    "PoE": "PoE index",
    "achievements": "Achievements index",
    "meta/accomplishments": "Accomplishments index",
    "deep research pipeline": "Deep research pipeline index",
    "inbox": "Inbox index"
}

def extract_date(filename, content):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match: return match.group(1)
    match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', content)
    if match: return match.group(1)
    return "Unknown Date"

def extract_title(filename, content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '): return line[2:].strip()
    name = filename.replace('.md', '').replace('-', ' ')
    name = re.sub(r'^\d{4} \d{2} \d{2}\s*', '', name)
    return name.title()

def extract_summary(content):
    match = re.search(r'Summary:\s*(.*)', content)
    if match: return match.group(1).strip()
    return ""

def extract_tags(content):
    match = re.search(r'Tags:\s*(.*)', content)
    if match: return match.group(1).strip()
    return ""

for folder, title in FOLDERS.items():
    if not os.path.exists(folder): continue
    entries = []
    for filename in os.listdir(folder):
        if not filename.endswith('.md') or filename == 'index.md': continue
        path = os.path.join(folder, filename)
        with open(path, 'r', encoding='utf-8') as f: content = f.read()
        entries.append({
            'date': extract_date(filename, content),
            'filename': filename,
            'title': extract_title(filename, content),
            'summary': extract_summary(content),
            'tags': extract_tags(content)
        })
    entries.sort(key=lambda x: x['date'], reverse=True)
    
    lines = [f"# {title}", "", f"This index tracks notes in `{folder}/`.", "", "## Entries (newest first)", ""]
    for e in entries:
        link = f"[{e['title']}](./{e['filename']})"
        line = f"- {e['date']} — {link}"
        if e['summary']: line += f" — {e['summary']}"
        lines.append(line)
        
    with open(os.path.join(folder, 'index.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
