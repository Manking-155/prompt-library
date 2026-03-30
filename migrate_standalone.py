import os
import shutil
import datetime

base_dir = '/Volumes/Workspace/0-Working/bkplus/master_prompt'
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Create structure
for d in ['prompts/agents', 'prompts/skills', 'prompts/workflows', 'prompts/experiments',
          'inboxes/archive', 'inboxes/raw_data', 'docs', '.templates']:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

def generate_yaml(name, category):
    return f"""---
name: "{name}"
category: {category}
version: 1.0.0
date_updated: {today}
---

"""

def move_any(src, dest_folder):
    if not os.path.exists(src):
        return
    dest_path = os.path.join(dest_folder, os.path.basename(src))
    shutil.move(src, dest_path)

def move_and_append_yaml(src, dest_folder, category):
    if not os.path.exists(src):
        return
    if os.path.isdir(src):
        for root, _, files in os.walk(src):
            for f in files:
                if f.startswith('.'): continue
                abs_src = os.path.join(root, f)
                dest_file = os.path.join(dest_folder, f)
                
                # Check target file doesn't already exist or handle safely
                if os.path.exists(dest_file):
                    continue
                
                if f.endswith('.md'):
                    with open(abs_src, 'r', encoding='utf-8') as file:
                        c = file.read()
                    if not c.startswith('---'):
                        name = os.path.splitext(f)[0]
                        c = generate_yaml(name, category) + c
                    with open(dest_file, 'w', encoding='utf-8') as file:
                        file.write(c)
                    os.remove(abs_src)
                else:
                    shutil.move(abs_src, dest_file)
        
        # Cleanup old dir safely
        try:
            shutil.rmtree(src)
        except Exception:
            pass
    else:
        f = os.path.basename(src)
        dest_file = os.path.join(dest_folder, f)
        if f.endswith('.md'):
            with open(src, 'r', encoding='utf-8') as file:
                c = file.read()
            if not c.startswith('---'):
                name = os.path.splitext(f)[0]
                c = generate_yaml(name, category) + c
            with open(dest_file, 'w', encoding='utf-8') as file:
                file.write(c)
            os.remove(src)
        else:
            shutil.move(src, dest_file)

def process_root():
    items = os.listdir(base_dir)
    for item in items:
        if item in ['.git', 'prompts', 'inboxes', 'docs', '.templates', 
                   'migrate_standalone.py', '.claudeignore', '.gitignore', 'README.md']:
            continue
            
        src_path = os.path.join(base_dir, item)
        
        if item.startswith('1 Agents'):
            move_and_append_yaml(src_path, os.path.join(base_dir, 'prompts/agents'), 'Agent')
        elif item.startswith('1 Skills'):
            move_and_append_yaml(src_path, os.path.join(base_dir, 'prompts/skills'), 'Skill')
        elif item.startswith('workflows'):
            move_and_append_yaml(src_path, os.path.join(base_dir, 'prompts/workflows'), 'Workflow')
        elif item in ['meta', 'guidelines', 'sops', 'meta.md'] or 'notebooklm' in item:
            move_any(src_path, os.path.join(base_dir, 'docs'))
        elif item == 'openai-prompts-multi.csv':
            move_any(src_path, os.path.join(base_dir, 'inboxes/raw_data'))
        else:
            move_any(src_path, os.path.join(base_dir, 'inboxes/archive'))

process_root()
print("Internal Migration to Standalone Repo Done!")
