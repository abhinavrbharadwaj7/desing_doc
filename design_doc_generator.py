#!/usr/bin/env python3
"""
Design Document Generator
A tool to create comprehensive technical design documents through interactive prompts.
Supports file inputs and multiline text for artifact ingestion.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional, List


class DesignDocGenerator:
    """Interactive design document generator with artifact ingestion support."""
    
    def __init__(self):
        self.project_data = {}
        self.artifacts = []  # Store ingested artifacts
        
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
    
    def prompt_multiline(self, question: str) -> str:
        """Prompt for multiline input. User enters 'END' on a new line to finish."""
        print(f"{question}")
        print("(Enter your text below. Type 'END' on a new line when finished)")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)
    
    def ingest_file(self, filepath: str) -> Dict[str, str]:
        """Read and ingest a file as an artifact."""
        try:
            if not os.path.exists(filepath):
                print(f"  ✗ File not found: {filepath}")
                return None
            
            # Get file extension
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            
            # Read text-based files
            if ext in ['.txt', '.md', '.markdown', '.rst', '.text', '.json', '.yaml', '.yml', '.csv', '']:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                artifact = {
                    'type': 'file',
                    'name': os.path.basename(filepath),
                    'path': filepath,
                    'extension': ext,
                    'content': content,
                    'summary': self._summarize_content(content, os.path.basename(filepath))
                }
                print(f"  ✓ Ingested: {os.path.basename(filepath)} ({len(content)} chars)")
                return artifact
            else:
                print(f"  ⚠ Unsupported file type: {ext}")
                print(f"    Supported: .txt, .md, .json, .yaml, .csv, and text files")
                return None
                
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            return None
    
    def ingest_text(self, text: str, name: str = "Pasted Text") -> Dict[str, str]:
        """Ingest pasted text as an artifact."""
        if not text.strip():
            return None
        
        artifact = {
            'type': 'text',
            'name': name,
            'content': text,
            'summary': self._summarize_content(text, name)
        }
        print(f"  ✓ Ingested: {name} ({len(text)} chars)")
        return artifact
    
    def _summarize_content(self, content: str, name: str) -> str:
        """Create a brief summary of the content."""
        lines = content.strip().split('\n')
        line_count = len(lines)
        word_count = len(content.split())
        
        # Extract first few meaningful lines
        preview_lines = []
        for line in lines[:5]:
            line = line.strip()
            if line:
                preview_lines.append(line)
                if len(preview_lines) >= 3:
                    break
        
        preview = " | ".join(preview_lines[:3])
        if len(preview) > 100:
            preview = preview[:97] + "..."
        
        return f"{name}: {line_count} lines, {word_count} words. Preview: {preview}"
    
    def gather_artifacts(self):
        """Collect artifacts (files or text) from the user."""
        print("\n=== Artifact Ingestion (Optional) ===")
        print("You can provide existing materials to enhance the design document.")
        print()
        
        while True:
            choice = input("Add artifact? (f)ile, (t)ext, or (s)kip: ").strip().lower()
            
            if choice == 's' or choice == 'skip' or not choice:
                break
            elif choice == 'f' or choice == 'file':
                filepath = input("  Enter file path: ").strip()
                if filepath:
                    # Remove quotes if user wrapped path in quotes
                    filepath = filepath.strip('"').strip("'")
                    artifact = self.ingest_file(filepath)
                    if artifact:
                        self.artifacts.append(artifact)
            elif choice == 't' or choice == 'text':
                print("  Paste or type your text below (type 'END' on a new line when done):")
                text = self.prompt_multiline("")
                if text:
                    name = input("  Give this artifact a name (optional): ").strip() or "Pasted Text"
                    artifact = self.ingest_text(text, name)
                    if artifact:
                        self.artifacts.append(artifact)
            else:
                print("  Invalid choice. Use 'f' for file, 't' for text, or 's' to skip.")
        
        if self.artifacts:
            print(f"\n✓ Total artifacts ingested: {len(self.artifacts)}")
        else:
            print("\nNo artifacts provided. Proceeding with manual input only.")

    
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
        
        # Artifact ingestion
        self.gather_artifacts()
        
        # Add metadata
        self.project_data['author'] = self.prompt("\nYour name (document author)", default="Anonymous")
        self.project_data['date'] = datetime.now().strftime("%Y-%m-%d")
        
    def generate_document(self) -> str:
        """Generate the complete design document using the new template structure."""
        doc = []
        
        # Title
        doc.append(f"# {self.project_data['project_name']}")
        doc.append(f"_{self.project_data['description']}_\n")
        
        # Revision History
        doc.append("## Revision History")
        doc.append("---")
        doc.append("| **Revision** | **Date** | **Created By** | **Changes** |")
        doc.append("| --- | --- | --- | --- |")
        doc.append(f"| R0 | {self.project_data['date']} | {self.project_data['author']} | Initial draft |\n")
        
        # Overview
        doc.append("# Overview")
        doc.append("---")
        doc.append("## Purpose")
        doc.append(f"{self.project_data['description']}\n")
        doc.append("Provide a clear understanding of the design decisions, architecture, and implementation strategy for the project/module.\n")
        
        doc.append("## Scope")
        doc.append("This document covers the technical design, architecture, implementation plan, and key decisions for the project.\n")
        if self.project_data.get('audience'):
            doc.append(f"**Target Audience:** {self.project_data['audience']}\n")
        
        doc.append("## Feature Description")
        if self.project_data.get('goals'):
            doc.append(f"**Goals:** {self.project_data['goals']}\n")
        doc.append("*Describe the main functionality of the feature/system being designed.*\n")
        
        # Add ingested artifacts summary if any
        if self.artifacts:
            doc.append("## Source Materials")
            for i, artifact in enumerate(self.artifacts, 1):
                doc.append(f"{i}. {artifact['summary']}")
            doc.append("")
        
        # Key Definitions
        doc.append("# Key Definitions")
        doc.append("---")
        doc.append("## Key Terms")
        doc.append("*Define important terms and concepts used throughout this document.*\n")
        
        doc.append("## Assumptions")
        doc.append("*List assumptions that guide the design process.*\n")
        
        # Proposed UI
        doc.append("# Proposed UI")
        doc.append("---")
        doc.append("*Screenshot of the proposed UI for the feature, along with figma link for further details.*\n")
        doc.append("*[Insert UI mockups or wireframes here]*\n")
        
        # More Feature Details
        doc.append("# More Feature Details")
        doc.append("---")
        doc.append("*Link to Azure wiki made by Product Managers or other feature documentation.*\n")
        
        # Revision Details Separator
        doc.append("## Revision Details")
        doc.append("---")
        doc.append("| **Revision** | **Date** | **Created By** | **Changes** |")
        doc.append("| --- | --- | --- | --- |")
        doc.append(f"| R0 | {self.project_data['date']} | {self.project_data['author']} | Initial draft |\n")
        
        # Proposed Design
        doc.append("# Proposed Design")
        doc.append("---")
        doc.append("## High-Level Approach")
        doc.append("Explain the high-level approach, breaking it into phases if necessary.\n")
        
        doc.append("### Phase 1: [Name]")
        doc.append("* **Objective:** *Define the objective for this phase*")
        doc.append("* **Tasks:**")
        doc.append("  * Task 1")
        doc.append("  * Task 2\n")
        
        doc.append("### Phase 2: [Name]")
        doc.append("* **Objective:** *Define the objective for this phase*")
        doc.append("* **Tasks:**")
        doc.append("  * Task 1")
        doc.append("  * Task 2\n")
        
        doc.append("## Technical Choices")
        if self.project_data.get('tech_stack'):
            doc.append(f"**Selected Technologies:** {self.project_data['tech_stack']}\n")
        doc.append("*Explain the frameworks, tools, and services being used, along with reasons for selection.*\n")
        
        # System Architecture
        doc.append("# System Architecture")
        doc.append("---")
        doc.append("## Component Overview")
        doc.append("Provide an overview of the system's key components and their roles.\n")
        
        doc.append("## Flow Diagram")
        doc.append("*Insert a high-level flow diagram illustrating the data/process flow.*")
        doc.append("```")
        doc.append("[Flow Diagram Placeholder]")
        doc.append("```\n")
        
        # Database Design
        doc.append("# Database Design")
        doc.append("---")
        doc.append("## Schema Definition")
        doc.append("```json")
        doc.append("{")
        doc.append('  "key": "value",')
        doc.append('  "example_field": "example_value"')
        doc.append("}")
        doc.append("```\n")
        doc.append("* **Indexes:**")
        doc.append("  * Explain the indexes used and why.\n")
        
        # Server Load and Cost Considerations
        doc.append("# Server Load and Cost Considerations")
        doc.append("---")
        doc.append("| **Factor** | **Method 1** | **Method 2** |")
        doc.append("| --- | --- | --- |")
        doc.append("| **Connection Load** | Description | Description |")
        doc.append("| **Data Load** | Description | Description |")
        doc.append("| **Cost Efficiency** | Description | Description |\n")
        
        # Development Effort
        doc.append("# Development Effort")
        doc.append("---")
        doc.append("## Phase 1")
        doc.append("* Estimated Effort: [Value]\n")
        doc.append("## Phase 2")
        doc.append("* Estimated Effort: [Value]\n")
        
        # Recommendation
        doc.append("# Recommendation")
        doc.append("---")
        doc.append("Provide recommendations based on analysis, including a preferred approach and justifications.\n")
        
        # Next Steps
        doc.append("# Next Steps")
        doc.append("---")
        if self.project_data.get('timeline'):
            doc.append(f"**Timeline:** {self.project_data['timeline']}\n")
        doc.append("1. **Task 1:** Description.")
        doc.append("2. **Task 2:** Description.\n")
        
        # Appendices
        doc.append("# Appendices")
        doc.append("---")
        doc.append("* Reference documents.")
        doc.append("* Links to relevant documentation.\n")
        
        # Second Revision Details (for implementation phase)
        doc.append("## Revision Details")
        doc.append("---")
        doc.append("| **Revision** | **Date** | **Created By** | **Changes** |")
        doc.append("| --- | --- | --- | --- |")
        doc.append(f"| R1 | {self.project_data['date']} | {self.project_data['author']} | - Added implementation sections |\n")
        
        # Failure Scenarios and Security section
        doc.append("# Failure Scenarios and Mitigations")
        doc.append("---")
        doc.append("## Failure Scenarios\n")
        doc.append("1. **Scenario 1:**")
        doc.append("   * Description.")
        doc.append("   * **Mitigation:** *Describe mitigation strategy*\n")
        doc.append("2. **Scenario 2:**")
        doc.append("   * Description.")
        doc.append("   * **Mitigation:** *Describe mitigation strategy*\n")
        
        doc.append("## Security Implications")
        if self.project_data.get('security'):
            doc.append(f"**Security Requirements:** {self.project_data['security']}\n")
        doc.append("1. **Issue 1:**")
        doc.append("   * Description.")
        doc.append("   * **Mitigation:** *Describe mitigation strategy*\n")
        doc.append("2. **Issue 2:**")
        doc.append("   * Description.")
        doc.append("   * **Mitigation:** *Describe mitigation strategy*\n")
        
        # Implementation Details Section
        doc.append("---\n")
        doc.append("# **Overview**")
        doc.append("---")
        doc.append("This document provides a structured approach for documenting the finalized implementation of a feature. It includes the following sections:")
        doc.append("* Architecture and Design Decisions")
        doc.append("* Database Schema & Storage Design")
        doc.append("* Frontend & Backend Implementation")
        doc.append("* Required dependencies (existing & new)")
        doc.append("* Business Logic & Functional Details")
        doc.append("* Security measures and failure handling\n")
        
        # Sequence Diagram
        doc.append("# **Sequence Diagram**")
        doc.append("---")
        doc.append("*Insert a sequence diagram illustrating the process flow relevant to this feature.*")
        doc.append("```")
        doc.append("[Sequence Diagram Placeholder]")
        doc.append("```\n")
        
        # Implementation Details
        doc.append("# **Implementation Details**")
        doc.append("---")
        doc.append("## **Technologies & Dependencies Required**\n")
        doc.append("### **Backend:**")
        if self.project_data.get('tech_stack'):
            doc.append(f"* {self.project_data['tech_stack']}")
        doc.append("* List the backend technologies, frameworks, or libraries used and their purpose.\n")
        doc.append("### **Frontend:**")
        doc.append("* List the frontend technologies, frameworks, or libraries used and their purpose.\n")
        
        # Backend Implementation
        doc.append("# **Backend Implementation**")
        doc.append("---")
        doc.append("## **Core Functionalities**")
        doc.append("* Describe the key backend functionalities implemented for this feature.")
        doc.append("* Outline any reusable components or services created.\n")
        
        doc.append("## **Endpoints & API Design**")
        doc.append("| Endpoint | Method | Description |")
        doc.append("| --- | --- | --- |")
        doc.append("| `/feature-endpoint` | GET | Fetches data related to this feature |")
        doc.append("| `/feature-endpoint/create` | POST | Creates a new record related to this feature |")
        doc.append("| `/feature-endpoint/update` | PUT | Updates an existing record |")
        doc.append("| `/feature-endpoint/delete` | DELETE | Deletes an existing record |\n")
        
        # Frontend Implementation
        doc.append("# **Frontend Implementation**")
        doc.append("---")
        doc.append("## **State Management & UI Components**")
        doc.append("* Describe how state is managed (Redux, Context API, etc.)")
        doc.append("* List and describe key UI components used or created for this feature.\n")
        doc.append("## **Helper Functions & Utilities**")
        doc.append("* Mention any utility/helper functions developed to support the feature.\n")
        
        # Business Logic
        doc.append("# **Business Logic & Functional Details**")
        doc.append("---")
        doc.append("## **Processing Logic**")
        doc.append("* Explain how the core logic of this feature is structured and executed.")
        doc.append("* Describe key operations, workflows, or automations involved.\n")
        
        # Security Considerations
        doc.append("# **Security Considerations**")
        doc.append("---")
        doc.append("* **Authentication & Authorization:** Describe how security measures are enforced.")
        doc.append("* **Data Validation & Sanitization:** Explain how input data is validated and sanitized.")
        doc.append("* **Rate Limiting & API Protection:** Mention any mechanisms to prevent abuse.")
        doc.append("* **Error Handling & Logging:** Describe the error handling approach used.\n")
        
        # Failure Scenarios & Mitigation
        doc.append("# **Failure Scenarios & Mitigation**")
        doc.append("---")
        doc.append("| Failure Scenario | Issue | Mitigation |")
        doc.append("| --- | --- | --- |")
        doc.append("| Scenario 1 | Describe issue | Describe mitigation strategy |")
        doc.append("| Scenario 2 | Describe issue | Describe mitigation strategy |\n")
        
        # Next Steps
        doc.append("# **Next Steps**")
        doc.append("---")
        doc.append("## **Pending Implementations**")
        doc.append("* List any pending or future enhancements required for this feature.\n")
        doc.append("## **Approval Required For:**")
        doc.append("* List any outstanding approvals or reviews required before full deployment.\n")
        
        # Summary
        doc.append("# **Summary**")
        doc.append("---")
        doc.append("✅ Feature successfully implemented following the structured design principles.")
        doc.append("✅ Key functionalities, security considerations, and failure handling documented.")
        doc.append("✅ Pending refinements: List next improvement areas.\n")
        
        # Appendix: Source Artifacts (if any)
        if self.artifacts:
            doc.append("---\n")
            doc.append("# Appendix: Source Artifacts")
            doc.append("---")
            doc.append("This section contains the full content of ingested artifacts for reference.\n")
            
            for i, artifact in enumerate(self.artifacts, 1):
                doc.append(f"## Artifact {i}: {artifact['name']}")
                doc.append("")
                if artifact['type'] == 'file':
                    doc.append(f"**Source:** `{artifact['path']}`")
                doc.append("")
                doc.append("```")
                # Limit very large content
                content = artifact['content']
                if len(content) > 10000:
                    doc.append(content[:10000])
                    doc.append(f"\n... (truncated, showing first 10,000 of {len(content)} characters)")
                else:
                    doc.append(content)
                doc.append("```")
                doc.append("")
        
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
            
            # Ask if user wants to see output for copy-paste
            show_output = input("Display output for copy-paste to wiki? (y/N): ").strip().lower()
            if show_output in ['y', 'yes']:
                print("\n" + "="*70)
                print("DESIGN DOCUMENT OUTPUT (Copy everything below)")
                print("="*70 + "\n")
                print(doc_content)
                print("\n" + "="*70)
                print("END OF DOCUMENT")
                print("="*70 + "\n")
            
            print("You can now:")
            print(f"  - Copy content from the file: {filename}")
            print("  - Review and edit the document")
            print("  - Add diagrams and detailed specifications")
            print("  - Share with stakeholders for feedback")
            print("  - Paste directly into your wiki\n")
            
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
