# Quick Start Guide

## Running the Design Document Generator

### Option 1: Interactive Mode (Recommended)

```bash
python3 design_doc_generator.py
```

Follow the prompts to create your design document.

### Option 2: Direct Execution

```bash
./design_doc_generator.py
```

### What to Expect

1. **Mandatory questions** (required):
   - Project name
   - One-line description
   - Primary audience

2. **Optional questions** (press Enter to skip):
   - Goals & success metrics
   - Stakeholders & roles
   - Tech stack
   - Non-functional requirements
   - Security concerns
   - Timeline
   - Budget constraints

3. **Output**:
   - A markdown file named `{project_name}_design_doc.md`
   - Ready to edit and share

## Example Output

See `example_design_doc.md` for a complete sample output.

## Tips

- **Be specific**: More details = better document
- **Skip optionals**: You can always edit the output later
- **Use placeholders**: The tool adds placeholders for diagrams and details
- **Iterate**: Generate, review, and run again if needed

## Next Steps After Generation

1. Review the generated document
2. Fill in placeholders and add diagrams
3. Add specific technical details
4. Share with your team for feedback
5. Update the revision history as you make changes

## Customization

Edit `design_doc_generator.py` to:
- Add/remove sections
- Change question prompts
- Modify output format
- Add company-specific templates
