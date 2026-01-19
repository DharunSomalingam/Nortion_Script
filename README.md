# Nortion_Script
# **Obsidian → Notion Sync**

A workflow to push Obsidian notes directly into Notion with a single click.

This system lets you send selected notes and unchecked tasks to Notion using a **single button inside each Obsidian note**. Everything runs through a Python backend, triggered via a shell script, QuickAdd, and Templater + Buttons plugins.

---

## **Goal**

Make it effortless for Obsidian users to:

- Export selected notes to a Notion Notes Repository Page.
- Sync unchecked to-dos to a Notion To-Do Database.
- Do it all with **one button** inside each note.

---

## **Core Features**

1. **Single Button Execution**
    
    A button inside each note (via plugins) triggers the entire sync.
    
2. **Markdown → Notion Sync**
    
    Converts your notes into Notion blocks, preserving headings, bold text, lists, and paragraphs.
    
3. **To-Do Sync**
    
    Sends unchecked tasks to a dedicated Notion To-Do Database.
    

---

## **Setup & Configuration**

The workflow uses Python, shell scripts, and a few Obsidian plugins.

### **1. Required Files**

Create a `.env` file in your project folder:

```
NOTION_TOKEN=secret_xxx
NOTION_NOTES_PAGE_ID=xxxxxxxxxxxx
NOTION_TODO_DATABASE_ID=xxxxxxxxxxxx
VAULT_PATH=/path/to/your/obsidian/vault

```

## **2. Get Your Notion Token**

1. Go to [Notion Integrations](https://www.notion.com/my-integrations).
2. Click **+ New Integration**.
3. Select your workspace.
4. Enable the following permissions:
    - Read Content
    - Update Content
    - Insert Content
5. Click **Submit** and copy your internal integration token.

```
NOTION_TOKEN=secret_xxx

```

## **3. Find Page and Database IDs**

You need:

- **A Notion Page** → where your notes will go.
- **A Notion Database** → for syncing tasks.

To get the IDs:

1. Open the page or database in Notion.
2. Copy the URL.
3. The ID is the 32-character string in the link.

Example:

```
https://www.notion.so/workspace/Notes-Repo-xxxxxxxxxxxxxxxxxxxx?pvs=4

```

---

## **4. How It Runs**

You trigger the workflow through:

- Shell Script
- QuickAdd Macro
- Buttons Plugin
- Templater Plugin (to automatically add the button in new notes)

### **4a. Shell Script**

Create `run_notion.sh`:

```bash

#!/bin/bash

# Pass all arguments to the Python script
python3 {path_to_your_project}/Notion_Script/main.py "$@"

```

To run the script:

```
sh {path_to_your_project}/run_notion.sh "{{file_name}}"
```

![image.png](attachment:fc52f1b0-ceb9-471c-b139-051fccb01737:image.png)

This passes the current file name to Python.

### **4b. QuickAdd Macro**

1. Install the **QuickAdd** plugin.
2. Create a macro called **Sync Notion**.
3. Configure it to run the shell command **Notion_RUN**.
4. Once enabled, it will show:

Shell commands: Execute: Notion_RUN

![image.png](attachment:a2437214-d681-44d3-acf1-0b9c5073f6d1:image.png)

---

### **4c. Buttons Plugin**

1. Install and enable the **Buttons** plugin.
2. Create a template named `buttonTemplate`.
3. Paste this code:

```markdown
```button
name Convert to Notion
type command
action QuickAdd: Sync Notion
color blue
```




### **4d. Templater Plugin**

1. Install and enable the **Templater** plugin.
2. In settings, enable **Trigger template on new file creation**.
3. Set your template folder to `/` and select `buttonTemplate.md`.

![image.png](attachment:da1e74a5-ce8c-446e-98ce-d460c9330689:image.png)

This automatically adds the **"Convert to Notion"** button in every new note.

![image.png](attachment:2c372be9-134e-4335-9c88-a8653fc756a3:image.png)

## **Quick Summary**

- **Goal:** Instantly push Obsidian notes and tasks to Notion using a single button inside each note.
- **Core Tools:**
    - Python script to sync notes and tasks.
    - Shell script (`run_notion.sh`) to trigger Python.
    - **QuickAdd** plugin to run the shell script.
    - **Buttons** plugin to create a clickable button in notes.
    - **Templater** plugin to automatically add the button to new notes.
- **Setup Steps:**
    1. Configure `.env` with your Notion token, page ID, database ID, and vault path.
    2. Install QuickAdd, Buttons, and Templater plugins in Obsidian.
    3. Create a QuickAdd macro to execute the shell script.
    4. Add a button template (`buttonTemplate.md`) with action to run the macro.
    5. Enable Templater to auto-add the button in every new note.
- **Usage:**
    
    Click the **Convert to Notion** button in any note to sync it directly to Notion.
    
- **Deliverables:**
    - Fully working Python script.
    - Shell runner (`run_notion.sh`).
    - `.env.example` config file.
    - README instructions.
    - Automated button in all notes.
