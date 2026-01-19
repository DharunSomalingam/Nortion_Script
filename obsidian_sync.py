import os
from notion_client import Client
from dotenv import load_dotenv

from parsers import md_to_notion_block  # your markdown → Notion converter

load_dotenv()

# Load environment variables
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_TODO_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)


# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def chunk_blocks(blocks, size=100):
    """Split block list into chunks (Notion only allows 100 children at once)."""
    for i in range(0, len(blocks), size):
        yield blocks[i:i + size]


def create_page(title):
    """Create a new page in the target database."""
    page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "title": [
                {"text": {"content": title}}
            ]
        }
    )
    return page["id"]


# ---------------------------------------------------
# Sync a single file
# ---------------------------------------------------

def sync_single_file(file_path):
    """Send only ONE Obsidian file to Notion."""
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return 0

    if not file_path.endswith(".md"):
        print(f"[ERROR] Not a markdown file: {file_path}")
        return 0

    # Read the markdown
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown → Notion blocks
    blocks = md_to_notion_block(md_text)

    # Use file name as page title
    title = os.path.basename(file_path).replace(".md", "")
    page_id = create_page(title)

    # Upload blocks in chunks of 100
    for chunk in chunk_blocks(blocks):
        notion.blocks.children.append(page_id, children=chunk)

    return 1


# ---------------------------------------------------
# Sync full vault
# ---------------------------------------------------

def sync_obsidian_notes(vault_path):
    """Send all markdown notes in entire vault to Notion."""
    notes_sent = 0

    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if not file.endswith(".md"):
                continue

            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            blocks = md_to_notion_block(md_text)

            title = file.replace(".md", "")
            page_id = create_page(title)

            for chunk in chunk_blocks(blocks):
                notion.blocks.children.append(page_id, children=chunk)

            notes_sent += 1

    return notes_sent
