"""
AXIOM Impact Module
Phase 4: Estimate carbon footprint delta (CO2e) between original and compliant code.
"""

import re
import ast
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ComplexityLevel(Enum):
    """Code complexity levels for carbon estimation."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CarbonEstimate:
    """Carbon footprint estimate for code."""
    original_co2e: float
    alternative_co2e: float
    delta_co2e: float
    percentage_change: float
    energy_kwh_original: float
    energy_kwh_alternative: float
    complexity_score: int
    optimization_recommendations: List[str]


class ImpactAnalyzer:
    """
    Analyzes code for computational complexity and estimates carbon footprint.
    Uses baseline of 0.233 kg CO2/kWh.
    """
    
    # Energy consumption factors (kWh per operation type)
    ENERGY_FACTORS = {
        "cpu_cycle": 1e-12,  # Per CPU cycle
        "memory_access": 1e-11,  # Per memory access
        "disk_io": 1e-6,  # Per disk I/O operation
        "network_request": 1e-5,  # Per network request
        "gpu_cycle": 1e-10,  # Per GPU cycle
    }
    
    # Complexity multipliers
    COMPLEXITY_MULTIPLIERS = {
        ComplexityLevel.LOW: 1.0,
        ComplexityLevel.MEDIUM: 2.5,
        ComplexityLevel.HIGH: 5.0,
        ComplexityLevel.CRITICAL: 10.0
    }
    
    def __init__(self, carbon_baseline: float = 0.233):
        """
        Initialize impact analyzer.
        
        Args:
            carbon_baseline: kg CO2 per kWh (default: 0.233)
        """
        self.carbon_baseline = carbon_baseline
    
    def analyze_code(self, original_code: str, alternative_code: str) -> CarbonEstimate:
        """
        Analyze both original and alternative code for carbon impact.
        
        Args:
            original_code: Original code to analyze
            alternative_code: Privacy-compliant alternative code
            
        Returns:
            CarbonEstimate with detailed metrics
        """
        # Analyze complexity
        original_complexity = self._analyze_complexity(original_code)
        alternative_complexity = self._analyze_complexity(alternative_code)
        
        # Estimate energy consumption
        original_energy = self._estimate_energy(original_code, original_complexity)
        alternative_energy = self._estimate_energy(alternative_code, alternative_complexity)
        
        # Calculate CO2e
        original_co2e = original_energy * self.carbon_baseline
        alternative_co2e = alternative_energy * self.carbon_baseline
        
        # Calculate delta
        delta_co2e = alternative_co2e - original_co2e
        percentage_change = ((alternative_co2e - original_co2e) / original_co2e * 100) if original_co2e > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            original_complexity, alternative_complexity, delta_co2e
        )
        
        return CarbonEstimate(
            original_co2e=original_co2e,
            alternative_co2e=alternative_co2e,
            delta_co2e=delta_co2e,
            percentage_change=percentage_change,
            energy_kwh_original=original_energy,
            energy_kwh_alternative=alternative_energy,
            complexity_score=original_complexity["score"],
            optimization_recommendations=recommendations
        )
    
    def _analyze_complexity(self, code: str) -> Dict:
        """
        Analyze code complexity using multiple metrics.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Dictionary with complexity metrics
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"score": 1, "level": ComplexityLevel.LOW, "metrics": {}}
        
        metrics = {
            "cyclomatic_complexity": 0,
            "nested_loop_depth": 0,
            "function_count": 0,
            "loop_count": 0,
            "recursion_count": 0,
            "io_operations": 0,
            "network_operations": 0
        }
        
        # Count functions and complexity
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["function_count"] += 1
                metrics["cyclomatic_complexity"] += self._count_branches(node)
            elif isinstance(node, (ast.For, ast.While, ast.ListComp, ast.DictComp)):
                metrics["loop_count"] += 1
            elif isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name:
                    if any(io in func_name.lower() for io in ["open", "read", "write", "save", "load"]):
                        metrics["io_operations"] += 1
                    if any(net in func_name.lower() for net in ["request", "fetch", "api", "http", "url"]):
                        metrics["network_operations"] += 1
                    if func_name in self._get_function_names(tree):
                        metrics["recursion_count"] += 1
        
        # Calculate nested loop depth
        metrics["nested_loop_depth"] = self._calculate_nested_depth(tree)
        
        # Calculate overall complexity score
        score = (
            metrics["cyclomatic_complexity"] * 2 +
            metrics["nested_loop_depth"] * 3 +
            metrics["function_count"] +
            metrics["loop_count"] * 2 +
            metrics["recursion_count"] * 5 +
            metrics["io_operations"] * 2 +
            metrics["network_operations"] * 3
        )
        
        # Determine complexity level
        if score < 10:
            level = ComplexityLevel.LOW
        elif score < 30:
            level = ComplexityLevel.MEDIUM
        elif score < 60:
            level = ComplexityLevel.HIGH
        else:
            level = ComplexityLevel.CRITICAL
        
        return {"score": score, "level": level, "metrics": metrics}
    
    def _count_branches(self, node: ast.AST) -> int:
        """Count branch points in AST node."""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, 
                                  ast.ExceptHandler, ast.With,
                                  ast.comprehension)):
                count += 1
        return count
    
    def _get_call_name(self, node: ast.Call) -> Optional[str]:
        """Extract function name from call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
    
    def _get_function_names(self, tree: ast.AST) -> List[str]:
        """Get all function names defined in the tree."""
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    def _calculate_nested_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nested loop depth."""
        max_depth = 0
        
        def visit(node, depth=0):
            nonlocal max_depth
            if isinstance(node, (ast.For, ast.While, ast.ListComp, ast.DictComp)):
                depth += 1
                max_depth = max(max_depth, depth)
            for child in ast.iter_child_nodes(node):
                visit(child, depth)
        
        visit(tree)
        return max_depth
    
    def _estimate_energy(self, code: str, complexity: Dict) -> float:
        """
        Estimate energy consumption in kWh.
        
        Args:
            code: Source code
            complexity: Complexity analysis results
            
        Returns:
            Estimated energy in kWh
        """
        metrics = complexity.get("metrics", {})
        level = complexity.get("level", ComplexityLevel.LOW)
        
        # Base energy calculation
        base_energy = (
            metrics.get("function_count", 0) * 1000 * self.ENERGY_FACTORS["cpu_cycle"] +
            metrics.get("loop_count", 0) * 10000 * self.ENERGY_FACTORS["cpu_cycle"] +
            metrics.get("io_operations", 0) * self.ENERGY_FACTORS["disk_io"] +
            metrics.get("network_operations", 0) * self.ENERGY_FACTORS["network_request"] +
            metrics.get("recursion_count", 0) * 50000 * self.ENERGY_FACTORS["cpu_cycle"]
        )
        
        # Apply complexity multiplier
        multiplier = self.COMPLEXITY_MULTIPLIERS[level]
        
        # Estimate for 1000 executions
        total_energy = base_energy * multiplier * 1000
        
        return total_energy
    
    def _generate_recommendations(self, 
                                   original: Dict, 
                                   alternative: Dict, 
                                   delta: float) -> List[str]:
        """
        Generate optimization recommendations based on analysis.
        
        Args:
            original: Original code complexity
            alternative: Alternative code complexity
            delta: CO2e difference
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        orig_metrics = original.get("metrics", {})
        alt_metrics = alternative.get("metrics", {})
        
        if delta > 0:
            recommendations.append(
                f"⚠️ Privacy-compliant code increases carbon footprint by {delta:.4f} kg CO2e"
            )
            recommendations.append(
                "Consider: Implement caching to reduce repeated computation"
            )
        else:
            recommendations.append(
                f"✅ Privacy-compliant code reduces carbon footprint by {abs(delta):.4f} kg CO2e"
            )
        
        if orig_metrics.get("nested_loop_depth", 0) > 2:
            recommendations.append(
                "Optimize: Reduce nested loop depth to improve efficiency"
            )
        
        if orig_metrics.get("network_operations", 0) > alt_metrics.get("network_operations", 0):
            recommendations.append(
                "✅ Alternative reduces network calls, improving efficiency"
            )
        
        if orig_metrics.get("io_operations", 0) > 5:
            recommendations.append(
                "Consider: Batch I/O operations to reduce disk access"
            )
        
        if original.get("level") == ComplexityLevel.CRITICAL:
            recommendations.append(
                "⚠️ Critical complexity detected - consider code refactoring"
            )
        
        return recommendations
    
    def generate_impact_report(self, estimate: CarbonEstimate) -> str:
        """
        Generate formatted impact report.
        
        Args:
            estimate: Carbon estimate to report
            
        Returns:
            Formatted markdown report
        """
        report = []
        report.append("## Carbon Footprint Impact Analysis")
        report.append("")
        report.append("### Energy Consumption")
        report.append(f"- **Original Code**: {estimate.energy_kwh_original:.6f} kWh")
        report.append(f"- **Alternative Code**: {estimate.energy_kwh_alternative:.6f} kWh")
        report.append("")
        report.append("### Carbon Emissions (CO2e)")
        report.append(f"- **Original Code**: {estimate.original_co2e:.6f} kg CO2e")
        report.append(f"- **Alternative Code**: {estimate.alternative_co2e:.6f} kg CO2e")
        report.append(f"- **Delta**: {estimate.delta_co2e:+.6f} kg CO2e")
        report.append(f"- **Percentage Change**: {estimate.percentage_change:+.2f}%")
        report.append("")
        report.append("### Complexity Score")
        report.append(f"- **Score**: {estimate.complexity_score}")
        report.append("")
        report.append("### Optimization Recommendations")
        for rec in estimate.optimization_recommendations:
            report.append(f"- {rec}")
        
        return "\n".join(report)
