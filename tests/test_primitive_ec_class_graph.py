"""Tests for the primitive elliptic-curve class graph projection."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_ec_class_graph import (  # noqa: E402
    PrimitiveEdge,
    build_primitive_graph,
    component_stats,
    export_gephi_tables,
    project_edge,
    summarize_primitive_graph,
)


def test_project_edge_tracks_cross_edges_and_loops() -> None:
    cross = project_edge({"u": [24, 60], "v": [32, 45]})
    loop = project_edge({"u": [24, 60], "v": [36, 90]})

    assert cross == PrimitiveEdge(
        source=(2, 5),
        target=(32, 45),
        source_scale=12,
        target_scale=1,
    )
    assert not cross.is_loop
    assert loop.source == (2, 5)
    assert loop.target == (2, 5)
    assert loop.is_loop


def test_build_primitive_graph_keeps_loop_weight_separate() -> None:
    rows = [
        {"u": [24, 60], "v": [32, 45]},
        {"u": [48, 120], "v": [64, 90]},
        {"u": [24, 60], "v": [36, 90]},
    ]

    graph = build_primitive_graph(rows)

    assert graph.node_count == 2
    assert graph.edge_count == 1
    assert graph.loop_raw_edges == 1
    assert graph.loop_template_count == 1
    assert graph.edge_weights[((2, 5), (32, 45))] == 2
    assert graph.loop_weights[(2, 5)] == 1


def test_component_stats_reports_largest_component_and_circuit_rank() -> None:
    rows = [
        {"u": [2, 5], "v": [3, 4]},
        {"u": [3, 4], "v": [5, 12]},
        {"u": [5, 12], "v": [2, 5]},
        {"u": [7, 24], "v": [8, 15]},
    ]

    graph = build_primitive_graph(rows)
    stats = component_stats(graph)

    assert stats["component_count"] == 2
    assert stats["largest_component_size"] == 3
    assert stats["largest_component_edges"] == 3
    assert stats["largest_component_circuit_rank"] == 1
    assert stats["component_size_hist"]["2"] == 1
    assert stats["component_size_hist"]["3"] == 1


def test_summarize_primitive_graph_includes_core_and_clustering() -> None:
    rows = [
        {"u": [2, 5], "v": [3, 4]},
        {"u": [3, 4], "v": [5, 12]},
        {"u": [5, 12], "v": [2, 5]},
        {"u": [2, 5], "v": [7, 24]},
        {"u": [10, 25], "v": [14, 35]},
    ]

    summary = summarize_primitive_graph(rows, top=3)

    assert summary["raw_edges_used"] == 5
    assert summary["primitive_nodes"] == 4
    assert summary["primitive_edges"] == 4
    assert summary["loop_raw_edges"] == 1
    assert summary["components"]["largest_component_size"] == 4
    assert summary["cycle"]["circuit_rank"] == 1
    assert summary["core_2"]["nodes"] == 3
    assert summary["clustering"]["transitivity"] == 0.6


def test_summarize_primitive_graph_can_filter_raw_vertices() -> None:
    rows = [
        {"u": [24, 60], "v": [32, 45]},
        {"u": [32, 45], "v": [20, 21]},
        {"u": [7, 24], "v": [8, 15]},
    ]
    raw_vertices = {(24, 60), (32, 45), (20, 21)}

    summary = summarize_primitive_graph(rows, raw_vertices=raw_vertices)

    assert summary["raw_edges_seen"] == 3
    assert summary["raw_edges_used"] == 2
    assert summary["raw_edges_skipped_by_filter"] == 1
    assert summary["primitive_nodes"] == 3


def test_export_gephi_tables_writes_nodes_edges_and_summary(tmp_path: Path) -> None:
    rows = [
        {"u": [24, 60], "v": [32, 45]},
        {"u": [48, 120], "v": [64, 90]},
        {"u": [32, 45], "v": [20, 21]},
        {"u": [24, 60], "v": [36, 90]},
    ]
    graph = build_primitive_graph(rows)

    summary = export_gephi_tables(graph, tmp_path)

    nodes_csv = tmp_path / "nodes.csv"
    edges_csv = tmp_path / "edges.csv"
    assert nodes_csv.exists()
    assert edges_csv.exists()
    assert (tmp_path / "summary.json").exists()
    assert "Id,Label,A,B,degree,weighted_degree,loop_raw_edges,core_2,core_3" in nodes_csv.read_text()
    assert "Source,Target,Type,Weight" in edges_csv.read_text()
    assert '2_5,"(2,5)",2,5,1,2,1,false,false' in nodes_csv.read_text()
    assert "2_5,32_45,Undirected,2" in edges_csv.read_text()
    assert summary["node_count"] == 3
    assert summary["edge_count"] == 2
    assert summary["loop_raw_edges"] == 1
