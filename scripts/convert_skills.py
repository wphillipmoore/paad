import os
import re
from pathlib import Path

# Paths relative to repository root
SOURCE_DIR = "plugins/paad/skills"
TARGET_DIR = "kiro_and_antigravity/skills"

def convert_skills():
    # Detect root if possible, but assume relative to cwd
    kiro_skills_root = Path(TARGET_DIR) / ".kiro" / "skills"
    agent_skills_root = Path(TARGET_DIR) / ".agent" / "skills"
    
    kiro_skills_root.mkdir(parents=True, exist_ok=True)
    agent_skills_root.mkdir(parents=True, exist_ok=True)
    
    skip_names = ["makefile", "help"]
    unwanted_headers = ["Arguments", "Input Resolution", "Pre-flight Checks", "Document classification"]

    for skill_path in Path(SOURCE_DIR).iterdir():
        if not skill_path.is_dir() or skill_path.name in skip_names:
            continue
            
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            continue
            
        print(f"Converting {skill_path.name}...")
        
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract frontmatter for wrapper
        name_match = re.search(r"name:\s*(.*)", content)
        desc_match = re.search(r"description:\s*(.*)", content)
        skill_name = name_match.group(1).strip() if name_match else skill_path.name
        description = desc_match.group(1).strip() if desc_match else ""

        # Split into sections by headers (##)
        # We use a non-capturing group for the split but keep the header as part of the next chunk
        # Actually splitting by \n## works better if we prepend \n to content
        parts = re.split(r'\n(##+ .*)', content)
        
        # parts[0] is everything before the first ##
        cleaned_content = parts[0]
        
        # Process header/body pairs
        for i in range(1, len(parts), 2):
            header_line = parts[i]
            body = parts[i+1]
            
            header_text = re.sub(r'^##+\s*', '', header_line).strip()
            
            # Skip unwanted sections
            if any(uh in header_text for uh in unwanted_headers):
                continue
                
            # Neutralize "paad/" paths to ".reviews/" or ".reports/"
            body = body.replace("paad/architecture-reviews/", ".reviews/architecture/")
            body = body.replace("paad/code-reviews/", ".reviews/code/")
            body = body.replace("paad/pushback-reviews/", ".reviews/pushback/")
            body = body.replace("paad/alignment-reviews/", ".reviews/alignment/")
            body = body.replace("paad/", ".reviews/")
            
            # Remove entire lines containing /paad: (usually follow-up suggestions or command examples)
            body = re.sub(r'^.*\/paad:[a-z0-9-]+.*$', '', body, flags=re.MULTILINE)
            
            # Additional cleanup for any remaining /paad: mentions just in case
            body = re.sub(r'\(?/paad:[a-z0-9-]+\)?', '', body)
            
            # Clean up trailing whitespace and excessive newlines
            body = body.rstrip() + "\n"
            
            cleaned_content += "\n" + header_line + body
            
        # Final cleanup for consecutive empty lines
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content).strip() + "\n"
        
        # Write Kiro Skill
        kiro_skill_dir = kiro_skills_root / skill_path.name
        kiro_skill_dir.mkdir(exist_ok=True)
        with open(kiro_skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(cleaned_content)
            
        # Write Antigravity wrapper
        h1_match = re.search(r'^#\s*(.*)', cleaned_content, re.MULTILINE)
        title = h1_match.group(1).strip() if h1_match else skill_path.name.replace("-", " ").title()
        
        agent_skill_dir = agent_skills_root / skill_path.name
        agent_skill_dir.mkdir(exist_ok=True)
        
        wrapper = f"""---
name: {skill_name}
description: {description}
---

# {title} (Antigravity Wrapper)

This is a project-specific skill. The detailed checklist and procedures are in:
**`.kiro/skills/{skill_path.name}/SKILL.md`**

Please refer to that file for the full criteria.
"""
        with open(agent_skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(wrapper)

    print("Conversion complete.")

if __name__ == "__main__":
    convert_skills()
