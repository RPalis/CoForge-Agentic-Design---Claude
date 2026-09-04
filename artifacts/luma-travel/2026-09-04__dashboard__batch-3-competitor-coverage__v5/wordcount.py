import sys, re
from html.parser import HTMLParser

class Counter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.skip_depth = 0   # inside <style>/<script>
        self.hidden_stack = []  # stack of bool: currently inside a hidden (collapsed details) region
        self.style_tag = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("style", "script"):
            self.style_tag = True
        if tag == "details":
            # hidden by default unless 'open' attribute present
            self.hidden_stack.append("open" not in attrs)
        if tag in ("summary",):
            pass  # summary text IS visible even when details is closed

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.style_tag = False
        if tag == "details":
            if self.hidden_stack:
                self.hidden_stack.pop()

    def handle_data(self, data):
        if self.style_tag:
            return
        # if we're inside a closed <details>'s BODY (not its summary), skip.
        # Approximate: if any ancestor details is hidden AND we are not currently
        # inside that details' own <summary>, skip. Since HTMLParser is not a tree,
        # track via a simpler heuristic below (handled in run()).
        self.text.append(data)

def main(path):
    html = open(path, encoding="utf-8").read()
    # Strip <style>...</style> and <script>...</script> blocks entirely first.
    html_nostyle = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S)
    html_nostyle = re.sub(r"<script[^>]*>.*?</script>", "", html_nostyle, flags=re.S)

    # ALL text present in the DOM regardless of visibility (includes collapsed <details> bodies)
    class Plain(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.text = []
        def handle_data(self, data):
            self.text.append(data)
    p = Plain()
    p.feed(html_nostyle)
    all_text = " ".join(p.text)
    all_words = len(all_text.split())

    # VISIBLE-only text: remove the body of every <details> that lacks the 'open'
    # attribute (summary text is kept because <summary> renders even when closed).
    # A details.note or details.meta with no `open` attribute is closed by default
    # in every browser; this file sets none of them open.
    def strip_closed_details_bodies(s):
        out = []
        i = 0
        while True:
            m = re.search(r"<details\b([^>]*)>", s[i:], flags=re.S)
            if not m:
                out.append(s[i:])
                break
            start = i + m.start()
            tag_end = i + m.end()
            out.append(s[i:start])
            is_open = "open" in m.group(1)
            # find matching </details> (no nested <details> in this file, checked separately)
            close = re.search(r"</details>", s[tag_end:], flags=re.S)
            if not close:
                out.append(s[tag_end:])
                break
            inner_end = tag_end + close.start()
            full_close_end = tag_end + close.end()
            inner = s[tag_end:inner_end]
            if is_open:
                out.append(inner)
            else:
                # keep only the <summary>...</summary> inside inner
                sm = re.search(r"<summary\b[^>]*>.*?</summary>", inner, flags=re.S)
                out.append(sm.group(0) if sm else "")
            i = full_close_end
        return "".join(out)

    visible_html = strip_closed_details_bodies(html_nostyle)
    pv = Plain()
    pv.feed(visible_html)
    visible_text = " ".join(pv.text)
    visible_words = len(visible_text.split())

    print(f"all-DOM words (incl. collapsed <details>):  {all_words}")
    print(f"visible words (closed-details bodies excluded): {visible_words}")
    nested = len(re.findall(r"<details\b[^>]*>\s*(?:(?!</details>).)*<details\b", html_nostyle, flags=re.S))
    print(f"nested <details> found (would break the stripper): {nested}")

if __name__ == "__main__":
    main(sys.argv[1])
