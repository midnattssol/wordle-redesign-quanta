#!/usr/bin/env python3.10
"""The Wordle redesign for the Quanta Magazine article below.

https://www.quantamagazine.org/how-to-win-at-wordle-without-cheating-20221025/
"""
import functools as ft
import itertools as it
import operator as op
import random
import typing as t


def random_empty(start: int, stop: int, mask: int, n_excluded) -> int:
    """Generate a random index corresponding to an index in mask containing a 0."""
    base_num = random.randrange(start, stop - n_excluded)

    for i in it.count():
        if mask & (1 << i):
            continue
        if not base_num:
            return i
        base_num -= 1

    raise NotImplementedError()  # Should be unreachable


def shuffle_min_dist(previous_sequence: t.List[int], min_dist=10):
    """Shuffle a sequence of unique elements.

    Provided the sentence is unique, this maintains that the minimum
    distance between equal elements is at the most `min_dist` after
    concatenating the two sequences.
    """
    previous_sequence = list(previous_sequence)
    n_items = len(previous_sequence)

    if min_dist > n_items:
        raise ValueError(
            f"The minimum distance is {min_dist},"
            f" but the number of items is {n_items}, so the shuffle is impossible."
        )

    # Store the elements together with the previous location where they can be placed.
    earliest_allowed_locations = [
        (max(0, i + min_dist - n_items), k) for i, k in enumerate(previous_sequence)
    ][::-1]

    # Add the items with limited placement options first,
    # selecting a random location for each element to be placed
    # from from the free locations in the iterable.
    new_sequence = list(it.repeat(None, n_items))
    n_excluded = 0
    arr = 0

    for index, item in earliest_allowed_locations:
        location = random_empty(index, n_items, arr, n_excluded)
        arr |= 1 << location
        new_sequence[location] = item
        n_excluded += 1

    return new_sequence


def partial_shuffle(items: list, fraction: float = 0.1) -> list:
    """Perform a partial shuffle of the items."""
    num_items = len(items)

    for index in range(num_items):
        if random.random() < fraction / 2:
            new_index = random.randrange(0, num_items)
            items[index], items[new_index] = items[new_index], items[index]

    return items


def main() -> None:
    """Shuffle Wordle indices as a proof of concept.

    Does a shuffle preserving minimum distance, then shuffles the list
    lightly, and removes some random items.
    """
    random.seed("I <3 Quanta")

    first_indices = list(range(2_309))
    min_days_until_repeat = 366
    num_repeats = 5
    random.shuffle(first_indices)
    wordle_indices = [first_indices]

    for _ in range(num_repeats - 1):
        wordle_indices.append(
            shuffle_min_dist(wordle_indices[-1], min_days_until_repeat)
        )

    # Concatenate, partially shuffle, and remove random items from the sequences.
    wordle_indices = ft.reduce(op.add, wordle_indices)
    wordle_indices = partial_shuffle(wordle_indices, 0.15)
    wordle_indices = list(filter(lambda x: random.random() > 0.05, wordle_indices))

    print(len(wordle_indices))


if __name__ == "__main__":
    main()
