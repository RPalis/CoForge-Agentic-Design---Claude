#!/usr/bin/env python3
"""Resolve colour literals against the token set. Shared by audit-system.py and gate-b.py.

WHY THIS EXISTS — correction C-058, and ADR-023.

The rule is "no value outside tokens". The implementation tested for a SPELLING:
a regex matching `#rgb` and `#rrggbb` and nothing else. Two failures followed from
that, in opposite directions, and both were live at once:

  FALSE NEGATIVE. ART-026 v2 inlines 708 literal colour values written as
  `color(srgb r g b)`. The check reported ZERO findings against it, every run, for
  days. Not because the values were on-token — they are — but because the checker
  could not read the notation. A check that reports clean on a form it cannot parse
  is the "check that cannot fail" this repo has now been bitten by five times
  (SR-11).

  FALSE POSITIVE. Thirty-one blockers were raised against files whose colours are
  token values, exactly, character for character. The check flagged them for being
  written as literals rather than as references — but a self-contained artifact that
  opens offline with no build step CANNOT reference a custom property defined in a
  token file at rest. The value has to be in the file. So the rule as implemented
  was unsatisfiable for a whole class of deliverable, and 30 of 31 blockers were
  noise standing in front of the 1 that was real.

WHAT ON-TOKEN MEANS NOW. A literal is on-token when it RESOLVES to a value in
tokens.json. Not when it is written as a reference. `var(--cf-bone)` and `#eeece6`
are both on-token if the token file says bone is #eeece6; `#9a978f` is off-token in
any notation, however it is spelled.

TWO RULES THAT KEEP THIS HONEST:

  1. A notation this module cannot parse is REPORTED, never skipped. That is the
     entire lesson of C-058 and it is the first thing that would be lost by a later
     edit trying to quiet the output. Unknown must never read as clean.
  2. Every off-token literal in a file is returned. The previous check stopped at
     the first hit per file, so a file with 227 literals contributed one finding and
     the count understated the work by two orders of magnitude.

Alpha is compared on the RGB triple only. Opacity is not a colour, and tokens.json
carries both `#8d8d8d` and `#8d8d8d1f` as separate entries of the same colour.
"""
import json
import re

# Keywords that are not colours. Anything here is neither on-token nor off-token.
KEYWORDS = {
    "none", "transparent", "inherit", "initial", "unset", "revert", "currentcolor",
    "canvastext", "canvas", "linktext", "visitedtext", "activetext", "buttonface",
    "buttontext", "buttonborder", "field", "fieldtext", "highlight", "highlighttext",
    "selecteditem", "selecteditemtext", "mark", "marktext", "graytext", "accentcolor",
    "accentcolortext",
}

# The CSS named colours. Present so a named colour resolves like any other notation
# rather than passing unseen — the exact hole C-058 recorded, in a different form.
NAMED = {
    "aliceblue": "f0f8ff", "antiquewhite": "faebd7", "aqua": "00ffff",
    "aquamarine": "7fffd4", "azure": "f0ffff", "beige": "f5f5dc", "bisque": "ffe4c4",
    "black": "000000", "blanchedalmond": "ffebcd", "blue": "0000ff",
    "blueviolet": "8a2be2", "brown": "a52a2a", "burlywood": "deb887",
    "cadetblue": "5f9ea0", "chartreuse": "7fff00", "chocolate": "d2691e",
    "coral": "ff7f50", "cornflowerblue": "6495ed", "cornsilk": "fff8dc",
    "crimson": "dc143c", "cyan": "00ffff", "darkblue": "00008b", "darkcyan": "008b8b",
    "darkgoldenrod": "b8860b", "darkgray": "a9a9a9", "darkgrey": "a9a9a9",
    "darkgreen": "006400", "darkkhaki": "bdb76b", "darkmagenta": "8b008b",
    "darkolivegreen": "556b2f", "darkorange": "ff8c00", "darkorchid": "9932cc",
    "darkred": "8b0000", "darksalmon": "e9967a", "darkseagreen": "8fbc8f",
    "darkslateblue": "483d8b", "darkslategray": "2f4f4f", "darkslategrey": "2f4f4f",
    "darkturquoise": "00ced1", "darkviolet": "9400d3", "deeppink": "ff1493",
    "deepskyblue": "00bfff", "dimgray": "696969", "dimgrey": "696969",
    "dodgerblue": "1e90ff", "firebrick": "b22222", "floralwhite": "fffaf0",
    "forestgreen": "228b22", "fuchsia": "ff00ff", "gainsboro": "dcdcdc",
    "ghostwhite": "f8f8ff", "gold": "ffd700", "goldenrod": "daa520", "gray": "808080",
    "grey": "808080", "green": "008000", "greenyellow": "adff2f",
    "honeydew": "f0fff0", "hotpink": "ff69b4", "indianred": "cd5c5c",
    "indigo": "4b0082", "ivory": "fffff0", "khaki": "f0e68c", "lavender": "e6e6fa",
    "lavenderblush": "fff0f5", "lawngreen": "7cfc00", "lemonchiffon": "fffacd",
    "lightblue": "add8e6", "lightcoral": "f08080", "lightcyan": "e0ffff",
    "lightgoldenrodyellow": "fafad2", "lightgray": "d3d3d3", "lightgrey": "d3d3d3",
    "lightgreen": "90ee90", "lightpink": "ffb6c1", "lightsalmon": "ffa07a",
    "lightseagreen": "20b2aa", "lightskyblue": "87cefa", "lightslategray": "778899",
    "lightslategrey": "778899", "lightsteelblue": "b0c4de", "lightyellow": "ffffe0",
    "lime": "00ff00", "limegreen": "32cd32", "linen": "faf0e6", "magenta": "ff00ff",
    "maroon": "800000", "mediumaquamarine": "66cdaa", "mediumblue": "0000cd",
    "mediumorchid": "ba55d3", "mediumpurple": "9370db", "mediumseagreen": "3cb371",
    "mediumslateblue": "7b68ee", "mediumspringgreen": "00fa9a",
    "mediumturquoise": "48d1cc", "mediumvioletred": "c71585",
    "midnightblue": "191970", "mintcream": "f5fffa", "mistyrose": "ffe4e1",
    "moccasin": "ffe4b5", "navajowhite": "ffdead", "navy": "000080",
    "oldlace": "fdf5e6", "olive": "808000", "olivedrab": "6b8e23", "orange": "ffa500",
    "orangered": "ff4500", "orchid": "da70d6", "palegoldenrod": "eee8aa",
    "palegreen": "98fb98", "paleturquoise": "afeeee", "palevioletred": "db7093",
    "papayawhip": "ffefd5", "peachpuff": "ffdab9", "peru": "cd853f", "pink": "ffc0cb",
    "plum": "dda0dd", "powderblue": "b0e0e6", "purple": "800080",
    "rebeccapurple": "663399", "red": "ff0000", "rosybrown": "bc8f8f",
    "royalblue": "4169e1", "saddlebrown": "8b4513", "salmon": "fa8072",
    "sandybrown": "f4a460", "seagreen": "2e8b57", "seashell": "fff5ee",
    "sienna": "a0522d", "silver": "c0c0c0", "skyblue": "87ceeb",
    "slateblue": "6a5acd", "slategray": "708090", "slategrey": "708090",
    "snow": "fffafa", "springgreen": "00ff7f", "steelblue": "4682b4",
    "tan": "d2b48c", "teal": "008080", "thistle": "d8bfd8", "tomato": "ff6347",
    "turquoise": "40e0d0", "violet": "ee82ee", "wheat": "f5deb3", "white": "ffffff",
    "whitesmoke": "f5f5f5", "yellow": "ffff00", "yellowgreen": "9acd32",
}

# GUARDS, both earned by a false positive this check produced on its first run.
# `&` — HTML numeric entities. &#8217; (right quote), &#9675; (circle) and
#   &#10003; (checkmark) all leave a hex-looking run after the '#'. Without the
#   lookbehind they raised 21 blockers against five real artifacts, every one of
#   them punctuation. Trading a false-negative class for a false-positive class is
#   not a fix.
# `\w` and `#` — an id, a URL fragment or a doubled hash is not a colour.
# LENGTH is restricted to the four valid CSS forms. A 5- or 7-digit run is not a
# colour in any notation, and treating it as a malformed one re-opens the entity
# problem from the other side. A colour written with the wrong digit count renders
# as nothing at all, which is what looking at the artifact is for (SR-5).
_HEX = re.compile(r"(?<![&\w#])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
# CSS Color 4/5 function names. FOUND BY THE 2026-09-09 ATTESTATION, which planted
# lab(), lch(), oklab(), oklch(), device-cmyk() and color-mix() against the first
# version of this module and got ZERO findings — not an "unresolvable" note, nothing.
# That is C-058 exactly, relocated into the module written to close C-058, and it made
# this file's own docstring claim false. Enumerating six more names would relocate it
# again, so the catch-all below closes the CLASS: any unrecognised function in a colour
# position is reported.
_FN = re.compile(
    r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|device-cmyk|color-mix|color)\s*\(", re.I)
# color-mix() is a CONTAINER, not a leaf. Its arguments are themselves colours and are
# already scanned by _HEX and by this pattern wherever they appear, so reporting the
# wrapper would flag `color-mix(in srgb, var(--teal-90) 40%, var(--bone))` — which holds
# no literal at all — while the literals it may contain are caught on their own terms.
_CONTAINER_FN = {"color-mix"}
# Anything else called in a colour-bearing position. REFUTED AND NARROWED by the
# round-2 attestation, 2026-09-09. The first version of this comment claimed the
# catch-all "closes the CLASS". It did not, and the attester proved it by planting:
# `border:`, `box-shadow:`, `outline:` and `text-shadow:` carry colours but do not end
# in the substring "color", so an unrecognised function in any of them produced zero
# findings — C-058's shape, one level down. A custom-property declaration was invisible
# for the same reason.
#
# THE HONEST BOUND, stated because overstating it is what round 2 caught: this reaches a
# function in the value of a property NAMED BELOW, and a colour-bearing property that is
# not on this list is not scanned. That is a list, not a class. It is a longer list than
# it was, and the limit is written down rather than described as coverage.
_COLOUR_PROPS = (
    r"fill|stroke|stop-color|flood-color|lighting-color|color|background|"
    r"background-color|background-image|border-color|border|border-top|border-right|"
    r"border-bottom|border-left|border-top-color|border-right-color|"
    r"border-bottom-color|border-left-color|outline|outline-color|box-shadow|"
    r"text-shadow|text-decoration-color|text-emphasis-color|caret-color|accent-color|"
    r"column-rule|column-rule-color|scrollbar-color|-webkit-text-stroke|"
    r"-webkit-text-stroke-color|--[a-zA-Z0-9-]+")
# Captures the whole DECLARATION VALUE, not the first token after the colon. Round 2
# planted `border:1px solid newfn(1,2,3)`; a first-token match sees `1px` and stops, so
# the colour function three tokens along was invisible. Shorthand properties put the
# colour anywhere in the value, which is the entire reason they were the gap.
_UNKNOWN_FN = re.compile(
    r"(?:" + _COLOUR_PROPS + r")\s*[:=]\s*([^;}\n\"']{0,400})", re.I)
# Inside a container function the property-position trick cannot work — the property
# slot is occupied by the container's own name. Round 2 planted
# `color: color-mix(in srgb, newweirdfn(1,2,3) 50%, blue 50%)` and got nothing. So
# container arguments are scanned for function calls directly.
_ANY_FN = re.compile(r"\b([a-zA-Z][a-zA-Z0-9-]*)\s*\(", re.I)
# Every function this check knows about, colour and not. A custom property may hold
# ANYTHING — `--ease-std: cubic-bezier(...)` is a timing curve — so without the
# non-colour half of this vocabulary, widening the property list to custom properties
# raised 18 blockers against easing functions. Closing a hole by widening, and creating
# a false-positive class doing it, is the same mistake twice in one file; both attempts
# are recorded rather than tidied away.
_KNOWN_FN = {
    # colour
    "rgb", "rgba", "hsl", "hsla", "hwb", "lab", "lch", "oklab", "oklch",
    "device-cmyk", "color-mix", "color", "light-dark",
    # references and arithmetic
    "var", "url", "attr", "calc", "clamp", "min", "max", "env", "counter", "counters",
    # images and gradients
    "linear-gradient", "radial-gradient", "conic-gradient", "image-set", "cross-fade",
    "repeating-linear-gradient", "repeating-radial-gradient", "repeating-conic-gradient",
    "element", "paint", "image", "src", "format", "local",
    # timing — the ones that caused the 18 false positives
    "cubic-bezier", "steps", "linear", "spring",
    # transforms
    "translate", "translatex", "translatey", "translatez", "translate3d",
    "scale", "scalex", "scaley", "scalez", "scale3d", "rotate", "rotatex",
    "rotatey", "rotatez", "rotate3d", "skew", "skewx", "skewy", "matrix",
    "matrix3d", "perspective",
    # filters
    "blur", "brightness", "contrast", "drop-shadow", "grayscale", "hue-rotate",
    "invert", "opacity", "saturate", "sepia",
    # shapes and layout
    "polygon", "circle", "ellipse", "inset", "path", "ray", "rect", "xywh",
    "minmax", "repeat", "fit-content", "symbols", "view", "scroll", "anchor",
}
_NAME = re.compile(
    r"(?:fill|stroke|stop-color|flood-color|lighting-color|color|background|"
    r"background-color|border-color|outline-color|text-decoration-color|"
    r"caret-color)\s*[:=]\s*[\"']?([a-zA-Z]+)\b", re.I)
_NUM = re.compile(r"[-+]?[0-9]*\.?[0-9]+")


def _hsl_to_rgb(h, s, l):
    h = (h % 360) / 360.0
    if s == 0:
        v = int(round(l * 255))
        return (v, v, v)
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    def cvt(t):
        t = t % 1.0
        if t < 1 / 6: v = p + (q - p) * 6 * t
        elif t < 1 / 2: v = q
        elif t < 2 / 3: v = p + (q - p) * (2 / 3 - t) * 6
        else: v = p
        return int(round(v * 255))
    return (cvt(h + 1 / 3), cvt(h), cvt(h - 1 / 3))


def token_rgb(tokens):
    """Every colour in tokens.json, as a set of (r, g, b) triples."""
    out = set()

    def walk(n):
        if isinstance(n, dict):
            for k, v in n.items():
                if k == "hex" and isinstance(v, str):
                    m = _HEX.match(v.strip())
                    if m:
                        rgb = _hex_rgb(m.group(1))
                        if rgb:
                            out.add(rgb)
                else:
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(tokens)
    return out


def _hex_rgb(digits):
    d = digits.lower()
    if len(d) in (3, 4):
        d = "".join(c * 2 for c in d[:3])
    elif len(d) in (6, 8):
        d = d[:6]
    else:
        return None
    return (int(d[0:2], 16), int(d[2:4], 16), int(d[4:6], 16))


def find_colours(text):
    """Yield (literal, rgb_or_None, note) for every colour-ish thing in `text`.

    rgb is None when the notation was recognised as a colour but could NOT be
    resolved. Those are reported, never skipped — C-058.
    """
    seen = []
    for m in _HEX.finditer(text):
        rgb = _hex_rgb(m.group(1))
        seen.append((m.group(0), rgb,
                     None if rgb else "hex value is not 3, 4, 6 or 8 digits"))
    for m in _FN.finditer(text):
        fn = m.group(1).lower()
        depth, i, n = 0, m.end() - 1, len(text)
        while i < n:
            if text[i] == "(": depth += 1
            elif text[i] == ")":
                depth -= 1
                if depth == 0: break
            i += 1
        arg = text[m.end():i]
        lit = text[m.start():i + 1]
        if len(lit) > 90: lit = lit[:87] + "..."
        if fn in _CONTAINER_FN:
            for im in _ANY_FN.finditer(arg):
                inner = im.group(1).lower()
                if inner not in _KNOWN_FN:
                    seen.append((f"{fn}(... {inner}(...) ...)", None,
                                 f"{inner}() inside {fn}() is a colour value this check "
                                 f"has never seen — reported rather than skipped"))
            continue
        if fn in ("hwb", "lab", "lch", "oklab", "oklch", "device-cmyk"):
            seen.append((lit, None,
                         f"{fn}() carries literal colour components in a space this "
                         f"check cannot convert — express it as a token value"))
            continue
        if fn.startswith("rgb"):
            n = [float(x) for x in _NUM.findall(arg)[:3]]
            if len(n) == 3:
                if "%" in arg:
                    n = [x * 255 / 100 for x in n]
                seen.append((lit, tuple(int(round(x)) for x in n), None))
            else:
                seen.append((lit, None, "rgb() did not yield three components"))
        elif fn.startswith("hsl"):
            n = [float(x) for x in _NUM.findall(arg)[:3]]
            if len(n) == 3:
                seen.append((lit, _hsl_to_rgb(n[0], n[1] / 100, n[2] / 100), None))
            else:
                seen.append((lit, None, "hsl() did not yield three components"))
        else:
            space = (arg.strip().split() or [""])[0].lower()
            n = [float(x) for x in _NUM.findall(arg)[:3]]
            if space == "srgb" and len(n) == 3:
                seen.append((lit, tuple(int(round(x * 255)) for x in n), None))
            else:
                # An unrecognised colour space is REPORTED. Silently ignoring one
                # is how 708 values passed unexamined for days.
                seen.append((lit, None,
                             f"colour space {space!r} is not one this check can resolve"))
    for m in _UNKNOWN_FN.finditer(text):
        for im in _ANY_FN.finditer(m.group(1)):
            fn = im.group(1).lower()
            if fn not in _KNOWN_FN:
                seen.append((m.group(0).strip()[:80], None,
                             f"{fn}() sits in a colour-bearing declaration and is a "
                             f"notation this check has never seen — reported rather "
                             f"than skipped, because passing unread is how C-058 "
                             f"happened"))
    for m in _NAME.finditer(text):
        name = m.group(1).lower()
        if name in KEYWORDS or name in ("var", "url", "rgb", "rgba", "hsl", "hsla",
                                        "color", "linear", "radial", "conic"):
            continue
        if name in NAMED:
            seen.append((name, _hex_rgb(NAMED[name]), None))
    return seen


def off_token(text, tokenset):
    """Every colour literal in `text` that does not resolve to a token value."""
    bad = []
    for lit, rgb, note in find_colours(text):
        if rgb is None:
            bad.append((lit, note))
        elif rgb not in tokenset:
            bad.append((lit, "#%02x%02x%02x is not a value in tokens.json" % rgb))
    return bad


def load_tokenset(path="design-system/tokens/tokens.json"):
    with open(path, encoding="utf-8") as fh:
        return token_rgb(json.load(fh))
