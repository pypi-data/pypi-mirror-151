from __future__ import annotations

import copy
import sys
from collections import defaultdict
from itertools import chain
from os import PathLike
from random import randint
from random import random
from random import shuffle
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Sequence
from typing import Type

import numpy as np
from negmas import Agent
from negmas.helpers import get_class
from negmas.helpers import get_full_type_name
from negmas.helpers import unique_name
from negmas.helpers.numeric import truncated_mean
from negmas.serialization import deserialize
from negmas.serialization import serialize
from negmas.tournaments import TournamentResults
from negmas.tournaments import WorldRunResults
from negmas.tournaments import tournament

from scml.oneshot.agents import GreedyOneShotAgent
from scml.oneshot.agents import GreedySyncAgent
from scml.oneshot.agents import SingleAgreementAspirationAgent
from scml.oneshot.sysagents import _SystemAgent as OneShotSysAgent
from scml.oneshot.world import SCML2020OneShotWorld
from scml.scml2020.agent import _SystemAgent as StdSysAgent
from scml.scml2020.agents import BuyCheapSellExpensiveAgent
from scml.scml2020.agents import DecentralizingAgent
from scml.scml2020.agents import MarketAwareIndDecentralizingAgent
from scml.scml2020.agents import SatisficerAgent
from scml.scml2020.world import SCML2020Agent
from scml.scml2020.world import SCML2020World
from scml.scml2020.world import SCML2021World
from scml.scml2020.world import SCML2022World
from scml.scml2020.world import is_system_agent

# try:
# except Exception as e:
#
#     def truncated_mean(
#         scores: np.ndarray,
#         limits: tuple[float, float] | None = None,
#         top_limit=2.0,
#         bottom_limit=float("inf"),
#         base="tukey",
#         return_limits=False,
#     ) -> float | tuple[float, tuple[float, float] | None]:
#         """
#         Calculates the truncated mean
#
#         Args:
#             scores: A list of scores for which to calculate the truncated mean
#             limits: The limits to use for trimming the scores. If not given, they will
#                     be calculated based on `top_fraction`, `bottom_fraction` and `base.`
#                     You can pass the special value "mean" as a string to disable limits and
#                     calcualte the mean. You can pass the special value "median" to calculate
#                     the median (which is the same as passing top_fraction==bottom_fraction=0.5
#                     and base == "scores").
#             top_limit: top limit on scores to use for truncated mean calculation. See `base`
#             bottom_limit: bottom limit on scores to use for truncated mean calculation. See `base`
#             base: The base for calculating the limits used to apply the `top_limit` and `bottom_limit`.
#                   Possible values are:
#                   - zscore: the number of sigmas to remove above/below. A good default choice is 3. Pass inf to disable a side.
#                   - tukey: the fraction of IQR to remove above/below. A good default choice is 1.5 or 3 (we use 2). Pass inf to disable a side.
#                   - iqr : same as tukey
#                   - iqr_fraction: the fraction is interpreted as the fraction of scores above/below the 1st/3rd qauntile
#                   - scores: the fraction is interpreted as fraction of highest and lowest scores
#                   - fraction: the fraction is interpreted as literal fraction of the values (i.e. given 10 values and 0.1, removes 1 value)
#                   - mean: simply returns the mean (limits ignored)
#                   - median: simply returns the median (limits ignored)
#             return_limits: If true, the method will also return the limiting scores used in its mean calculation.
#         """
#
#         scores = np.asarray(scores)
#         scores = scores[~np.isnan(scores)]
#
#         if isinstance(limits, str) and limits.lower() == "mean":
#             return (
#                 tmean(scores, None)
#                 if not return_limits
#                 else (tmean(scores, None), None)
#             )
#         if isinstance(limits, str) and limits.lower() == "median":
#             return np.median(scores) if not return_limits else (np.median(scores), None)
#         if limits is not None:
#             return np.mean(scores) if not return_limits else (np.mean(scores), None)
#
#         if base == "zscore":
#             m, s = np.nanmean(scores), np.nanstd(scores)
#             limits = (m - s * bottom_limit, m + s * top_limit)
#         elif base in ("tukey", "iqr"):
#             q1, q3 = np.quantile(scores, 0.25), np.quantile(scores, 0.75)
#             iqr = q3 - q1
#             limits = (
#                 q1
#                 - (bottom_limit * iqr if not np.isinf(bottom_limit) else bottom_limit),
#                 q3 + (top_limit * iqr if not np.isinf(top_limit) else top_limit),
#             )
#         elif base == "iqr_fraction":
#             bottom_limit = min(1, max(0, bottom_limit))
#             top_limit = min(1, max(0, top_limit))
#             limits = (np.quantile(scores, 0.25), np.quantile(scores, 0.75))
#             high = np.sort(scores[scores > limits[1]])
#             low = np.sort(scores[scores < limits[0]])
#             limits = (
#                 low[int((len(low) - 1) * bottom_limit)] if len(low) > 0 else None,
#                 high[int((len(high) - 1) * (1 - top_limit))] if len(high) > 0 else None,
#             )
#         elif base == "fraction":
#             bottom_limit = min(1, max(0, bottom_limit))
#             top_limit = min(1, max(0, top_limit))
#             scores = np.sort(scores)
#             top_indx = int((len(scores) - 1) * (1 - top_limit))
#             bottom_indx = int((len(scores) - 1) * bottom_limit)
#             if top_indx < bottom_indx:
#                 return float("nan") if not return_limits else (float("nan"), limits)
#             m = np.mean(scores[bottom_indx : top_indx + 1])
#             return (
#                 m if not return_limits else (m, (scores[bottom_indx], scores[top_indx]))
#             )
#         elif base == "scores":
#             bottom_limit = min(1, max(0, bottom_limit))
#             top_limit = min(1, max(0, top_limit))
#             limits = (
#                 np.quantile(scores, bottom_limit),
#                 np.quantile(scores, 1 - top_limit),
#             )
#             if limits[0] > limits[1]:
#                 return float("nan") if not return_limits else (float("nan"), limits)
#         elif base == "mean":
#             return np.mean(scores) if not return_limits else (np.mean(scores), None)
#         elif base == "median":
#             return np.median(scores) if not return_limits else (np.median(scores), None)
#         else:
#             raise ValueError(f"Unknown base for truncated_mean ({base})")
#         if len(scores) == 0 or limits[1] < limits[0]:
#             return float("nan") if not return_limits else (float("nan"), limits)
#         try:
#             # this is an inclusive trimmed mean
#             # tm = tmean(scores, limits)
#             scores = scores[scores >= limits[0]]
#             scores = scores[scores <= limits[1]]
#             if len(scores) == 0:
#                 return float("nan") if not return_limits else (float("nan"), limits)
#             tm = np.mean(scores)
#             return tm if not return_limits else (tm, limits)
#         except ValueError:
#             return float("nan") if not return_limits else (float("nan"), limits)
#


__all__ = [
    "anac2020_config_generator",
    "anac2021_config_generator_collusion",
    "anac2020_assigner",
    "anac2020_world_generator",
    "anac2020_tournament",
    "anac2020_collusion",
    "anac2020_std",
    "balance_calculator2020",
    "balance_calculator2021",
    "balance_calculator2021oneshot",
    "balance_calculator2021collusion",
    "DefaultAgents",
    "DefaultAgents2021",
    "DefaultAgents2022",
    "DefaultAgentsOneShot",
    "anac2021_collusion",
    "anac2021_std",
    "anac2021_oneshot",
    "anac2022_collusion",
    "anac2022_std",
    "anac2022_oneshot",
]


FORCED_LOGS_FRACTION = 1.0


ROUND_ROBIN = True


DefaultAgents: tuple[type[SCML2020Agent], ...] = (
    DecentralizingAgent,
    BuyCheapSellExpensiveAgent,
)


DefaultAgents2021 = [
    DecentralizingAgent,
    # MarketAwareDecentralizingAgent,
    MarketAwareIndDecentralizingAgent,
    SatisficerAgent,
    # RandomOneShotAgent,
]

DefaultAgents2022 = [
    DecentralizingAgent,
    # MarketAwareDecentralizingAgent,
    MarketAwareIndDecentralizingAgent,
    SatisficerAgent,
    # RandomOneShotAgent,
]


DefaultAgentsOneShot = [
    GreedyOneShotAgent,
    SingleAgreementAspirationAgent,
    GreedySyncAgent,
]


def integer_cut(
    n: int,
    l: int,
    l_m: int | list[int],
    l_max: int | list[int] = float("inf"),  # type: ignore
) -> list[int]:
    """
    Generates l random integers that sum to n where each of them is at least l_m
    Args:
        n: total
        l: number of levels
        l_m: minimum per level
        l_max: maximum per level. Can be set to infinity

    Returns:

    """
    if not isinstance(l_m, Iterable):
        l_m = [l_m] * l
    if not isinstance(l_max, Iterable):
        l_max = [l_max] * l
    sizes = np.asarray(l_m)
    if n < sizes.sum():
        raise ValueError(
            f"Cannot generate {l} numbers summing to {n}  with a minimum summing to {sizes.sum()}"
        )
    maxs = np.asarray(l_max)
    if n > maxs.sum():
        raise ValueError(
            f"Cannot generate {l} numbers summing to {n}  with a maximum summing to {maxs.sum()}"
        )
    # TODO  That is most likely the most stupid way to do it. We just try blindly. There MUST be a better way
    while sizes.sum() < n:
        indx = randint(0, l - 1)
        if sizes[indx] >= l_max[indx]:
            continue
        sizes[indx] += 1
    return list(sizes.tolist())


def integer_cut_dynamic(
    n: int, l_min: int, l_max: int, min_levels: int = 0
) -> list[int]:
    """
    Generates a list random integers that sum to n where each of them is between l_m and l_max

    Args:
        n: total
        l_min: minimum per level
        l_max: maximum per level. Can be set to infinity
        min_levels: THe minimum number of levels to use

    Returns:

    """
    if n < min_levels * l_min:
        raise ValueError(
            f"Cannot cut {n} into at least {min_levels} numbers each is at least {l_min}"
        )

    sizes = [l_min] * min_levels

    for i in range(len(sizes)):
        sizes[i] += randint(0, l_max - l_min)

    while sum(sizes) < n:
        i = randint(l_min, l_max)
        sizes.append(i)

    to_remove = sum(sizes) - n
    if to_remove == 0:
        return sizes

    sizes = sorted(sizes, reverse=True)
    for i, x in enumerate(sizes):
        can_remove = x - l_min
        removed = min(can_remove, to_remove)
        sizes[i] -= removed
        to_remove -= removed
        if sum(sizes) == n:
            break
    sizes = [_ for _ in sizes if _ > 0]
    shuffle(sizes)
    assert sum(sizes) == n, f"n={n}\nsizes={sizes}"
    return sizes


def _realin(rng: tuple[float, float] | float) -> float:
    """
    Selects a random number within a range if given or the input if it was a float

    Args:
        rng: Range or single value

    Returns:

        the real within the given range
    """
    if isinstance(rng, float):
        return rng
    if abs(rng[1] - rng[0]) < 1e-8:
        return rng[0]
    return rng[0] + random() * (rng[1] - rng[0])


def _intin(rng: tuple[int, int] | int) -> int:
    """
    Selects a random number within a range if given or the input if it was an int

    Args:
        rng: Range or single value

    Returns:

        the int within the given range
    """
    if not isinstance(rng, Iterable):
        return int(rng)
    if rng[0] == rng[1]:
        return rng[0]
    return randint(rng[0], rng[1])


def anac2020_config_generator(
    n_competitors: int,
    n_agents_per_competitor: int,
    agent_names_reveal_type: bool = False,
    non_competitors: tuple[str | type[SCML2020Agent], ...] | None = None,
    non_competitor_params: tuple[dict[str, Any], ...] | None = None,
    compact: bool = False,
    *,
    n_steps: int | tuple[int, int] = (50, 200),
    n_processes: tuple[int, int] = (
        2,
        4,
    ),  # minimum is strictly guarantee but maximum is only guaranteed if select_n_levels_first
    min_factories_per_level: int = 2,  # strictly guaranteed
    max_factories_per_level: int = 6,  # not strictly guaranteed except if select_n_levels_first is False
    n_lines: int = 10,
    select_n_levels_first=True,
    oneshot_world: bool = False,
    **kwargs,
) -> list[dict[str, Any]]:
    if non_competitors is None:
        non_competitors = DefaultAgents
        non_competitor_params = tuple(dict() for _ in non_competitors)
    if isinstance(n_processes, Iterable):
        n_processes = tuple(n_processes)
    else:
        n_processes = (n_processes, n_processes)

    n_steps = _intin(n_steps)

    if select_n_levels_first:
        n_processes = randint(*n_processes)
        n_agents = n_agents_per_competitor * n_competitors
        n_default_managers = max(0, n_processes * min_factories_per_level)
        n_defaults = integer_cut(n_default_managers, n_processes, 0)
        n_a_list = integer_cut(n_agents, n_processes, 0)
        for i, n_a in enumerate(n_a_list):
            if n_a + n_defaults[i] < min_factories_per_level:
                n_defaults[i] = min_factories_per_level - n_a
            if n_a + n_defaults[i] > max_factories_per_level and n_defaults[i] > 1:
                n_defaults[i] = max(1, min_factories_per_level - n_a)
        n_f_list = [a + b for a, b in zip(n_defaults, n_a_list)]
    else:
        min_n_processes = randint(*n_processes)
        n_agents = n_agents_per_competitor * n_competitors
        n_default_managers = max(
            0, min_n_processes * min_factories_per_level - n_agents
        )
        n_f_list = integer_cut_dynamic(
            n_agents + n_default_managers,
            min_factories_per_level,
            max_factories_per_level,
            min_n_processes,
        )
        n_processes = len(n_f_list)
        n_defaults = [0] * n_processes
        while n_default_managers > 0:
            indx = randint(0, n_processes - 1)
            if n_f_list[indx] <= n_defaults[indx]:
                continue
            n_defaults[indx] += 1
            n_default_managers -= 1

    n_factories = sum(n_f_list)

    if non_competitor_params is None:
        non_competitor_params = [{}] * len(non_competitors)

    non_competitors = [get_full_type_name(_) for _ in non_competitors]

    max_def_agents = len(non_competitors) - 1
    agent_types = [None] * n_factories
    manager_params = [None] * n_factories
    first_in_level = 0
    for level in range(n_processes):
        n_d = n_defaults[level]
        n_f = n_f_list[level]
        assert (
            n_d <= n_f
        ), f"Got {n_f} total factories at level {level} out of which {n_d} are default!!"
        for j in range(n_f):
            if j >= n_f - n_d:  # default managers are last managers in the list
                def_indx = randint(0, max_def_agents)
                agent_types[first_in_level + j] = non_competitors[def_indx]
                params_ = copy.deepcopy(non_competitor_params[def_indx])
                params_["name"] = f"_df_{level}_{j}"
                manager_params[first_in_level + j] = params_
        first_in_level += n_f

    world_name = unique_name("", add_time=True, rand_digits=4)
    agent_types = [
        get_full_type_name(_) if isinstance(_, SCML2020Agent) else _
        for _ in agent_types
    ]
    no_logs = compact
    agent_processes = []
    for i, n in enumerate(n_f_list):
        for j in range(n):
            agent_processes.append(i)
    if oneshot_world:
        world_params = dict(
            name=world_name,
            agent_types=agent_types,
            agent_params=manager_params,
            time_limit=7200 + 3600,
            neg_time_limit=120,
            neg_n_steps=20,
            neg_step_time_limit=10,
            negotiation_speed=21,
            start_negotiations_immediately=False,
            agent_processes=agent_processes,
            n_processes=n_processes,
            n_steps=n_steps,
            n_lines=n_lines,
            compact=compact,
            no_logs=no_logs,
            random_agent_types=False,
        )
    else:
        world_params = dict(
            name=world_name,
            agent_types=agent_types,
            agent_params=manager_params,
            time_limit=7200 + 3600,
            neg_time_limit=120,
            neg_n_steps=20,
            neg_step_time_limit=10,
            negotiation_speed=21,
            spot_market_global_loss=0.2,
            interest_rate=0.08,
            bankruptcy_limit=1.0,
            initial_balance=None,
            start_negotiations_immediately=False,
            agent_processes=agent_processes,
            n_processes=n_processes,
            n_steps=n_steps,
            n_lines=n_lines,
            compact=compact,
            no_logs=no_logs,
            random_agent_types=False,
        )
    world_params.update(kwargs)
    # _agent_types = copy.deepcopy(world_params.pop("agent_types"))
    # _agent_params = copy.deepcopy(world_params.pop("agent_params"))
    if oneshot_world:
        generated_world_params = SCML2020OneShotWorld.generate(**world_params)
    else:
        generated_world_params = SCML2022World.generate(**world_params)
    # world_params["agent_types"] = _agent_types
    # world_params["agent_params"] = _agent_params
    for k in ("agent_types", "agent_params"):
        if k in generated_world_params.keys():
            del generated_world_params[k]
    if oneshot_world:
        for _p in generated_world_params["profiles"]:
            _p.cost = int(_p.cost)
    else:
        for _p in generated_world_params["profiles"]:
            _p.costs = _p.costs.tolist()
    world_params["__exact_params"] = serialize(
        generated_world_params, deep=True, ignore_lambda=True
    )
    config = {
        "world_params": world_params,
        "compact": compact,
        "scoring_context": {},
        "non_competitors": non_competitors,
        "non_competitor_params": non_competitor_params,
        "agent_types": agent_types,
        "agent_params": manager_params,
    }
    config.update(kwargs)
    return [config]


def anac2021_config_generator_collusion(
    n_competitors: int,
    n_agents_per_competitor: int,
    agent_names_reveal_type: bool = False,
    non_competitors: tuple[str | type[SCML2020Agent], ...] | None = None,
    non_competitor_params: tuple[dict[str, Any], ...] | None = None,
    *args,
    **kwargs,
) -> list[dict[str, Any]]:
    assert n_agents_per_competitor > 1
    return anac2020_config_generator(
        n_competitors=n_competitors,
        n_agents_per_competitor=n_agents_per_competitor,
        agent_names_reveal_type=agent_names_reveal_type,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        *args,
        **kwargs,
    )


def anac2020_assigner(
    config: list[dict[str, Any]],
    max_n_worlds: int,
    n_agents_per_competitor: int = 1,
    fair: bool = True,
    competitors: Sequence[type[Agent]] = (),
    params: Sequence[dict[str, Any]] = (),
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
) -> list[list[dict[str, Any]]]:
    tentative = []
    for i, current_config in enumerate(config):
        if i > 0:
            n_agents_per_competitor = 1

        competitors = list(
            get_full_type_name(_) if not isinstance(_, str) and _ is not None else _
            for _ in competitors
        )
        n_competitors = len(competitors)
        params = (
            list(params)
            if params is not None
            else [dict() for _ in range(n_competitors)]
        )

        n_permutations = n_competitors

        agent_types = current_config["agent_types"]
        is_default = [_ is not None for _ in agent_types]
        # assign non-competitor factories to extra-non-competitors
        if dynamic_non_competitors is not None:
            n_extra = len(dynamic_non_competitors)
            dynamic_non_competitors = list(
                get_full_type_name(_) if not isinstance(_, str) and _ is not None else _
                for _ in dynamic_non_competitors
            )
            if dynamic_non_competitor_params is None:
                dynamic_non_competitor_params = [dict() for _ in range(n_extra)]
            # removing the competitors from the dynamic competitors
            if exclude_competitors_from_reassignment:
                # TODO May be use a better way to hash the a parameters than just conversion to str
                # Note that None and and empty dict() will both become ""
                compset = set(zip(competitors, (str(_) if _ else "" for _ in params)))
                dynset = list(
                    zip(
                        dynamic_non_competitors,
                        (str(_) if _ else "" for _ in dynamic_non_competitor_params),
                    )
                )
                dynamic_non_competitor_indices = [
                    i for i, _ in enumerate(dynset) if _ not in compset
                ]
                dynamic_non_competitors = [
                    dynamic_non_competitors[i] for i in dynamic_non_competitor_indices
                ]
                dynamic_non_competitor_params = [
                    dynamic_non_competitor_params[i]
                    for i in dynamic_non_competitor_indices
                ]
                n_extra = len(dynamic_non_competitors)
            if n_extra:
                for i, isd in enumerate(is_default):
                    if not isd:
                        continue
                    extra_indx = randint(0, n_extra - 1)
                    current_config["agent_types"][i] = dynamic_non_competitors[
                        extra_indx
                    ]
                    current_config["agent_params"][i] = dynamic_non_competitor_params[
                        extra_indx
                    ]
        assignable_factories = [
            i for i, mtype in enumerate(agent_types) if mtype is None
        ]
        shuffle(assignable_factories)
        assignable_factories = (
            np.asarray(assignable_factories)
            .reshape((n_competitors, n_agents_per_competitor))
            .tolist()
        )

        current_configs = []

        def _copy_config(perm_, c, indx):
            new_config = copy.deepcopy(c)
            new_config["is_default"] = is_default
            for (a, p_), assignable in zip(perm_, assignable_factories):
                for factory in assignable:
                    new_config["agent_types"][factory] = a
                    new_config["agent_params"][factory] = copy.deepcopy(p_)
            return [new_config]

        if n_permutations is not None and max_n_worlds is None:
            permutation = list(zip(competitors, params))
            assert len(permutation) == len(assignable_factories)
            shuffle(permutation)
            perm = permutation
            for k in range(n_permutations):
                perm = copy.deepcopy(perm)
                perm = perm[-1:] + perm[:-1]
                current_configs.append(_copy_config(perm, current_config, k))
        elif max_n_worlds is None:
            raise ValueError(
                f"Did not give max_n_worlds and cannot find n_permutations."
            )
        else:
            permutation = list(zip(competitors, params))
            assert len(permutation) == len(assignable_factories)
            if fair:
                n_min = len(assignable_factories)
                n_rounds = int(max_n_worlds // n_min)
                if n_rounds < 1:
                    raise ValueError(
                        f"Cannot guarantee fair assignment: n. competitors {len(assignable_factories)}, at least"
                        f" {n_min} runs are needed for fair assignment"
                    )
                max_n_worlds = n_rounds * n_min
                k = 0
                for _ in range(n_rounds):
                    shuffle(permutation)
                    for __ in range(n_min):
                        k += 1
                        perm = copy.deepcopy(permutation)
                        perm = perm[-1:] + perm[:-1]
                        current_configs.append(_copy_config(perm, current_config, k))
            else:
                for k in range(max_n_worlds):
                    perm = copy.deepcopy(permutation)
                    shuffle(perm)
                    current_configs.append(_copy_config(perm, current_config, k))

        tentative.append(current_configs)
    if len(config) == 1:
        return tentative[0]
    assert len({len(_) for _ in tentative}) == 1
    n = len(tentative[0])
    final_configs = []
    for i in range(n):
        lst = [_[i] for _ in tentative]
        final_configs += lst
    return final_configs


def anac2021_assigner_collusion(
    config: list[dict[str, Any]],
    max_n_worlds: int,
    n_agents_per_competitor: int = 1,
    fair: bool = True,
    competitors: Sequence[type[Agent]] = (),
    params: Sequence[dict[str, Any]] = (),
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
) -> list[list[dict[str, Any]]]:
    current_config = config[0]

    competitors = list(
        get_full_type_name(_) if not isinstance(_, str) and _ is not None else _
        for _ in competitors
    )
    n_competitors = len(competitors)
    params = (
        list(params) if params is not None else [dict() for _ in range(n_competitors)]
    )

    n_permutations = n_competitors

    agent_types = current_config["agent_types"]
    is_default = [_ is not None for _ in agent_types]
    # assign non-competitor factories to extra-non-competitors
    if dynamic_non_competitors is not None:
        n_extra = len(dynamic_non_competitors)
        dynamic_non_competitors = list(
            get_full_type_name(_) if not isinstance(_, str) and _ is not None else _
            for _ in dynamic_non_competitors
        )
        if dynamic_non_competitor_params is None:
            dynamic_non_competitor_params = [dict() for _ in range(n_extra)]
        # removing the competitors from the dynamic competitors
        if exclude_competitors_from_reassignment:
            # TODO May be use a better way to hash the a parameters than just conversion to str
            # Note that None and and empty dict() will both become ""
            compset = set(zip(competitors, (str(_) if _ else "" for _ in params)))
            dynset = list(
                zip(
                    dynamic_non_competitors,
                    (str(_) if _ else "" for _ in dynamic_non_competitor_params),
                )
            )
            dynamic_non_competitor_indices = [
                i for i, _ in enumerate(dynset) if _ not in compset
            ]
            dynamic_non_competitors = [
                dynamic_non_competitors[i] for i in dynamic_non_competitor_indices
            ]
            dynamic_non_competitor_params = [
                dynamic_non_competitor_params[i] for i in dynamic_non_competitor_indices
            ]
            n_extra = len(dynamic_non_competitors)
        if n_extra:
            for i, isd in enumerate(is_default):
                if not isd:
                    continue
                extra_indx = randint(0, n_extra - 1)
                current_config["agent_types"][i] = dynamic_non_competitors[extra_indx]
                current_config["agent_params"][i] = dynamic_non_competitor_params[
                    extra_indx
                ]
    assignable_factories = [i for i, mtype in enumerate(agent_types) if mtype is None]
    shuffle(assignable_factories)
    assignable_factories = (
        np.asarray(assignable_factories)
        .reshape((n_competitors, n_agents_per_competitor))
        .tolist()
    )

    current_configs = []

    def _copy_config(perm_, c, indx):
        new_config = copy.deepcopy(c)
        new_config["is_default"] = is_default
        for (a, p_), assignable in zip(perm_, assignable_factories):
            for factory in assignable:
                new_config["agent_types"][factory] = a
                new_config["agent_params"][factory] = copy.deepcopy(p_)
        configs: list[dict] = [
            copy.deepcopy(new_config) for _ in range(n_agents_per_competitor + 1)
        ]

        non_competitor_info = list(
            (a, p if p else dict())
            for a, p, d in zip(
                new_config["agent_types"], new_config["agent_params"], is_default
            )
            if d and a is not None and a not in competitors
        )

        non_competitors = [get_full_type_name(a) for a, _ in non_competitor_info]
        non_competitor_params = [b for _, b in non_competitor_info]
        max_def_agents = len(non_competitors) - 1

        assert len({tuple(_) for _ in assignable_factories}) == 1
        free_factories = assignable_factories[0]

        assert len(free_factories) == n_agents_per_competitor
        # for each config other than the first, remove all unassigned factories keeping one
        for j, config in zip(free_factories, configs[1:]):
            for i in free_factories:
                if i == j:
                    continue
                # assert config["agent_types"][i] is None
                assert not config["is_default"][i]
                def_indx = randint(0, max_def_agents)
                params_ = copy.deepcopy(non_competitor_params[def_indx])
                params_["name"] = f"_df_{100}_{i}"
                config["agent_types"][i] = non_competitors[def_indx]
                config["agent_params"][i] = params_
                config["is_default"][i] = True
                # config["is_default"][i] = False
            assert len([_ for _ in config["is_default"] if not _]) == 1
        return configs

    if n_permutations is not None and max_n_worlds is None:
        permutation = list(zip(competitors, params))
        assert len(permutation) == len(assignable_factories)
        shuffle(permutation)
        perm = permutation
        for k in range(n_permutations):
            perm = copy.deepcopy(perm)
            perm = perm[-1:] + perm[:-1]
            current_configs.append(_copy_config(perm, current_config, k))
    elif max_n_worlds is None:
        raise ValueError(f"Did not give max_n_worlds and cannot find n_permutations.")
    else:
        permutation = list(zip(competitors, params))
        assert len(permutation) == len(assignable_factories)
        if fair:
            n_min = len(assignable_factories)
            n_rounds = int(max_n_worlds // n_min)
            if n_rounds < 1:
                raise ValueError(
                    f"Cannot guarantee fair assignment: n. competitors {len(assignable_factories)}, at least"
                    f" {n_min} runs are needed for fair assignment"
                )
            max_n_worlds = n_rounds * n_min
            k = 0
            for _ in range(n_rounds):
                shuffle(permutation)
                for __ in range(n_min):
                    k += 1
                    perm = copy.deepcopy(permutation)
                    perm = perm[-1:] + perm[:-1]
                    current_configs.append(_copy_config(perm, current_config, k))
        else:
            for k in range(max_n_worlds):
                perm = copy.deepcopy(permutation)
                shuffle(perm)
                current_configs.append(_copy_config(perm, current_config, k))

    return current_configs


def anac2020_world_generator(**kwargs):
    if "n_agents_per_process" in kwargs["world_params"]:
        assert sum(kwargs["world_params"]["n_agents_per_process"]) == len(
            kwargs["world_params"]["agent_types"]
        )
    else:
        assert len(kwargs["world_params"]["agent_processes"]) == len(
            kwargs["world_params"]["agent_types"]
        )
    cnfg = kwargs["world_params"].pop("__exact_params")
    cnfg = deserialize(cnfg)
    kwargs["world_params"]["random_agent_typea"] = False
    cnfg2 = SCML2022World.generate(**kwargs["world_params"])
    for k in ("agent_types", "agent_params"):
        cnfg[k] = cnfg2[k]
    for _p in cnfg["profiles"]:
        _p.costs = np.asarray(_p.costs)
    if "info" not in cnfg.keys():
        cnfg["info"] = dict()
    cnfg["info"]["is_default"] = kwargs["is_default"]
    world = SCML2022World(**cnfg)
    return world


def anac2020oneshot_world_generator(**kwargs):
    if "n_agents_per_process" in kwargs["world_params"]:
        assert sum(kwargs["world_params"]["n_agents_per_process"]) == len(
            kwargs["world_params"]["agent_types"]
        )
    else:
        assert len(kwargs["world_params"]["agent_processes"]) == len(
            kwargs["world_params"]["agent_types"]
        )
    # cnfg = SCML2020OneShotWorld.generate(**kwargs["world_params"])
    # for k in ("n_agents_per_process","n_processes"):
    #     del kwargs["world_params"][k]
    cnfg = kwargs["world_params"].pop("__exact_params")
    cnfg = deserialize(cnfg)
    kwargs["world_params"]["random_agent_typea"] = False
    cnfg2 = SCML2020OneShotWorld.generate(**kwargs["world_params"])
    for k in ("agent_types", "agent_params", "name"):
        cnfg[k] = cnfg2[k]
    if "info" not in cnfg.keys():
        cnfg["info"] = dict()
    cnfg["info"]["is_default"] = kwargs["is_default"]
    world = SCML2020OneShotWorld(**cnfg)
    return world


def balance_calculator2020(
    worlds: list[SCML2020World],
    scoring_context: dict[str, Any],
    dry_run: bool,
    ignore_default=True,
    inventory_catalog_price_weight=0.0,
    inventory_trading_average_weight=0.5,
    consolidated=False,
) -> WorldRunResults:
    """A scoring function that scores factory managers' performance by the final balance only ignoring whatever still
    in their inventory.

    Args:

        worlds: The world which is assumed to be run up to the point at which the scores are to be calculated.
        scoring_context:  A dict of context parameters passed by the world generator or assigner.
        dry_run: A boolean specifying whether this is a dry_run. For dry runs, only names and types are expected in
                 the returned `WorldRunResults`
        ignore_default: Whether to ignore non-competitors (default agents)
        inventory_catalog_price_weight: The weight assigned to catalog price
        inventory_trading_average_weight: The weight assigned to trading price average
        consolidated: If true, the score of an agent type will be based on a consolidated statement of
                     all the factories it controlled

    Returns:
        WorldRunResults giving the names, scores, and types of factory managers.

    """
    if scoring_context is not None:
        inventory_catalog_price_weight = scoring_context.get(
            "inventory_catalog_price_weight", inventory_catalog_price_weight
        )
        inventory_trading_average_weight = scoring_context.get(
            "inventory_trading_average_weight", inventory_trading_average_weight
        )
        consolidated = scoring_context.get("consolidated", consolidated)
    assert len(worlds) == 1
    world = worlds[0]
    if world.inventory_valuation_trading is not None:
        inventory_trading_average_weight = world.inventory_valuation_trading
    if world.inventory_valuation_catalog is not None:
        inventory_catalog_price_weight = world.inventory_valuation_catalog
    result = WorldRunResults(
        world_names=[world.name], log_file_names=[world.log_file_name]
    )
    initial_balances = []
    is_default = world.info["is_default"]
    factories = [_ for _ in world.factories if not is_system_agent(_.agent_id)]
    agents = [
        world.agents[f.agent_id] for f in factories if not is_system_agent(f.agent_id)
    ]
    agent_types = [
        _
        for _ in world.agent_unique_types
        if not _.startswith("system_agent")
        and not _.split(".")[-1].startswith("_System")
    ]
    if len(set(agent_types)) == len(set(world.agent_types)):
        agent_types = [
            _
            for _ in world.agent_types
            if not _.startswith("system_agent")
            and not _.split(".")[-1].startswith("_System")
            and not get_class(_) == StdSysAgent
        ]
    for i, factory in enumerate(factories):
        if is_default[i] and ignore_default:
            continue
        initial_balances.append(factory.initial_balance)
    normalize = all(_ != 0 for _ in initial_balances)
    consolidated_scores = defaultdict(float)
    individual_scores = list()
    initial_sums = defaultdict(float)
    assert len(is_default) == len(agents)
    assert len(agents) == len(factories)
    assert len(factories) == len(agent_types)
    for default, factory, manager, agent_type in zip(
        is_default, factories, agents, agent_types
    ):
        if default and ignore_default:
            continue
        result.names.append(manager.name)
        result.ids.append(manager.id)
        result.types.append(agent_type)
        if dry_run:
            result.scores.append(None)
            continue
        final_balance = factory.current_balance
        if inventory_catalog_price_weight != 0.0:
            final_balance += np.sum(
                inventory_catalog_price_weight
                * factory.current_inventory
                * world.catalog_prices
            )
        if inventory_trading_average_weight != 0.0:
            final_balance += np.sum(
                inventory_trading_average_weight
                * factory.current_inventory
                * world.trading_prices
            )
        profit = final_balance - factory.initial_balance
        individual_scores.append(
            profit / factory.initial_balance if normalize else profit
        )
        consolidated_scores[agent_type] += profit
        initial_sums[agent_type] += factory.initial_balance
    if normalize:
        for k in consolidated_scores.keys():
            consolidated_scores[k] /= initial_sums[k]
    extra = []
    for k, v in consolidated_scores.items():
        extra.append(dict(type=k, score=v))
    result.extra_scores["combined_scores"] = extra
    result.extra_scores["consolidated_scores"] = extra

    if consolidated:
        for indx, type_ in enumerate(result.types):
            result.scores.append(consolidated_scores[type_])
    else:
        result.scores = individual_scores

    return result


def balance_calculator2021oneshot(
    worlds: list[SCML2020World],
    scoring_context: dict[str, Any],
    dry_run: bool,
    ignore_default=True,
    consolidated=True,
    **kwargs,
) -> WorldRunResults:
    """A scoring function that scores factory managers' performance by the final balance only ignoring whatever still
    in their inventory.

    Args:

        worlds: The world which is assumed to be run up to the point at which the scores are to be calculated.
        scoring_context:  A dict of context parameters passed by the world generator or assigner.
        dry_run: A boolean specifying whether this is a dry_run. For dry runs, only names and types are expected in
                 the returned `WorldRunResults`
        ignore_default: Whether to ignore non-competitors (default agents)
        consolidated: If true, the score of an agent type will be based on a consolidated statement of
                     all the factories it controlled

    Returns:
        WorldRunResults giving the names, scores, and types of factory managers.

    """
    if scoring_context is not None:
        consolidated = scoring_context.get("consolidated", consolidated)
    assert len(worlds) == 1
    world = worlds[0]
    result = WorldRunResults(
        world_names=[world.name], log_file_names=[world.log_file_name]
    )
    is_default = world.info["is_default"]
    agents = list(_ for _ in world.agents.values() if _.__class__ != OneShotSysAgent)
    agent_types = [
        _
        for _ in world.agent_unique_types
        if not _.startswith("system_agent") and not _.startswith("System")
    ]
    if len(set(agent_types)) == len(set(world.agent_types)):
        agent_types = [
            _
            for _ in world.agent_types
            if not _.startswith("system_agent") and not _.startswith("System")
        ]
    consolidated_scores = defaultdict(float)
    individual_scores = list()
    scores = world.scores()
    assert len(agents) == len(is_default) and len(agents) == len(agent_types)
    for default, manager, agent_type in zip(is_default, agents, agent_types):
        if default and ignore_default:
            continue
        result.names.append(manager.name)
        result.ids.append(manager.id)
        result.types.append(agent_type)
        if dry_run:
            result.scores.append(None)
            continue
        profit = scores[manager.id]
        individual_scores.append(profit)
        consolidated_scores[agent_type] += profit
    extra = []
    for k, v in consolidated_scores.items():
        extra.append(dict(type=k, score=v))
    result.extra_scores["combined_scores"] = extra
    result.extra_scores["consolidated_scores"] = extra

    if consolidated:
        for indx, type_ in enumerate(result.types):
            result.scores.append(consolidated_scores[type_])
    else:
        result.scores = individual_scores

    return result


def balance_calculator2021(
    worlds: list[SCML2020World],
    scoring_context: dict[str, Any],
    dry_run: bool,
    ignore_default=True,
    inventory_catalog_price_weight=0.0,
    inventory_trading_average_weight=0.5,
) -> WorldRunResults:
    """A scoring function that scores factory managers' performance by the
    final balance only ignoring whatever still in their inventory after
    consolidating all factories in the simulation that belong to the same
    agent type.

    Args:

        worlds: The world which is assumed to be run up to the point at which the scores are to be calculated.
        scoring_context:  A dict of context parameters passed by the world generator or assigner.
        dry_run: A boolean specifying whether this is a dry_run. For dry runs, only names and types are expected in
                 the returned `WorldRunResults`
        ignore_default: Whether to ignore non-competitors (default agents)
        inventory_catalog_price_weight: The weight assigned to catalog price
        inventory_trading_average_weight: The weight assigned to trading price average

    Returns:
        WorldRunResults giving the names, scores, and types of factory managers.

    Remarks:

        - If multiple agents belonged to the same agent_type, the score of
          all of these agents will be set to the same value which is the
          consolidated profit of the group. This means that agent types that
          have more instantiations will tend to have higher scores at the end.
          When using this balance calculator, it is recommended to have the
          same number of instantiations of all agent types in each simulation
          to make sure that scores of different agent types are comparable in
          each and every simulation.

    """
    return balance_calculator2020(
        worlds,
        scoring_context,
        dry_run,
        ignore_default,
        inventory_catalog_price_weight,
        inventory_trading_average_weight,
        consolidated=True,
    )


def balance_calculator2021collusion(
    worlds: list[SCML2020World],
    scoring_context: dict[str, Any],
    dry_run: bool,
    ignore_default=True,
    inventory_catalog_price_weight=0.0,
    inventory_trading_average_weight=0.5,
) -> WorldRunResults:
    """A scoring function that scores factory managers' performance by the
    final balance only ignoring whatever still in their inventory after
    consolidating all factories in the simulation that belong to the same
    agent type.

    Args:

        worlds: The world which is assumed to be run up to the point at which the scores are to be calculated.
        scoring_context:  A dict of context parameters passed by the world generator or assigner.
        dry_run: A boolean specifying whether this is a dry_run. For dry runs, only names and types are expected in
                 the returned `WorldRunResults`
        ignore_default: Whether to ignore non-competitors (default agents)
        inventory_catalog_price_weight: The weight assigned to catalog price
        inventory_trading_average_weight: The weight assigned to trading price average

    Returns:
        WorldRunResults giving the names, scores, and types of factory managers.

    Remarks:

        - If multiple agents belonged to the same agent_type, the score of
          all of these agents will be set to the same value which is the
          consolidated profit of the group. This means that agent types that
          have more instantiations will tend to have higher scores at the end.
          When using this balance calculator, it is recommended to have the
          same number of instantiations of all agent types in each simulation
          to make sure that scores of different agent types are comparable in
          each and every simulation.

    """
    assert len(worlds) > 1
    results_with_collusion = balance_calculator2021(
        [worlds[0]],
        scoring_context,
        dry_run,
        ignore_default,
        inventory_catalog_price_weight,
        inventory_trading_average_weight,
    )
    results_without_collusion = [
        balance_calculator2021(
            [w],
            scoring_context,
            dry_run,
            ignore_default,
            inventory_catalog_price_weight,
            inventory_trading_average_weight,
        )
        for w in worlds[1:]
    ]
    if dry_run:
        return results_with_collusion
    allscores = list(chain(*(_.scores for _ in results_without_collusion)))
    mean_score = sum(allscores) / len(allscores)
    results_with_collusion.scores = [
        _ - mean_score for _ in results_with_collusion.scores
    ]
    # todo: check consolidated scores
    return results_with_collusion


def anac2020_tournament(
    competitors: Sequence[str | type[SCML2020Agent]],
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 2,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (by rotating agents over factories).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, effort will be made to reduce memory footprint including disableing most logs
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    return anac2020_collusion(
        competitors=competitors,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        max_worlds_per_config=max_worlds_per_config,
        n_runs_per_world=n_runs_per_world,
        n_agents_per_competitor=n_agents_per_competitor,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        min_factories_per_level=min_factories_per_level,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        compact=compact,
        configs_only=configs_only,
        non_competitors=None,
        non_competitor_params=None,
        **kwargs,
    )


def anac2020_std(
    competitors: Sequence[str | type[SCML2020Agent]],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (standard track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        n_agents_per_competitor=1,
        world_generator=anac2020_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2020,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric="median",
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        **kwargs,
    )


def anac2020_collusion(
    competitors: Sequence[str | type],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        n_agents_per_competitor=n_agents_per_competitor,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        world_generator=anac2020_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2020,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric="median",
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        **kwargs,
    )


def anac2021_tournament(
    competitors: Sequence[str | type[SCML2020Agent]],
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 2,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (by rotating agents over factories).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, effort will be made to reduce memory footprint including disableing most logs
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    return anac2021_collusion(
        competitors=competitors,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        max_worlds_per_config=max_worlds_per_config,
        n_runs_per_world=n_runs_per_world,
        n_agents_per_competitor=n_agents_per_competitor,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        min_factories_per_level=min_factories_per_level,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        compact=compact,
        configs_only=configs_only,
        non_competitors=None,
        non_competitor_params=None,
        **kwargs,
    )


def anac2021_std(
    competitors: Sequence[str | type[SCML2020Agent]],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (standard track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents2021
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        n_agents_per_competitor=1,
        world_generator=anac2020_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2021,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )


def anac2021_collusion(
    competitors: Sequence[str | type],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = False,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=1,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors. This value will
                                 always be set to 1 in SCML2021
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    n_competitors_per_world = 1
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents2021
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        n_agents_per_competitor=n_agents_per_competitor,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        world_generator=anac2020_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2021,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )


def anac2021_oneshot(
    competitors: Sequence[str | type[SCML2020Agent]],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    min_factories_per_level: int = 4,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = False,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2021 SCML tournament (oneshot track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    # if competitor_params is None:
    #     competitor_params = [dict() for _ in range(len(competitors))]
    # for t, p in zip(competitors, competitor_params):
    #     p["controller_type"] = get_full_type_name(t)
    # competitors = ["scml.oneshot.world.DefaultOneShotAdapter"] * len(competitors)
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgentsOneShot
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    kwargs["oneshot_world"] = True
    kwargs["n_processes"] = 2
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        n_agents_per_competitor=1,
        world_generator=anac2020oneshot_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2021oneshot,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )


def anac2022_tournament(
    competitors: Sequence[str | type[SCML2020Agent]],
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 2,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (by rotating agents over factories).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, effort will be made to reduce memory footprint including disableing most logs
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    return anac2022_std(
        competitors=competitors,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        max_worlds_per_config=max_worlds_per_config,
        n_runs_per_world=n_runs_per_world,
        n_agents_per_competitor=n_agents_per_competitor,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        min_factories_per_level=min_factories_per_level,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        compact=compact,
        configs_only=configs_only,
        non_competitors=None,
        non_competitor_params=None,
        **kwargs,
    )


def anac2022_std(
    competitors: Sequence[str | type[SCML2020Agent]],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = True,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (standard track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents2022
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        n_agents_per_competitor=1,
        world_generator=anac2020_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2021,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )


def anac2022_collusion(
    competitors: Sequence[str | type],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    n_agents_per_competitor: int = 3,
    min_factories_per_level: int = 2,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = False,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=1,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2020 SCML tournament (collusion track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        n_agents_per_competitor: Number of agents per competitor
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors. This value will
                                 always be set to 1 in SCML2022
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    n_competitors_per_world = 1
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgents2022
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        n_agents_per_competitor=n_agents_per_competitor,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        world_generator=anac2020_world_generator,
        config_generator=anac2021_config_generator_collusion,
        config_assigner=anac2021_assigner_collusion,
        score_calculator=balance_calculator2021collusion,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )


def anac2022_oneshot(
    competitors: Sequence[str | type[SCML2020Agent]],
    competitor_params: Sequence[dict[str, Any]] | None = None,
    agent_names_reveal_type=False,
    n_configs: int = 5,
    max_worlds_per_config: int | None = None,
    n_runs_per_world: int = 1,
    min_factories_per_level: int = 4,
    tournament_path: str | None = None,
    total_timeout: int | None = None,
    parallelism="parallel",
    scheduler_ip: str | None = None,
    scheduler_port: str | None = None,
    tournament_progress_callback: Callable[[WorldRunResults | None], None]
    | None = None,
    world_progress_callback: Callable[[SCML2020World | None], None] | None = None,
    non_competitors: Sequence[str | type[SCML2020Agent]] | None = None,
    non_competitor_params: Sequence[str | type[SCML2020Agent]] | None = None,
    dynamic_non_competitors: list[type[Agent]] | None = None,
    dynamic_non_competitor_params: list[dict[str, Any]] | None = None,
    exclude_competitors_from_reassignment: bool = False,
    name: str | None = None,
    verbose: bool = False,
    configs_only=False,
    compact=False,
    n_competitors_per_world=None,
    forced_logs_fraction: float = FORCED_LOGS_FRACTION,
    **kwargs,
) -> TournamentResults | PathLike:
    """
    The function used to run ANAC 2022 SCML tournament (oneshot track).

    Args:

        name: Tournament name
        competitors: A list of class names for the competitors
        competitor_params: A list of competitor parameters (used to initialize the competitors).
        agent_names_reveal_type: If true then the type of an agent should be readable in its name (most likely at its
                                 beginning).
        n_configs: The number of different world configs (up to competitor assignment) to be generated.
        max_worlds_per_config: The maximum number of worlds to run per config. If None, then all possible assignments
                             of competitors within each config will be tried (all permutations).
        n_runs_per_world: Number of runs per world. All of these world runs will have identical competitor assignment
                          and identical world configuration.
        min_factories_per_level: Minimum number of factories for each production level
        total_timeout: Total timeout for the complete process
        tournament_path: Path at which to store all results. A scores.csv file will keep the scores and logs folder will
                         keep detailed logs
        parallelism: Type of parallelism. Can be 'serial' for serial, 'parallel' for parallel and 'distributed' for
                     distributed
        scheduler_port: Port of the dask scheduler if parallelism is dask, dist, or distributed
        scheduler_ip: IP Address of the dask scheduler if parallelism is dask, dist, or distributed
        world_progress_callback: A function to be called after everystep of every world run (only allowed for serial
                                 evaluation and should be used with cautious).
        tournament_progress_callback: A function to be called with `WorldRunResults` after each world finished
                                      processing
        non_competitors: A list of agent types that will not be competing in the sabotage competition but will exist
                         in the world
        non_competitor_params: parameters of non competitor agents
        dynamic_non_competitors: A list of non-competing agents that are assigned to the simulation dynamically during
                                 the creation of the final assignment instead when the configuration is created
        dynamic_non_competitor_params: paramters of dynamic non competitor agents
        exclude_competitors_from_reassignment: If true, competitors are excluded from the dyanamic non-competitors
        verbose: Verbosity
        configs_only: If true, a config file for each
        compact: If true, compact logs will be created and effort will be made to reduce the memory footprint
        n_competitors_per_world: Number of competitors in every simulation. If not given it will be a random number
                                 between 2 and min(2, n), where n is the number of competitors
        forced_logs_fraction: Fraction of simulations for which logs are always saved (including negotiations)
        kwargs: Arguments to pass to the `world_generator` function

    Returns:

        `TournamentResults` The results of the tournament or a `PathLike` giving the location where configs were saved

    Remarks:

        Default parameters will be used in the league with the exception of `parallelism` which may use distributed
        processing

    """
    # if competitor_params is None:
    #     competitor_params = [dict() for _ in range(len(competitors))]
    # for t, p in zip(competitors, competitor_params):
    #     p["controller_type"] = get_full_type_name(t)
    # competitors = ["scml.oneshot.world.DefaultOneShotAdapter"] * len(competitors)
    if n_competitors_per_world is None:
        n_competitors_per_world = kwargs.get(
            "n_competitors_per_world", randint(2, min(4, len(competitors)))
        )
    kwargs.pop("n_competitors_per_world", None)
    if non_competitors is None:
        non_competitors = DefaultAgentsOneShot
        non_competitor_params = [dict() for _ in non_competitors]
    kwargs["round_robin"] = kwargs.get("round_robin", ROUND_ROBIN)
    kwargs["oneshot_world"] = True
    kwargs["n_processes"] = 2
    return tournament(
        competitors=competitors,
        competitor_params=competitor_params,
        non_competitors=non_competitors,
        non_competitor_params=non_competitor_params,
        agent_names_reveal_type=agent_names_reveal_type,
        n_configs=n_configs,
        n_runs_per_world=n_runs_per_world,
        max_worlds_per_config=max_worlds_per_config,
        tournament_path=tournament_path,
        total_timeout=total_timeout,
        parallelism=parallelism,
        scheduler_ip=scheduler_ip,
        scheduler_port=scheduler_port,
        tournament_progress_callback=tournament_progress_callback,
        world_progress_callback=world_progress_callback,
        name=name,
        verbose=verbose,
        configs_only=configs_only,
        n_agents_per_competitor=1,
        world_generator=anac2020oneshot_world_generator,
        config_generator=anac2020_config_generator,
        config_assigner=anac2020_assigner,
        score_calculator=balance_calculator2021oneshot,
        min_factories_per_level=min_factories_per_level,
        compact=compact,
        metric=truncated_mean,
        n_competitors_per_world=n_competitors_per_world,
        dynamic_non_competitors=dynamic_non_competitors,
        dynamic_non_competitor_params=dynamic_non_competitor_params,
        exclude_competitors_from_reassignment=exclude_competitors_from_reassignment,
        save_video_fraction=0.0,
        forced_logs_fraction=forced_logs_fraction,
        publish_exogenous_summary=True,
        publish_trading_prices=True,
        **kwargs,
    )
