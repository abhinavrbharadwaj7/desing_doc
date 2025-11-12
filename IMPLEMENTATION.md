# Agent Implementation Notes

This repository contains both the **agent definition** and the **implementation** for a design document generator.

## Components

### 1. Agent Definition (`.github/agents/my-agent.agent.md`)
- Defines the ProjectDesignDoc-Agent specification
- Describes the intended behavior and features
- Used by GitHub Copilot for understanding the agent's purpose

### 2. Implementation (`design_doc_generator.py`)
- Python script that implements the agent's functionality
- Can be run standalone or integrated into workflows
- Follows the structure outlined in the agent definition

## How They Work Together

The **agent definition** describes what the agent should do:
- Interactive intake questions
- Document structure
- Output format
- Use cases

The **implementation** provides the actual tool:
- Command-line interface
- Template generation
- File output
- Testing

## Usage Scenarios

### Scenario 1: Standalone Tool
```bash
python3 design_doc_generator.py
```
Use the script directly to generate design documents.

### Scenario 2: GitHub Copilot Integration
When using GitHub Copilot, the agent definition helps Copilot understand:
- How to structure design documents
- What questions to ask users
- What sections to include
- Best practices for technical documentation

### Scenario 3: CI/CD Integration
Integrate the script into your workflow:
```yaml
- name: Generate Design Doc
  run: python3 design_doc_generator.py < inputs.txt
```

## Extending the Implementation

To customize the generator for your organization:

1. **Add custom sections**: Edit `generate_document()` method
2. **Add more prompts**: Modify `gather_project_info()` method
3. **Change output format**: Update the markdown generation
4. **Add templates**: Create additional template files
5. **Integrate with tools**: Add export to Confluence, Notion, etc.

## Best Practices

1. **Run the generator early** - Create docs before coding
2. **Iterate on the output** - The generator creates a starting point
3. **Keep docs updated** - Use the revision history section
4. **Share with stakeholders** - Get feedback before implementation
5. **Use as a template** - Customize the output for your needs

## File Structure

```
desing_doc/
├── .github/
│   └── agents/
│       └── my-agent.agent.md       # Agent definition
├── design_doc_generator.py         # Main implementation
├── README.md                        # Full documentation
├── QUICKSTART.md                    # Quick reference
├── example_design_doc.md            # Sample output
├── test_generator.py                # Test suite
└── .gitignore                       # Git ignore rules
```

## Development

To contribute or modify:

1. Clone the repository
2. Make changes to `design_doc_generator.py`
3. Run tests: `python3 test_generator.py`
4. Update documentation if needed
5. Submit a pull request

## Support

For questions or issues:
- Check the README.md for usage instructions
- Review the example_design_doc.md for sample output
- Run the test suite to verify functionality
- Open an issue on GitHub

---

Built with ❤️ for better technical documentation
