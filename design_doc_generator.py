#!/usr/bin/env python3
"""
Design Document Generator
A tool to create comprehensive technical design documents through interactive prompts.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional


class DesignDocGenerator:
    """Interactive design document generator."""
    
    def __init__(self):
        self.project_data = {}
        
    def prompt(self, question: str, required: bool = True, default: str = "") -> str:
        """Prompt user for input with optional default value."""
        while True:
            if default:
                user_input = input(f"{question} [{default}]: ").strip()
                if not user_input:
                    user_input = default
            else:
                user_input = input(f"{question}: ").strip()
            
            if user_input or not required:
                return user_input
            
            if required:
                print("This field is required. Please provide a value.")
    
    def gather_project_info(self):
        """Collect project information through interactive prompts."""
        print("\n" + "="*70)
        print("Design Document Generator - Project Intake")
        print("="*70 + "\n")
        
        # Mandatory fields
        print("=== Mandatory Information ===\n")
        self.project_data['project_name'] = self.prompt("Project name")
        self.project_data['description'] = self.prompt("One-line description (what problem does it solve?)")
        self.project_data['audience'] = self.prompt("Primary audience (engineering/PMs/stakeholders/vendors)")
        
        # Optional but useful fields
        print("\n=== Optional Information (press Enter to skip) ===\n")
        self.project_data['goals'] = self.prompt("Goals & success metrics", required=False)
        self.project_data['stakeholders'] = self.prompt("Stakeholders & their roles", required=False)
        self.project_data['tech_stack'] = self.prompt("Preferred tech stack / infrastructure constraints", required=False)
        self.project_data['nfr'] = self.prompt("Non-functional requirements (scale, latency, SLA)", required=False)
        self.project_data['security'] = self.prompt("Data sensitivity / compliance concerns", required=False)
        self.project_data['timeline'] = self.prompt("Timeline / milestones & hard deadlines", required=False)
        self.project_data['constraints'] = self.prompt("Budget or other constraints", required=False)
        
        # Add metadata
        self.project_data['author'] = self.prompt("\nYour name (document author)", default="Anonymous")
        self.project_data['date'] = datetime.now().strftime("%Y-%m-%d")
        
    def generate_document(self) -> str:
        """Generate the complete design document."""
        doc = []
        
        # Title
        doc.append(f"# {self.project_data['project_name']}")
        doc.append(f"_{self.project_data['description']}_\n")
        
        # Metadata
        doc.append("---")
        doc.append(f"**Author:** {self.project_data['author']}")
        doc.append(f"**Date:** {self.project_data['date']}")
        doc.append(f"**Audience:** {self.project_data['audience']}")
        doc.append("---\n")
        
        # 1. Summary
        doc.append("## 1. Summary")
        doc.append(f"\n{self.project_data['description']}\n")
        if self.project_data.get('goals'):
            doc.append(f"**Goals:** {self.project_data['goals']}\n")
        doc.append("**Recommended Next Steps:** Review this document with stakeholders and approve the proposed design.\n")
        
        # 2. Overview
        doc.append("## 2. Overview")
        doc.append(f"\n**Purpose:** {self.project_data['description']}\n")
        doc.append("**Scope:** This document covers the technical design, architecture, implementation plan, and key decisions for the project.\n")
        if self.project_data.get('goals'):
            doc.append(f"**Goals:**\n- {self.project_data['goals']}\n")
        
        # 3. Key Definitions
        doc.append("## 3. Key Definitions")
        doc.append("\n*Add project-specific terminology and abbreviations here.*\n")
        
        # 4. Proposed Design
        doc.append("## 4. Proposed Design (High-Level)")
        doc.append("\n### User Flows")
        doc.append("*Describe the main user flows and interactions.*\n")
        doc.append("### Components and Responsibilities")
        doc.append("*List the major components and their responsibilities.*\n")
        doc.append("### Data Flows")
        doc.append("*Describe how data moves through the system.*\n")
        doc.append("```")
        doc.append("[Sequence diagram placeholder - add your diagram here]")
        doc.append("```\n")
        
        # 5. System Architecture
        doc.append("## 5. System Architecture")
        doc.append("\n### Logical Architecture")
        doc.append("```")
        doc.append("[Architecture diagram placeholder]")
        doc.append("```\n")
        doc.append("### Backend Services")
        if self.project_data.get('tech_stack'):
            doc.append(f"**Tech Stack:** {self.project_data['tech_stack']}\n")
        doc.append("*Describe backend services, APIs, and business logic components.*\n")
        doc.append("### Frontend Considerations")
        doc.append("*Describe user interface components and client-side logic.*\n")
        doc.append("### Third-Party Integrations")
        doc.append("*List external services and APIs to be integrated.*\n")
        
        # 6. Database Design
        doc.append("## 6. Database Design")
        doc.append("\n### Entity-Relationship Model")
        doc.append("```")
        doc.append("[ER diagram placeholder]")
        doc.append("```\n")
        doc.append("### Tables/Collections")
        doc.append("*Define database schema, tables, fields, types, and relationships.*\n")
        doc.append("### Indexes")
        doc.append("*List required indexes for performance.*\n")
        doc.append("### Data Retention")
        doc.append("*Define data retention and archival policies.*\n")
        
        # 7. API Contracts
        doc.append("## 7. API Contracts")
        doc.append("\n### Example Endpoints")
        doc.append("```")
        doc.append("GET /api/v1/resource")
        doc.append("POST /api/v1/resource")
        doc.append("PUT /api/v1/resource/{id}")
        doc.append("DELETE /api/v1/resource/{id}")
        doc.append("```\n")
        doc.append("### Request/Response Formats")
        doc.append("*Define API contract details, data models, and validation rules.*\n")
        doc.append("### Authentication Model")
        doc.append("*Describe authentication and authorization mechanisms.*\n")
        
        # 8. Failure Scenarios
        doc.append("## 8. Failure Scenarios & Mitigations")
        doc.append("\n### Failure Modes")
        doc.append("*Identify potential failure scenarios and their impact.*\n")
        doc.append("### Retry/Backoff Strategies")
        doc.append("*Define retry logic, exponential backoff, and circuit breaker patterns.*\n")
        doc.append("### Data Recovery")
        doc.append("*Describe backup and recovery procedures.*\n")
        
        # 9. Security & Privacy
        doc.append("## 9. Security & Privacy")
        if self.project_data.get('security'):
            doc.append(f"\n**Security Requirements:** {self.project_data['security']}\n")
        doc.append("### Threat Model")
        doc.append("*Identify security threats and mitigation strategies.*\n")
        doc.append("### Authentication/Authorization")
        doc.append("*Define access control mechanisms.*\n")
        doc.append("### Encryption")
        doc.append("*Specify encryption requirements for data at rest and in transit.*\n")
        doc.append("### Secrets Management")
        doc.append("*Describe how secrets and credentials are managed.*\n")
        
        # 10. Non-Functional Requirements
        doc.append("## 10. Non-Functional Requirements")
        if self.project_data.get('nfr'):
            doc.append(f"\n**Requirements:** {self.project_data['nfr']}\n")
        doc.append("### SLAs & Performance Targets")
        doc.append("*Define availability, latency, and throughput requirements.*\n")
        doc.append("### Monitoring & Alerting")
        doc.append("*Describe monitoring strategy and alert thresholds.*\n")
        doc.append("### Scale Plan")
        doc.append("*Define horizontal and vertical scaling strategies.*\n")
        
        # 11. Implementation Plan
        doc.append("## 11. Implementation Plan & Timeline")
        if self.project_data.get('timeline'):
            doc.append(f"\n**Timeline:** {self.project_data['timeline']}\n")
        if self.project_data.get('stakeholders'):
            doc.append(f"**Stakeholders:** {self.project_data['stakeholders']}\n")
        doc.append("### Milestones")
        doc.append("| Milestone | Owner | Deliverables | Target Date |")
        doc.append("|-----------|-------|--------------|-------------|")
        doc.append("| Phase 1   | TBD   | TBD          | TBD         |")
        doc.append("| Phase 2   | TBD   | TBD          | TBD         |")
        doc.append("| Phase 3   | TBD   | TBD          | TBD         |\n")
        doc.append("### Dependencies")
        doc.append("*List external dependencies and blockers.*\n")
        
        # 12. Testing & Validation
        doc.append("## 12. Testing & Validation")
        doc.append("\n### Testing Strategy")
        doc.append("- **Unit Tests:** Test individual components and functions")
        doc.append("- **Integration Tests:** Test component interactions")
        doc.append("- **End-to-End Tests:** Test complete user flows")
        doc.append("- **Performance Tests:** Validate performance requirements\n")
        doc.append("### Test Data")
        doc.append("*Define test data requirements and generation strategy.*\n")
        doc.append("### Load Testing Plan")
        doc.append("*Describe load testing approach and success criteria.*\n")
        
        # 13. Recommendations & Trade-offs
        doc.append("## 13. Recommendations & Trade-offs")
        doc.append("\n### Options Considered")
        doc.append("*List alternative approaches that were evaluated.*\n")
        doc.append("### Rationale")
        doc.append("*Explain the reasoning behind chosen approach.*\n")
        doc.append("### Trade-offs")
        doc.append("*Document known trade-offs and compromises.*\n")
        
        # 14. Open Questions
        doc.append("## 14. Open Questions & Decisions Needed")
        doc.append("\n- [ ] *List questions requiring stakeholder input*")
        doc.append("- [ ] *Add proposed default choices where applicable*\n")
        
        # 15. Revision History
        doc.append("## 15. Revision History")
        doc.append("\n| Version | Date | Author | Summary |")
        doc.append("|---------|------|--------|---------|")
        doc.append(f"| 1.0 | {self.project_data['date']} | {self.project_data['author']} | Initial draft |\n")
        
        return "\n".join(doc)
    
    def save_document(self, content: str, filename: Optional[str] = None):
        """Save the generated document to a file."""
        if filename is None:
            # Create filename from project name
            safe_name = self.project_data['project_name'].lower().replace(" ", "_")
            safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
            filename = f"{safe_name}_design_doc.md"
        
        with open(filename, 'w') as f:
            f.write(content)
        
        return filename
    
    def run(self):
        """Run the interactive design document generator."""
        try:
            # Gather information
            self.gather_project_info()
            
            # Generate document
            print("\n" + "="*70)
            print("Generating design document...")
            print("="*70 + "\n")
            
            doc_content = self.generate_document()
            
            # Save document
            filename = self.save_document(doc_content)
            
            print(f"✓ Design document generated successfully!")
            print(f"✓ Saved to: {filename}\n")
            print("You can now:")
            print("  - Review and edit the document")
            print("  - Add diagrams and detailed specifications")
            print("  - Share with stakeholders for feedback")
            print("  - Use it as a template for implementation planning\n")
            
            return filename
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    generator = DesignDocGenerator()
    generator.run()


if __name__ == "__main__":
    main()
