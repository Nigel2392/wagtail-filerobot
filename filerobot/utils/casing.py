"""
    Code taken from humps.
    https://github.com/nficano/humps/blob/master/humps/main.py

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to <http://unlicense.org/>
"""

import re

from collections.abc import Mapping  # pylint: disable-msg=E0611

ACRONYM_RE = re.compile(r"([A-Z\d]+)(?=[A-Z\d]|$)")
SPLIT_RE = re.compile(r"([\-_]*(?<=[^0-9])(?=[A-Z])[^A-Z]*[\-_]*)")
UNDERSCORE_RE = re.compile(r"(?<=[^\-_])[\-_]+[^\-_]")


def camelize(str_or_iter):
    """
    Convert a string, dict, or list of dicts to camel case.

    :param str_or_iter:
        A string or iterable.
    :type str_or_iter: Union[list, dict, str]
    :rtype: Union[list, dict, str]
    :returns:
        camelized string, dictionary, or list of dictionaries.
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, camelize)

    s = _is_none(str_or_iter)
    if s.isupper() or s.isnumeric():
        return str_or_iter

    if len(s) != 0 and not s[:2].isupper():
        s = s[0].lower() + s[1:]

    # For string "hello_world", match will contain
    #             the regex capture group for "_w".
    return UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)


def decamelize(str_or_iter):
    """
    Convert a string, dict, or list of dicts to snake case.

    :param str_or_iter:
        A string or iterable.
    :type str_or_iter: Union[list, dict, str]
    :rtype: Union[list, dict, str]
    :returns:
        snake cased string, dictionary, or list of dictionaries.
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, decamelize)

    s = _is_none(str_or_iter)
    if s.isupper() or s.isnumeric():
        return str_or_iter

    return _separate_words(_fix_abbreviations(s)).lower()


def _is_none(_in):
    """
    Determine if the input is None
    and returns a string with white-space removed
    :param _in: input
    :return:
        an empty sting if _in is None,
        else the input is returned with white-space removed
    """
    return "" if _in is None else re.sub(r"\s+", "", str(_in))


def _process_keys(str_or_iter, fn):
    if isinstance(str_or_iter, list):
        return [_process_keys(k, fn) for k in str_or_iter]
    if isinstance(str_or_iter, Mapping):
        return {fn(k): _process_keys(v, fn) for k, v in str_or_iter.items()}
    return str_or_iter


def _fix_abbreviations(string):
    """
    Rewrite incorrectly cased acronyms, initialisms, and abbreviations,
    allowing them to be decamelized correctly. For example, given the string
    "APIResponse", this function is responsible for ensuring the output is
    "api_response" instead of "a_p_i_response".

    :param string: A string that may contain an incorrectly cased abbreviation.
    :type string: str
    :rtype: str
    :returns:
        A rewritten string that is safe for decamelization.
    """
    return ACRONYM_RE.sub(lambda m: m.group(0).title(), string)


def _separate_words(string, separator="_"):
    """
    Split words that are separated by case differentiation.
    :param string: Original string.
    :param separator: String by which the individual
        words will be put back together.
    :returns:
        New string.
    """
    return separator.join(s for s in SPLIT_RE.split(string) if s)
