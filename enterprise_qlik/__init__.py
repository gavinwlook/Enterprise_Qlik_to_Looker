"""
Enterprise Qlik-to-Looker Migration Engine
===========================================
A modular, decoupled enterprise migration framework:
- Stage 1: QIX Engine Extraction, PII Sanitization, 3-Tier Compatibility Auditing, and Canonical IR Compilation.
- Stage 2: Target Code Generation (LookML Explores, Views, Dashboards, and dbt blueprints) consuming only the Canonical IR.
- Storage: Dual SQLite (WAL) / PostgreSQL persistence layer for fleet-scale migrations.
- Web UI: Decoupled migration management studio with handoff export.
"""

__version__ = "2.0.0"
__author__ = "Gavin Look"
