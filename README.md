# Design Document Generator

An interactive tool that generates comprehensive technical design documents through guided prompts. This agent helps you create professional design documentation following industry best practices.

## Features

- **Interactive intake form** - Guided prompts for project information
- **Comprehensive structure** - 15 essential sections covering all aspects of technical design
- **Ready-to-use templates** - Professional markdown format with placeholders
- **Quick generation** - Create complete design docs in minutes
- **Customizable** - Easy to extend and modify for specific needs

## What is a Design Document?

A design document is a comprehensive specification that outlines the technical approach, architecture, and implementation plan for a software project. It serves as:

- A blueprint for implementation
- A communication tool for stakeholders
- A decision log for trade-offs and choices
- A reference for future maintenance and evolution

## Installation

No installation required! Just Python 3.6+.

```bash
# Clone the repository
git clone https://github.com/abhinavrbharadwaj7/desing_doc.git
cd desing_doc

# Make the script executable (optional)
chmod +x design_doc_generator.py
```

## Usage

### Interactive Mode (Recommended)

Run the generator and answer the prompts:

```bash
python3 design_doc_generator.py
```

The tool will ask you for:

**Mandatory Information:**
- Project name
- One-line description
- Primary audience

**Optional Information:**
- Goals & success metrics
- Stakeholders & roles
- Tech stack preferences
- Non-functional requirements
- Security concerns
- Timeline & milestones
- Budget constraints

### Example Session

```
$ python3 design_doc_generator.py

======================================================================
Design Document Generator - Project Intake
======================================================================

=== Mandatory Information ===

Project name: User Authentication Service
One-line description: A secure OAuth2-based authentication service for microservices
Primary audience: engineering/PMs

=== Optional Information (press Enter to skip) ===

Goals & success metrics: 99.9% uptime, <100ms latency
Stakeholders & their roles: 
Preferred tech stack: Python, FastAPI, PostgreSQL, Redis
Non-functional requirements: Handle 10k req/sec
Data sensitivity / compliance concerns: GDPR, SOC2
Timeline / milestones: Q1 2024 launch
Budget or other constraints: 

Your name (document author) [Anonymous]: John Doe

======================================================================
Generating design document...
======================================================================

✓ Design document generated successfully!
✓ Saved to: user_authentication_service_design_doc.md
```

## Document Structure

The generated document includes these sections:

1. **Summary** - Quick overview for stakeholders
2. **Overview** - Purpose, scope, and goals
3. **Key Definitions** - Terminology and abbreviations
4. **Proposed Design** - High-level design and flows
5. **System Architecture** - Components and infrastructure
6. **Database Design** - Schema and data model
7. **API Contracts** - Endpoints and interfaces
8. **Failure Scenarios** - Error handling and recovery
9. **Security & Privacy** - Threat model and mitigations
10. **Non-Functional Requirements** - SLAs and performance
11. **Implementation Plan** - Timeline and milestones
12. **Testing & Validation** - Test strategy
13. **Recommendations** - Trade-offs and decisions
14. **Open Questions** - Items needing input
15. **Revision History** - Change log

## Output Format

The tool generates a markdown file with:
- Professional formatting
- Placeholder sections for diagrams
- Tables for structured data
- Checklists for open questions
- Metadata header with author and date

## Customization

You can modify the template by editing the `generate_document()` method in `design_doc_generator.py`. Common customizations:

- Add/remove sections
- Change section order
- Add company-specific templates
- Include additional prompts
- Integrate with external tools

## Use Cases

Perfect for:
- New project proposals
- Architecture decision records
- System design documentation
- Technical RFCs
- Project planning and estimation
- Stakeholder communication
- Team alignment and knowledge sharing

## Tips for Best Results

1. **Be specific** - Provide detailed answers for better outputs
2. **Include artifacts** - Reference existing docs and diagrams
3. **Iterate** - Generate, review, and refine
4. **Collaborate** - Share early drafts with team members
5. **Keep it updated** - Use revision history to track changes

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is open source and available for use and modification.

## Support

For issues or questions:
- Open an issue on GitHub
- Contact the maintainers

---

**Happy documenting!** 🚀
