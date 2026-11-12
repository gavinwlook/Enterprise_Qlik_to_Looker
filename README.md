# Enterprise Qlik-to-Looker Migration Engine

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-Decoupled_Stages-emerald.svg)]()
[![Looker](https://img.shields.io/badge/LookML-Explore--Centric-purple.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero_External_pip-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-54_Passed-brightgreen.svg)]()

An enterprise-grade, decoupled migration suite designed for Heads of Business Intelligence, Lead Data Architects, and Cloud Engineering teams in highly regulated industries (banking, insurance, healthcare, retail, and telecommunications).

It transitions sprawling legacy **Qlik Sense Enterprise (On-Premises Windows & Qlik Cloud SaaS)** business intelligence portfolios into modern **Google Cloud Looker** semantic models, **LookML Explores**, and **Cloud Data Warehouse (BigQuery / Snowflake)** architectures with zero row-data egress and zero external runtime dependencies.

---

## 🏛️ Key Architectural Principles

```
                                  STAGE 1: SOURCE TO CONTRACT                                   STAGE 2: TARGET SYNTHESIS
┌─────────────────────────┐         ┌───────────────────────────┐        ┌───────────────────┐        ┌─────────────────────────┐
│       Qlik Source       │ ──────> │  PII / Secrets Sanitizer  │ ─────> │   Open Canonical  │ ─────> │   LookML & dbt Studio   │
│  (Cloud SaaS / QSEoW)   │         │  & 3-Tier Gap Engine      │        │      IR (v2.0)    │        │  (Explores, Views, Dash)│
└─────────────────────────┘         └───────────────────────────┘        └───────────────────┘        └─────────────────────────┘
                                                                                   │
                                                                                   ▼
                                                                     [Autonomous Handoff Contract]
                                                                     • No Qlik or vendor lock-in
                                                                     • Ingestible by AI coding agents
                                                                     • CI/CD & dbt pipeline ready
```

1. **Decoupled Stage Architecture (Clean Handoff Contract):**
   - **Stage 1 (Source Extraction & Canonical IR Compiler):** Connects to Qlik instances via QIX WebSocket / REST, sanitizes PII and tokens, audits 3-tier compatibility gaps, and compiles a formal 2-tier **Canonical Intermediate Representation (IR)** (`canonical_ir.json` and `feature_gaps.json`) validated against JSON Schema Draft 2020-12.
   - **Stage 2 (Target Code Generation):** Decoupled compiler reading **only** `canonical_ir.json` with zero imports from Stage 1 or Qlik. Customers can take their Canonical IR to any pipeline, dbt repository, or custom AI coding agent without vendor lock-in.
2. **Explore-Centric LookML Modeling:**
   - In Looker, dashboards bind strictly to **Explores**, not raw database views.
   - Stage 2 compiles **Multi-View Star/Snowflake Explores** (root fact views joined to dimension views with `relationship: many_to_one`) and **Single-View Explores** (for flat denormalized tables).
   - Dashboard elements reference fully qualified fields (`${explore_name.field_name}`) and specify both `model:` and `explore:` explicitly.
3. **Zero Row-Data Egress & Air-Gapped Security:**
   - The engine inspects *metadata, load scripts, AST expressions, and sheet layouts only*. It never reads raw database table data.
   - Automated regular-expression scrubbers redact PANs, IBANs, SSNs, bearer tokens, passwords, and emails before saving to disk or database.
4. **Zero External Runtime Dependencies:**
   - Written 100% in the **Python 3.10+ Standard Library** (`http.server`, `urllib`, `sqlite3`, `json`, `ssl`, `dataclasses`).
   - Runs out-of-the-box on developer laptops, cloud development environments, hardened bastion hosts, or air-gapped VMs without requiring `pip install`.

---

## 🧭 The Head of Business Intelligence Journey (Web Studio)

The Migration Web Studio provides a 6-stage operational workspace tailored for BI leadership and migration teams:

```
  ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  │ 🏢 1. Instances │ ───> │  📊 2. Executive │ ───> │  🌊 3. Migration │
  │   & Connections │      │  Command Center  │      │   Wave Planner   │
  └─────────────────┘      └──────────────────┘      └──────────────────┘
                                                              │
  ┌─────────────────┐      ┌──────────────────┐               ▼
  │  🚀 6. Stage 2  │ <─── │   🔬 5. Stage 1  │ <─── ┌──────────────────┐
  │  LookML Studio  │      │    App Studio    │      │  📂 4. Fleet &   │
  └─────────────────┘      └──────────────────┘      │     Catalog      │
                                                     └──────────────────┘
```

### 1. 🏢 Multi-Environment Management (`#tab-instances`)
- Manage concurrent connections across **Qlik Cloud SaaS** (tenant URL, Bearer API keys, Web Integration IDs) and **Qlik Sense Enterprise on Windows (QSEoW)** (cluster host, mTLS client certificates on port 4242/4747).
- Real-time connection latency probes, JWT token claim verification, and active instance switching.

### 2. 📊 Executive Command Center (`#tab-executive`)
- **Portfolio Health & Velocity:** Total applications discovered, Canonical IR readiness velocity, active migration waves, and projected transition timelines.
- **Space Governance & Risk:** Breakdown across *Managed Spaces* (governed production), *Shared Spaces* (co-development), and *Personal Spaces* (developer sandbox).
- **Semantic Model Deduplication Engine:** Automatically identifies redundant Qlik data models across different apps and groups them into unified Looker Explores, projecting up to 60% savings in data warehouse modeling and maintenance overhead.

### 3. 🌊 Migration Wave Planner (`#tab-waves`)
- Interactive 5-column Kanban board:
  - `📋 Backlog / Unassigned`
  - `⚡ Wave 1: Quick Wins (Clean Mappings)`
  - `🏛️ Wave 2: Governed Enterprise Core`
  - `🔬 Wave 3: Complex Multi-Fact Models`
  - `📦 Decommissioned & Retired`
- **Migration Wave Policy Builder & Simulation Wizard:** Configurable rule engine (`simulate_policies`, `apply_policies`) to dry-run and auto-assign applications to migration waves and lead engineers based on space type, sheet/widget complexity, and Category 2/3 gap findings.
- **Migration Leads Roster:** Database-backed team management system assigning technical leads (e.g. Principal Architect, Analytics Engineer, LookML Specialist) to specific migration waves with visual avatar badges.
- **Portfolio CSV & JSON Export:** One-click enterprise portfolio exports with comprehensive metadata (governance space, complexity metrics, assigned leads, wave allocations, and extraction status).

### 4. 📂 Fleet Hierarchy & Catalog (`#tab-catalog`)
- **Autonomous Live Fleet Discovery:** Server startup background daemon and self-healing browser discovery immediately pull live spaces and applications from Qlik Cloud (`/api/v1/spaces` and `/api/v1/items?resourceType=app`) and on-premise QRS endpoints without requiring terminal commands.
- **Container Tree Explorer:** Visualizes the true organizational hierarchy:
  - *Qlik Cloud SaaS:* `Tenant -> Spaces (Managed, Shared, Personal) -> Applications`
  - *QSEoW On-Premises:* `Cluster -> Streams (Published) / Work Area (Sandbox) -> Applications`
- **Catalog Table & Batch Operations Bar:** Multi-select apps for batch Canonical IR extraction, batch wave assignment, or batch decommissioning.
- **+ Register Qlik App Modal:** Instantly register any Qlik app by Name, ID, or pasting its Qlik Cloud browser URL with immediate Canonical IR extraction.
- **🔄 Refresh Fleet:** Instant on-demand catalog synchronization directly from the UI header.

### 5. 🔬 Stage 1: App Inspection Studio (`#tab-canvas`)
- Unified deep-dive inspection workspace eliminating redundant setup steps:
  - **Top App Strip:** Application name, GUID, space type, IR compile status, and `🔄 Re-Extract App` action.
  - **Multi-Source Sheet Discovery & Private ("My own") Unpacking:** Overcomes QIX `SheetList` space-filter truncation by combining `Doc.GetAllInfos` graph inventory, `Doc.GetObjects`, and deep property tree unpacking (`Doc.GetObject` -> `GetLayout` -> `GetFullPropertyTree`) to extract both **🌐 Public** approved base sheets and **👤 My own** unpublished/personal sheets with chart geometry, hypercubes, dimensions, measures, and filterpane list objects.
  - **Left Navigation Sidebar:** Instant access to Shared Architecture (`🗄️ Shared Data Model ERD`, `🔍 Compatibility Audit`) and Dashboards & Sheets categorized into Public and My own groups with instant search and Category 1/2/3 breakdown pills.
  - **Responsive Canvas Grid:** Visualizes sheets on a Looker 12-column responsive grid layout with visual tile types, dimensions, measures, and target Explore bindings.
  - **Autonomous Milestone Footer:** Download the complete `canonical_ir.json` and `feature_gaps.json` package or proceed to Stage 2.

### 6. 🚀 Stage 2: Explore-First LookML Studio (`#tab-lookml`)
- Automated synthesis of LookML models, Explores, view files, dashboard definitions, and upstream dbt transformations directly from the Canonical IR contract.
- Pure decoupled consumption: reads exclusively from `canonical_ir.json` with zero imports or dependencies on Qlik.

---

## 🔍 3-Tier Migration Gap Taxonomy

Every Qlik visual expression, script statement, and data model construct is audited against the 3-Tier Taxonomy:

| Tier | Classification | Detected Qlik Constructs | Automated Looker / dbt Remediation Plan |
| :--- | :--- | :--- | :--- |
| **Category 1** | **Direct LookML Mapping (Low Effort)** | • Simple Set Analysis (`{<status={'Active'}>}`)<br>• What-If Variables (`vDiscountRate`)<br>• Section Access security<br>• Master Dimensions & Measures<br>• Drill-down hierarchies | • LookML `filters: [field: "val"]`<br>• LookML `parameter` + Liquid `{% parameter %}`<br>• User Attributes + `access_filter`<br>• Direct view dimensions & measures<br>• LookML `drill_fields` |
| **Category 2** | **Upstream dbt / Complex LookML (Medium Effort)** | • QVS Script ETL (`RESIDENT`, `LEFT JOIN`)<br>• Complex Set Analysis (`P()`, `E()`, `$(=...)`)<br>• Alternate States (comparative analysis)<br>• Data Islands (disconnected tables)<br>• Synthetic Keys (`$Syn`)<br>• Cyclic Dimensions | • Upstream dbt SQL models / BigQuery views<br>• LookML Native Derived Tables (NDTs)<br>• Duplicate Explore joins with templated filters<br>• Looker parameters / explicit `type: cross` joins<br>• Composite surrogate keys in Cloud Data Warehouse<br>• Looker parameter with dynamic CASE statement |
| **Category 3** | **Target Deprecated / Incompatible (Architectural Pivot)** | • Green / White / Gray Associative Engine<br>• In-Memory Global Smart Search<br>• Sheet-Level Actions & Document Triggers<br>• **Cyclic Data Model Loops (A-B-C-A)** | • Deprecated (educate on SQL WHERE / enable `cross_filtering: true`)<br>• Deprecated (use dimension filters / BigQuery Search)<br>• Deprecated (use native Looker URL parameters)<br>• **CRITICAL BLOCKER**: Break circular join loop in dbt |

### Fine-Grained Location Tracking & Grouping
Audit findings link directly to their exact origin:
- **Sheet Location:** Linked to specific sheets (e.g., `📊 1. Executive Revenue & Order Analytics`) and visual tiles (e.g., `Tile: Order Return Rate %`).
- **Data Model & Script:** Linked to `🗄️ Shared Data Model & Script`.
- **Global Items:** Linked to `⚙️ Global Master Items & Parameters`.
- Includes instant switching between **Grouped by Sheet View** (with per-sheet estimated remediation hours) and **Flat List View**.

---

## 💻 Quickstart & Execution

### Running the Web UI Studio

The Web Studio automatically binds to both port **8085** and **8080** for seamless access through cloud development workspaces, corporate proxies, or local browsers.

```bash
# Option A: Using the convenience launcher script
./run_local_studio.sh 8085

# Option B: Direct Python CLI
python3 -m enterprise_qlik.cli serve --port 8085
```

Open **`http://localhost:8085`** (or `http://localhost:8080`) in your browser.

---

### Command Line Interface (CLI)

The CLI provides headless, scriptable execution for automated CI/CD pipelines:

#### 1. Stage 1: Extract, Sanitize, and Compile Canonical IR
```bash
python3 -m enterprise_qlik.cli extract \
  --app-id "05bdadd9-0358-4a45-a16f-fc30a8aa16ef" \
  --output-dir ./migration_artifacts

# Outputs:
# - migration_artifacts/canonical_ir.json
# - migration_artifacts/feature_gaps.json
```

#### 2. Validate Canonical IR against JSON Schema
```bash
python3 -m enterprise_qlik.cli validate \
  --ir-file ./migration_artifacts/canonical_ir.json
```

#### 3. Stage 2: Generate Explore-Centric LookML & dbt Models
*(Consumes ONLY `canonical_ir.json` — zero Qlik connection needed)*
```bash
python3 -m enterprise_qlik.cli generate \
  --ir-file ./migration_artifacts/canonical_ir.json \
  --model-name "ecommerce_analytics" \
  --explore-name "order_items" \
  --output-dir ./looker_project

# Generates:
# - looker_project/models/ecommerce_analytics.model.lkml
# - looker_project/explores/order_items.explore.lkml
# - looker_project/views/*.view.lkml
# - looker_project/dashboards/*.dashboard.lookml
# - looker_project/dbt/*.sql
```

#### 4. Run 3-Tier Compatibility Gap Audit
```bash
python3 -m enterprise_qlik.cli audit \
  --input-file ./migration_artifacts/canonical_ir.json \
  --output-file ./migration_artifacts/audit_report.json
```

#### 5. Fleet Discovery from Terminal (Optional CLI)
```bash
python3 -m enterprise_qlik.cli discover
```

---

## 🧪 Comprehensive Test Suite

The test suite covers API routes, CORS preflights, instance connections, autonomous app discovery, multi-source sheet extraction, sanitization, 3-tier gap categorization, schema validation, LookML synthesis, and stage isolation:

```bash
python3 -m unittest discover tests -v
```

All 54 unit tests execute hermetically in ~2.0 seconds using standard Python `unittest`.

---

## 📦 Project Layout

```text
Enterprise_Qlik_to_Looker/
├── enterprise_qlik/
│   ├── stage1_extract/            # === STAGE 1: Source Extractor & IR Compiler ===
│   │   ├── connection.py          # Multi-Instance Service (Qlik Cloud SaaS & QSEoW)
│   │   ├── extractor.py           # WebSocket QIX Engine & Metadata Extractor
│   │   ├── sanitizer.py           # Regex PII, secrets, and token scrubber
│   │   ├── compatibility.py       # 3-Tier Gap Engine (All 11 items & location mapping)
│   │   ├── ir_compiler.py         # 2-Tier Canonical IR Compiler (Data Layer + Visual Catalog)
│   │   ├── schema_validator.py    # Formal JSON Schema validator
│   │   └── canonical_schema.json  # Draft 2020-12 Schema specification
│   │
│   ├── stage2_lookml/             # === STAGE 2: Decoupled Target Code Generator ===
│   │   ├── explore_compiler.py    # Star/Snowflake & Single-View Explore compiler
│   │   ├── view_compiler.py       # Dimensions, measures, parameters & Liquid filters
│   │   ├── dashboard_compiler.py  # LookML Dashboards bound strictly to Explores
│   │   ├── dbt_compiler.py        # Upstream dbt / BigQuery SQL models
│   │   └── generator.py           # Master Stage 2 orchestrator (Zero Qlik dependency)
│   │
│   ├── storage/                   # === DATABASE & PERSISTENCE LAYER ===
│   │   ├── db.py                  # DatabaseManager (SQLite WAL & PostgreSQL support)
│   │   └── migrations.py          # DDL schema migrations (waves, findings, apps, IR)
│   │
│   ├── web/                       # === WEB STUDIO & API SERVER ===
│   │   ├── server.py              # Pure standard library dual-port HTTP server
│   │   └── static/
│   │       ├── index.html         # Modern 6-view migration studio UI
│   │       ├── app.js             # Client SPA controller (cache-busted v2.6)
│   │       └── style.css          # MD3 Clean Light Theme styling
│   │
│   └── cli.py                     # Unified Command Line Interface
│
├── tests/                         # Hermetic Unit Tests (54 tests)
│   ├── test_compatibility.py
│   ├── test_database_storage.py
│   ├── test_explore_lookml.py
│   ├── test_extractor.py
│   ├── test_fleet_status.py
│   ├── test_instances.py
│   ├── test_ir_compiler.py
│   ├── test_sanitizer.py
│   ├── test_server.py
│   └── test_stage_separation.py
│
├── run_local_studio.sh            # Convenience one-click launcher
├── pyproject.toml
└── README.md
```

---

## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
