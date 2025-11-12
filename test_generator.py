#!/usr/bin/env python3
"""
Test script for the Design Document Generator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from design_doc_generator import DesignDocGenerator


def test_basic_generation():
    """Test basic document generation with minimal data."""
    print("Test 1: Basic document generation...")
    gen = DesignDocGenerator()
    gen.project_data = {
        'project_name': 'Test API',
        'description': 'REST API for testing',
        'audience': 'engineering',
        'author': 'Test User',
        'date': '2025-11-12'
    }
    
    doc = gen.generate_document()
    assert len(doc) > 1000, "Document should have substantial content"
    assert "Test API" in doc
    assert "REST API for testing" in doc
    assert "## Revision History" in doc
    assert "# Overview" in doc
    print("✓ Basic generation works")


def test_full_generation():
    """Test document generation with all fields."""
    print("Test 2: Full document generation...")
    gen = DesignDocGenerator()
    gen.project_data = {
        'project_name': 'Full Feature App',
        'description': 'Complete application with all features',
        'audience': 'engineering/PMs',
        'goals': 'Achieve 99.9% uptime',
        'stakeholders': 'Engineering team, Product team',
        'tech_stack': 'Python, Django, PostgreSQL',
        'nfr': 'Handle 1M users',
        'security': 'GDPR compliant',
        'timeline': 'Q1 2025',
        'constraints': 'Budget: $100k',
        'author': 'Full Test User',
        'date': '2025-11-12'
    }
    
    doc = gen.generate_document()
    assert "Full Feature App" in doc
    assert "99.9% uptime" in doc
    assert "Python, Django, PostgreSQL" in doc
    assert "GDPR compliant" in doc
    print("✓ Full generation works")


def test_filename_generation():
    """Test that safe filenames are generated."""
    print("Test 3: Filename generation...")
    gen = DesignDocGenerator()
    
    # Test with spaces
    gen.project_data = {'project_name': 'My Test Project'}
    filename = gen.save_document("test content", None)
    assert filename == "my_test_project_design_doc.md"
    os.remove(filename)
    
    # Test with special characters
    gen.project_data = {'project_name': 'Test@Project#123!'}
    filename = gen.save_document("test content", None)
    assert filename == "testproject123_design_doc.md"
    os.remove(filename)
    
    print("✓ Filename generation works")


def test_document_structure():
    """Test that all required sections are present."""
    print("Test 4: Document structure...")
    gen = DesignDocGenerator()
    gen.project_data = {
        'project_name': 'Structure Test',
        'description': 'Test structure',
        'audience': 'engineering',
        'author': 'Test',
        'date': '2025-11-12'
    }
    
    doc = gen.generate_document()
    
    required_sections = [
        "## Revision History",
        "# Overview",
        "# Key Definitions",
        "# Proposed UI",
        "# More Feature Details",
        "# Proposed Design",
        "# System Architecture",
        "# Database Design",
        "# Server Load and Cost Considerations",
        "# Development Effort",
        "# Recommendation",
        "# Next Steps",
        "# Appendices",
        "# Failure Scenarios and Mitigations",
        "# **Implementation Details**",
        "# **Backend Implementation**",
        "# **Frontend Implementation**",
        "# **Security Considerations**",
        "# **Summary**"
    ]
    
    for section in required_sections:
        assert section in doc, f"Missing section: {section}"
    
    print("✓ Document structure is complete")


def test_prompt_function():
    """Test the prompt function with defaults."""
    print("Test 5: Prompt function...")
    gen = DesignDocGenerator()
    
    # This is a unit test - we can't test interactive input easily
    # but we can verify the function exists and has correct signature
    assert hasattr(gen, 'prompt')
    assert callable(gen.prompt)
    print("✓ Prompt function exists")


def test_artifact_ingestion():
    """Test artifact ingestion functionality."""
    print("Test 6: Artifact ingestion...")
    gen = DesignDocGenerator()
    
    # Test text ingestion
    text = "Sample text for testing"
    artifact = gen.ingest_text(text, "Test Artifact")
    assert artifact is not None
    assert artifact['type'] == 'text'
    assert artifact['name'] == 'Test Artifact'
    assert artifact['content'] == text
    
    # Test that artifacts list is maintained
    gen.artifacts.append(artifact)
    assert len(gen.artifacts) == 1
    
    print("✓ Artifact ingestion works")


def test_document_with_artifacts():
    """Test document generation includes artifacts."""
    print("Test 7: Document with artifacts...")
    gen = DesignDocGenerator()
    gen.project_data = {
        'project_name': 'Artifact Test',
        'description': 'Test with artifacts',
        'audience': 'engineering',
        'author': 'Test',
        'date': '2025-11-12'
    }
    
    # Add an artifact
    gen.artifacts.append({
        'type': 'text',
        'name': 'Test Doc',
        'content': 'Test content',
        'summary': 'Test Doc: summary here'
    })
    
    doc = gen.generate_document()
    
    # Check that artifacts are included
    assert 'Source Materials' in doc
    assert 'Test Doc' in doc
    assert 'Appendix: Source Artifacts' in doc
    
    print("✓ Document with artifacts works")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("Running Design Document Generator Tests")
    print("="*70 + "\n")
    
    tests = [
        test_basic_generation,
        test_full_generation,
        test_filename_generation,
        test_document_structure,
        test_prompt_function,
        test_artifact_ingestion,
        test_document_with_artifacts
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
