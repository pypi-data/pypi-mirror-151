import re
from copy import deepcopy
from numbers import Number
from random import uniform
from typing import Dict
from typing import List
from typing import Union

import sonusai
from sonusai import SonusAIError


def get_augmentations(rules: Union[List[Dict], Dict], target: bool = False) -> List[dict]:
    """Generate augmentations from list of input rules."""
    augmentations = list()
    if not isinstance(rules, list):
        rules = [rules]

    for in_rule in rules:
        expand_rules(augmentations, in_rule, target)

    augmentations = rand_rules(augmentations)
    return augmentations


def expand_rules(out_rules: List[dict], in_rule: dict, target: bool) -> None:
    """Expand rules."""
    # replace old 'eq' rule with new 'eq1' rule to allow both for backward compatibility
    in_rule = {'eq1' if key == 'eq' else key: value for key, value in in_rule.items()}

    for key in in_rule:
        if key not in sonusai.mixture.VALID_AUGMENTATIONS:
            raise SonusAIError(f'Invalid augmentation: {key}')

        if key in ['eq1', 'eq2', 'eq3']:
            # eq must be a list of length 3 or a list of length 3 lists
            valid = True
            multiple = False
            if isinstance(in_rule[key], list):
                if any(isinstance(el, list) for el in in_rule[key]):
                    multiple = True
                    for value in in_rule[key]:
                        if not isinstance(value, list) or len(value) != 3:
                            valid = False
                else:
                    if len(in_rule[key]) != 3:
                        valid = False
            else:
                valid = False

            if not valid:
                raise SonusAIError(f'Invalid augmentation value for {key}: {in_rule[key]}')

            if multiple:
                for value in in_rule[key]:
                    expanded_rule = deepcopy(in_rule)
                    expanded_rule[key] = deepcopy(value)
                    expand_rules(out_rules, expanded_rule, target)
                return

        elif key == 'count':
            pass

        else:
            if isinstance(in_rule[key], list):
                for value in in_rule[key]:
                    if isinstance(value, list):
                        raise SonusAIError(f'Invalid augmentation value for {key}: {in_rule[key]}')
                    expanded_rule = deepcopy(in_rule)
                    expanded_rule[key] = deepcopy(value)
                    expand_rules(out_rules, expanded_rule, target)
                return
            elif not isinstance(in_rule[key], Number):
                if not in_rule[key].startswith('rand'):
                    raise SonusAIError(f'Invalid augmentation value for {key}: {in_rule[key]}')

    out_rules.append(in_rule)


def rand_rules(in_rules: List[dict]) -> List[dict]:
    """Randomize rules."""
    out_rules = list()
    for in_rule in in_rules:
        if rule_has_rand(in_rule):
            count = 1
            if 'count' in in_rule and in_rule['count'] is not None:
                count = in_rule['count']
                del in_rule['count']
            for i in range(count):
                out_rules.append(generate_random_rule(in_rule))
        else:
            out_rules.append(in_rule)
    return out_rules


def generate_random_rule(in_rule: dict) -> dict:
    """Generate a new rule from a rule that contains 'rand' directives."""

    def rand_repl(m):
        return f'{uniform(float(m.group(1)), float(m.group(4))):.2f}'

    out_rule = deepcopy(in_rule)
    for key in out_rule:
        out_rule[key] = eval(re.sub(sonusai.mixture.RAND_PATTERN, rand_repl, str(out_rule[key])))

        # convert eq values from strings to numbers
        if key in ['eq1', 'eq2', 'eq3']:
            for n in range(3):
                if isinstance(out_rule[key][n], str):
                    out_rule[key][n] = eval(out_rule[key][n])

    return out_rule


def rule_has_rand(rule: dict) -> bool:
    """Determine if any keys in the given rule contain 'rand'?"""
    for key in rule:
        if 'rand' in str(rule[key]):
            return True

    return False
