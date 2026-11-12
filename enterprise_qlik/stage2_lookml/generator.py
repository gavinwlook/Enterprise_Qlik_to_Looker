"""
Master Stage 2 Generator Orchestrator
=====================================
Coordinates the compilation of LookML models, Explores, views, dashboards,
and dbt blueprints from a Canonical IR input package.

CRITICAL ARCHITECTURAL GUARANTEE:
This module has ZERO imports from Stage 1 or Qlik.
It can run in an isolated environment with only the Canonical IR JSON.
"""

import json
import os
from typing import Any, Dict, Optional, Union
from enterprise_qlik.stage2_lookml.explore_compiler import ExploreCompiler
from enterprise_qlik.stage2_lookml.view_compiler import ViewCompiler
from enterprise_qlik.stage2_lookml.dashboard_compiler import DashboardCompiler
from enterprise_qlik.stage2_lookml.dbt_compiler import DbtBlueprintCompiler


class LookMLGenerator:
    """Consumes Canonical IR to generate LookML Explores, Views, Dashboards, and dbt models."""

    def __init__(self, model_name: str = "enterprise_analytics"):
        self.model_name = model_name
        self.explore_compiler = ExploreCompiler(model_name=model_name)
        self.view_compiler = ViewCompiler()
        self.dashboard_compiler = DashboardCompiler(model_name=model_name)
        self.dbt_compiler = DbtBlueprintCompiler()

    def generate(
        self,
        canonical_ir_input: Union[str, Dict[str, Any]],
        target_explore_name: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes complete Stage 2 target code generation from Canonical IR.
        """
        if isinstance(canonical_ir_input, str):
            with open(canonical_ir_input, "r", encoding="utf-8") as f:
                canonical_ir = json.load(f)
        else:
            canonical_ir = canonical_ir_input

        # 1. Compile LookML Explore & Model
        explore_result = self.explore_compiler.compile_explore(
            canonical_ir=canonical_ir,
            target_explore_name=target_explore_name,
        )
        explore_name = explore_result["explore_name"]
        root_view_name = explore_result["root_view"]

        # 2. Compile LookML Views
        views = self.view_compiler.compile_views(canonical_ir=canonical_ir)

        # 3. Compile LookML Dashboards (bound strictly to explore_name)
        dashboards = self.dashboard_compiler.compile_dashboards(
            canonical_ir=canonical_ir,
            explore_name=explore_name,
            root_view_name=root_view_name,
        )

        # 4. Compile dbt Blueprints
        dbt_models = self.dbt_compiler.compile_blueprints(canonical_ir=canonical_ir)

        artifacts = {
            "model": {
                f"{self.model_name}.model.lkml": explore_result["model_lkml"],
            },
            "explores": {
                f"{explore_name}.explore.lkml": explore_result["explore_lkml"],
            },
            "views": views,
            "dashboards": dashboards,
            "dbt_models": dbt_models,
            "metadata": {
                "explore_name": explore_name,
                "root_view": root_view_name,
                "is_single_view": explore_result["is_single_view"],
                "total_views": len(views),
                "total_dashboards": len(dashboards),
            },
        }

        # Write to disk if output_dir specified
        if output_dir:
            self._write_artifacts(artifacts, output_dir)

        return artifacts

    def _write_artifacts(self, artifacts: Dict[str, Any], base_dir: str):
        os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "views"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "dashboards"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "dbt"), exist_ok=True)

        for fname, content in artifacts["model"].items():
            with open(os.path.join(base_dir, "models", fname), "w", encoding="utf-8") as f:
                f.write(content)

        for fname, content in artifacts["views"].items():
            with open(os.path.join(base_dir, "views", fname), "w", encoding="utf-8") as f:
                f.write(content)

        for fname, content in artifacts["dashboards"].items():
            with open(os.path.join(base_dir, "dashboards", fname), "w", encoding="utf-8") as f:
                f.write(content)

        for fname, content in artifacts["dbt_models"].items():
            with open(os.path.join(base_dir, "dbt", fname), "w", encoding="utf-8") as f:
                f.write(content)
