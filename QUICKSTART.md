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

3. **Artifact ingestion** (optional):
   - Import text files (requirements, specs, docs)
   - Paste multiline text directly
   - Files are included in document appendix

4. **Output**:
   - A markdown file named `{project_name}_design_doc.md`
   - Option to display for direct copy-paste
   - Ready to edit and share or paste into wiki

## Example Output

See `example_design_doc.md` for a complete sample output.

## Tips

- **Be specific**: More details = better document
- **Skip optionals**: You can always edit the output later
- **Import files**: Add existing requirements, specs, or documentation
- **Paste text**: Use multiline text input for quick context
- **Copy to wiki**: Choose 'y' to display output for easy copy-paste
- **Use placeholders**: The tool adds placeholders for diagrams and details
- **Iterate**: Generate, review, and run again if needed

## Artifact Ingestion

When prompted "Add artifact?":
- Type `f` to import a file (supports .txt, .md, .json, .yaml, etc.)
- Type `t` to paste multiline text (end with 'END' on new line)
- Type `s` to skip and proceed

Artifacts are:
- Summarized in the Overview section
- Included in full in the Appendix
- Useful for incorporating existing materials

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
