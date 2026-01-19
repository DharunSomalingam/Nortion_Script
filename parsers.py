import re


# ---------------------------
#  Extract unfinished todos
# ---------------------------
def extract_todos(md_text):
    return re.findall(r"-\[\]\s*(.+)", md_text)


# ---------------------------
#  Inline Bold Parser
# ---------------------------
def parse_inline_bold(text):
    """
    Convert text with inline **bold** into Notion rich_text elements.
    Supports multiple bold segments.
    """
    parts = []
    pattern = r"\*\*(.*?)\*\*"
    last_end = 0

    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            parts.append({
                "type": "text",
                "text": {"content": text[last_end:match.start()]}
            })

        parts.append({
            "type": "text",
            "text": {"content": match.group(1)},
            "annotations": {"bold": True}
        })

        last_end = match.end()

    if last_end < len(text):
        parts.append({
            "type": "text",
            "text": {"content": text[last_end:]}
        })

    return parts


# ---------------------------
#  Convert Markdown → Notion Blocks
# ---------------------------
def md_to_notion_block(md_text):
    lines = md_text.split("\n")
    blocks = []

    skip_block = False  # for detecting ```button blocks

    for line in lines:
        stripped = line.strip()

        # ======================================
        # REMOVE OBSIDIAN BUTTON BLOCK
        # ======================================
        if stripped.startswith("```button"):
            skip_block = True
            continue

        if skip_block:
            if stripped.startswith("```"):
                skip_block = False
            continue

        # ======================================
        # HEADINGS
        # ======================================
        if stripped.startswith("# ") and not stripped.startswith("## "):
            blocks.append({
                "type": "heading_1",
                "heading_1": {"rich_text": parse_inline_bold(stripped[2:].strip())}
            })
            continue

        elif stripped.startswith("## "):
            blocks.append({
                "type": "heading_2",
                "heading_2": {"rich_text": parse_inline_bold(stripped[3:].strip())}
            })
            continue

        elif stripped.startswith("### "):
            blocks.append({
                "type": "heading_3",
                "heading_3": {"rich_text": parse_inline_bold(stripped[4:].strip())}
            })
            continue

        # ======================================
        # FULL LINE BOLD
        # ======================================
        full_bold = re.fullmatch(r"\*\*(.*?)\*\*", stripped)
        if full_bold:
            blocks.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": full_bold.group(1)},
                            "annotations": {"bold": True}
                        }
                    ]
                }
            })
            continue

        # ======================================
        # BULLETED LIST
        # ======================================
        if re.match(r"^- +", stripped) and not stripped.startswith("-[]"):
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": parse_inline_bold(stripped[2:].strip())
                }
            })
            continue

        # ======================================
        # DEFAULT PARAGRAPH
        # ======================================
        blocks.append({
            "type": "paragraph",
            "paragraph": {"rich_text": parse_inline_bold(stripped)}
        })

    return blocks


# ---------------------------
#  CLEAN INVALID BLOCKS
# ---------------------------
def clean_notion_blocks(blocks):
    valid_blocks = []

    for b in blocks:
        block_type = b.get("type")
        if not block_type:
            continue

        content = b.get(block_type)
        if not content or not content.get("rich_text"):
            continue

        valid_blocks.append(b)

    return valid_blocks
