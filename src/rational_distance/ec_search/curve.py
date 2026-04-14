"""Quartic elliptic-curve rules for one Pythagorean triple."""

from __future__ import annotations

from fractions import Fraction

from rational_distance.math_utils import rational_sqrt

from .models import ECCurveEdgeRecord, ECCurveNodeRecord, ECOrbitTrace, ECSeedBranch


class QuarticEC:
    """Quartic elliptic curve E^2 = F(t) associated with triple (p, q, r)."""

    def __init__(self, p: int, q: int, r: int) -> None:
        self.p = p
        self.q = q
        self.r = r
        self.c4 = r * r
        self.c3 = 4 * q * r
        self.c2 = 2 * r * r + 4 * p * q
        self.c1 = 4 * r * (2 * p - q)
        self.c0 = 4 * p * p - 4 * p * q + r * r

    def F(self, t: Fraction) -> Fraction:
        return self.c4 * t**4 + self.c3 * t**3 + self.c2 * t**2 + self.c1 * t + self.c0

    def on_curve(self, t: Fraction, E: Fraction) -> bool:
        return self.F(t) == E * E

    def k_from_t(self, t: Fraction) -> Fraction | None:
        denom = 1 - t * t
        if denom == 0:
            return None
        return 2 * (t + Fraction(self.p, self.r)) / denom

    def t_from_k_dB(self, k: Fraction, dB: Fraction) -> list[Fraction]:
        if k == 0:
            return []
        return [(-1 + dB) / k, (-1 - dB) / k]

    def E_from_t_dD(self, t: Fraction, dD: Fraction) -> Fraction:
        return Fraction(self.r) * dD * (1 - t * t)

    def _tangent_quadratic(self, t0: Fraction, E0: Fraction) -> tuple[Fraction, Fraction, Fraction]:
        Fp = 4 * self.c4 * t0**3 + 3 * self.c3 * t0**2 + 2 * self.c2 * t0 + self.c1
        slope = Fp / (2 * E0)
        A = Fraction(self.c4)
        B = Fraction(self.c3) + 2 * A * t0
        C = Fraction(self.c2) - slope**2 + 2 * Fraction(self.c3) * t0 + 3 * A * t0**2
        return A, B, C

    def _secant_quadratic(
        self,
        t1: Fraction,
        E1: Fraction,
        t2: Fraction,
        E2: Fraction,
    ) -> tuple[Fraction, Fraction, Fraction]:
        slope = (E2 - E1) / (t2 - t1)
        A = Fraction(self.c4)
        B = Fraction(self.c3) + A * (t1 + t2)
        C = Fraction(self.c2) - slope**2 + B * (t1 + t2) - A * t1 * t2
        return A, B, C

    def _new_t_from_line(
        self,
        A: Fraction,
        B: Fraction,
        C: Fraction,
        slope: Fraction,
        intercept: Fraction,
    ) -> list[tuple[Fraction, Fraction]]:
        disc = B * B - 4 * A * C
        sqrt_disc = rational_sqrt(disc)
        if sqrt_disc is None:
            return []
        results = []
        for sign in [1, -1]:
            t_new = (-B + sign * sqrt_disc) / (2 * A)
            E_new = slope * t_new + intercept
            results.append((t_new, E_new))
        return results

    def tangent_points(self, t0: Fraction, E0: Fraction) -> list[tuple[Fraction, Fraction]]:
        A, B, C = self._tangent_quadratic(t0, E0)
        Fp = 4 * self.c4 * t0**3 + 3 * self.c3 * t0**2 + 2 * self.c2 * t0 + self.c1
        slope = Fp / (2 * E0)
        intercept = E0 - slope * t0
        pts = self._new_t_from_line(A, B, C, slope, intercept)
        return [(t, E) for t, E in pts if t != t0]

    def secant_points(
        self,
        t1: Fraction,
        E1: Fraction,
        t2: Fraction,
        E2: Fraction,
    ) -> list[tuple[Fraction, Fraction]]:
        if t1 == t2:
            return []
        A, B, C = self._secant_quadratic(t1, E1, t2, E2)
        slope = (E2 - E1) / (t2 - t1)
        intercept = E1 - slope * t1
        pts = self._new_t_from_line(A, B, C, slope, intercept)
        return [(t, E) for t, E in pts if t != t1 and t != t2]

    def expand_orbit(
        self,
        seeds: list[tuple[Fraction, Fraction]],
        max_steps: int = 20,
        max_denom: int = 10**18,
    ) -> list[Fraction]:
        orbit: dict[Fraction, Fraction] = {}
        for t, E in seeds:
            if abs(t.denominator) <= max_denom:
                orbit[t] = E

        queue = list(orbit.items())
        step = 0

        while queue and step < max_steps:
            step += 1
            new_pts: list[tuple[Fraction, Fraction]] = []

            for t0, E0 in queue:
                for t_new, E_new in self.tangent_points(t0, E0):
                    if t_new not in orbit and abs(t_new.denominator) <= max_denom:
                        new_pts.append((t_new, E_new))

            frontier = list(orbit.items())
            for index_a in range(len(frontier)):
                for index_b in range(index_a + 1, len(frontier)):
                    t1, E1 = frontier[index_a]
                    t2, E2 = frontier[index_b]
                    for t_new, E_new in self.secant_points(t1, E1, t2, E2):
                        if t_new not in orbit and abs(t_new.denominator) <= max_denom:
                            new_pts.append((t_new, E_new))
                    for t_new, E_new in self.secant_points(t1, E1, t2, -E2):
                        if t_new not in orbit and abs(t_new.denominator) <= max_denom:
                            new_pts.append((t_new, E_new))

            if not new_pts:
                break

            for t_new, E_new in new_pts:
                if t_new not in orbit:
                    orbit[t_new] = E_new
            queue = new_pts

        k_values = []
        for t in orbit:
            k = self.k_from_t(t)
            if k is not None and k > 0:
                k_values.append(k)
        return k_values

    def expand_orbit_trace(
        self,
        seed_branches: list[ECSeedBranch],
        max_steps: int = 20,
        max_denom: int = 10**18,
    ) -> ECOrbitTrace:
        nodes: list[ECCurveNodeRecord] = []
        edges: list[ECCurveEdgeRecord] = []
        node_lookup: dict[tuple[Fraction, Fraction], int] = {}
        edge_keys: set[tuple[int, int, str, int]] = set()
        seed_primary_nodes: dict[int, int] = {}

        def _kind_rank(kind: str) -> int:
            return {"conjugate_branch": 0, "seed_branch": 1, "orbit": 2}.get(kind, -1)

        def ensure_node(
            t: Fraction,
            E: Fraction,
            kind: str,
            step: int,
            seed_index: int | None = None,
        ) -> int:
            key = (t, E)
            existing = node_lookup.get(key)
            if existing is not None:
                node = nodes[existing]
                if _kind_rank(kind) > _kind_rank(node.kind):
                    node.kind = kind
                if seed_index is not None and node.seed_index is None:
                    node.seed_index = seed_index
                node.step = min(node.step, step)
                return existing

            node_index = len(nodes)
            nodes.append(
                ECCurveNodeRecord(
                    node_index=node_index,
                    t=t,
                    E=E,
                    kind=kind,
                    step=step,
                    seed_index=seed_index,
                )
            )
            node_lookup[key] = node_index
            if seed_index is not None and seed_index not in seed_primary_nodes:
                seed_primary_nodes[seed_index] = node_index
            return node_index

        active_orbit: dict[Fraction, int] = {}
        for branch in seed_branches:
            if abs(branch.t.denominator) > max_denom:
                continue
            node_index = ensure_node(branch.t, branch.E, "seed_branch", 0, branch.seed_index)
            active_orbit[branch.t] = node_index

        queue = list(active_orbit.values())
        step = 0

        while queue and step < max_steps:
            step += 1
            new_active: list[tuple[Fraction, int]] = []
            pending_t: set[Fraction] = set()

            for parent_index in queue:
                parent = nodes[parent_index]
                for t_new, E_new in self.tangent_points(parent.t, parent.E):
                    if abs(t_new.denominator) > max_denom:
                        continue
                    child_index = ensure_node(t_new, E_new, "orbit", step)
                    edge_key = (child_index, parent_index, "tangent", 0)
                    if edge_key not in edge_keys:
                        edge_keys.add(edge_key)
                        edges.append(ECCurveEdgeRecord(child_index, parent_index, "tangent", 0))
                    if t_new not in active_orbit and t_new not in pending_t:
                        pending_t.add(t_new)
                        new_active.append((t_new, child_index))

            frontier = list(active_orbit.values())
            for index_a in range(len(frontier)):
                for index_b in range(index_a + 1, len(frontier)):
                    parent_a = nodes[frontier[index_a]]
                    parent_b = nodes[frontier[index_b]]
                    for t_new, E_new in self.secant_points(
                        parent_a.t, parent_a.E, parent_b.t, parent_b.E
                    ):
                        if abs(t_new.denominator) > max_denom:
                            continue
                        child_index = ensure_node(t_new, E_new, "orbit", step)
                        for position, parent_index in enumerate(
                            (frontier[index_a], frontier[index_b])
                        ):
                            edge_key = (child_index, parent_index, "secant", position)
                            if edge_key not in edge_keys:
                                edge_keys.add(edge_key)
                                edges.append(
                                    ECCurveEdgeRecord(
                                        child_index=child_index,
                                        parent_index=parent_index,
                                        relation="secant",
                                        position=position,
                                    )
                                )
                        if t_new not in active_orbit and t_new not in pending_t:
                            pending_t.add(t_new)
                            new_active.append((t_new, child_index))

                    neg_parent_index = ensure_node(
                        parent_b.t,
                        -parent_b.E,
                        "conjugate_branch",
                        parent_b.step,
                        parent_b.seed_index,
                    )
                    for t_new, E_new in self.secant_points(
                        parent_a.t, parent_a.E, parent_b.t, -parent_b.E
                    ):
                        if abs(t_new.denominator) > max_denom:
                            continue
                        child_index = ensure_node(t_new, E_new, "orbit", step)
                        for position, parent_index in enumerate(
                            (frontier[index_a], neg_parent_index)
                        ):
                            edge_key = (child_index, parent_index, "secant_neg_branch", position)
                            if edge_key not in edge_keys:
                                edge_keys.add(edge_key)
                                edges.append(
                                    ECCurveEdgeRecord(
                                        child_index=child_index,
                                        parent_index=parent_index,
                                        relation="secant_neg_branch",
                                        position=position,
                                    )
                                )
                        if t_new not in active_orbit and t_new not in pending_t:
                            pending_t.add(t_new)
                            new_active.append((t_new, child_index))

            if not new_active:
                break

            queue = []
            for t_new, child_index in new_active:
                if t_new not in active_orbit:
                    active_orbit[t_new] = child_index
                    queue.append(child_index)

        for node_index in active_orbit.values():
            nodes[node_index].active = True

        return ECOrbitTrace(
            nodes=nodes,
            edges=edges,
            active_node_indices=list(active_orbit.values()),
            seed_primary_nodes=seed_primary_nodes,
        )


__all__ = ["QuarticEC"]
