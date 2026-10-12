import re, sys
def sub(pat, rep, s, n, flags=re.S, name=''):
    new, c = re.subn(pat, rep, s, flags=flags)
    if c != n: raise SystemExit(f'{name}: expected {n}, got {c}')
    return new
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    # 1. pricing section
    m = re.search(r'\n[ \t]*<!-- =+ PRICING =+ -->\s*<section class="pricing" id="pricing">(.*?)</section>[ \t]*\n', s, re.S)
    assert m and '<section' not in m.group(1), f
    s = s[:m.start()] + '\n' + s[m.end():]
    # 2. nav/footer links
    s = sub(r'[ \t]*<li><a href="#pricing">[^<]*</a></li>\n', '', s, 2, name='links')
    # 3. pricing CSS
    s = sub(r'[ \t]*/\* =+\s*\n\s*\* Pricing\s*\n\s*\* =+ \*/\n.*?(?=[ \t]*/\* =+\s*\n\s*\* About)', '', s, 1, name='pricing css')
    s = sub(r'\n\n[ \t]*\.price-row \{[^}]*\}', '', s, 1, name='price-row mq')
    s = sub(r'\n\n[ \t]*\.price strong \{[^}]*\}', '', s, 1, name='price strong mq')
    # 4. reveal CSS
    s = sub(r'[ \t]*/\* =+\s*\n\s*\* Reveal / zoom animations\s*\n\s*\* =+ \*/\n.*?(?=[ \t]*/\* =+\s*\n\s*\* Feature icons)', '', s, 1, name='reveal css')
    s = sub(r'\n\n[ \t]*\.hero-app-preview,\s*\.hero-app-preview\.is-visible,\s*\.reveal \{[^}]*\}', '', s, 1, name='reduced motion')
    # 5. markup
    s = re.sub(r' class="reveal"', '', s)
    s = re.sub(r'(class="[^"]*?) reveal"', r'\1"', s)
    s = re.sub(r' style="transition-delay:\d+ms"', '', s)
    # 6. JS observer
    s = sub(r'[ \t]*/\*(?:(?!\*/).)*?\*/\s*\(function \(\) \{\s*const targets =\s*document\.querySelectorAll\(\'\.hero-app-preview, \.reveal\'\);.*?targets\.forEach\(function \(target\) \{\s*observer\.observe\(target\);\s*\}\);\s*\}\)\(\);\n\n?', '', s, 1, name='js')
    for bad in ['reveal', 'is-visible', 'pricing', 'price-row', 'transition-delay', '95 €']:
        if bad in s: print(f, 'still contains', bad)
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', f)
