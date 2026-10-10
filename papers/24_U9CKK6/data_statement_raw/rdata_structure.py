# Read-only structural scan of an .Rdata (XDR, gzip) file: object names, data.frame column types and lengths.
# Streams the file; does not load it into memory and does not run any analysis.
import gzip, struct, sys, json

REFS = []
import bz2, lzma
class S:
    def __init__(s, path):
        m = open(path,'rb').read(3)
        s.f = gzip.open(path,'rb') if m[:2]==b'\x1f\x8b' else (bz2.open(path,'rb') if m==b'BZh' else lzma.open(path,'rb')); s.buf = b''; s.pos = 0
    def read(s, n):
        while len(s.buf) - s.pos < n:
            c = s.f.read(1 << 22)
            if not c: raise EOFError
            s.buf = s.buf[s.pos:] + c; s.pos = 0
        r = s.buf[s.pos:s.pos+n]; s.pos += n; return r
    def i(s): return struct.unpack('>i', s.read(4))[0]
    def skip(s, n):
        while n > 0:
            k = min(n, 1 << 22); s.read(k); n -= k

def item(s, depth=0, info=None):
    fl = s.i() & 0xFFFFFFFF
    t = fl & 0xFF; hasattr = fl & 0x200; hastag = fl & 0x400
    if t == 254 or t == 242 or t == 253 or t == 251 or t == 252: return ('NIL',)
    if t == 255:
        k = fl >> 8
        if k == 0: k = s.i()
        return REFS[k-1]
    if t == 1:  # SYMSXP
        c = item(s); r = ('SYM', c[1] if c[0]=='CHAR' else None); REFS.append(r); return r
    if t == 9:
        L = s.i()
        if L == -1: return ('CHAR', None)
        return ('CHAR', s.read(L).decode('latin-1'))
    if t in (2, 6, 4, 17, 5):  # LISTSXP, LANGSXP, ENVSXP?, DOTSXP, PROMSXP
        if t == 4:
            REFS.append(('ENV',)); s.i(); item(s); item(s); item(s); item(s); return ('ENV',)
        attr = item(s) if hasattr else None
        tag = item(s)[1] if hastag else None
        car = item(s, depth+1)
        cdr = item(s, depth+1)
        return ('LIST', tag, car, cdr, attr)
    if t == 238:  # ALTREP
        inf = item(s); st = item(s); at = item(s); return ('ALTREP', inf, st, at)
    if t in (10, 13, 14, 15, 16, 19, 20, 24):
        n = s.i()
        if n == -1: n = (s.i() << 32) + s.i()
        res = {'type': {10:'logical',13:'integer',14:'double',15:'complex',16:'character',19:'list',20:'expression',24:'raw'}[t], 'n': n}
        if t == 10 or t == 13: s.skip(4*n)
        elif t == 14: s.skip(8*n)
        elif t == 15: s.skip(16*n)
        elif t == 24: s.skip(n)
        elif t == 16:
            na = 0
            for _ in range(n):
                s.i(); L = s.i()
                if L == -1: na += 1
                else: s.skip(L)
            res['na'] = na
        elif t in (19, 20):
            res['elements'] = [item(s, depth+1) for _ in range(n)]
        if hasattr: res['attr'] = item(s, depth+1)
        return ('VEC', res)
    if t in (3, 25):  # closure, S4
        if hasattr: item(s)
        if t == 3:
            item(s); item(s); item(s)
        return ('OTHER', t)
    raise ValueError('unhandled type %d' % t)

def attrs(a):
    out = {}
    while a and a[0] == 'LIST':
        out[a[1]] = a[2]; a = a[3]
    return out

def strvals(x):
    return x

path = sys.argv[1]
s = S(path)
assert s.read(5) in (b'RDX3\n', b'RDX2\n')
assert s.read(2) == b'X\n'
ver = s.i(); s.i(); s.i()
if ver == 3: s.read(s.i())
top = item(s)
report = {}
o = top
while o and o[0] == 'LIST':
    name, val = o[1], o[2]
    entry = {}
    if val[0] == 'VEC':
        v = val[1]; entry['type'] = v['type']; entry['n'] = v['n']
        at = attrs(v.get('attr'))
        entry['attributes'] = list(at.keys())
        if 'class' in at: entry['class'] = at['class'][0]
        if v['type'] == 'list' and 'names' in at:
            # names vector: we skipped string contents, so re-derive not possible; record column types in order
            cols = []
            for el in v['elements']:
                if el[0] == 'VEC':
                    ea = attrs(el[1].get('attr'))
                    cols.append({'type': el[1]['type'], 'n': el[1]['n'], 'attr': list(ea.keys()), 'na': el[1].get('na')})
                else:
                    cols.append({'kind': el[0]})
            entry['columns'] = cols
    report[name] = entry
    o = o[3]
json.dump(report, open(sys.argv[2], 'w'), indent=1)
print('objects:', list(report.keys()))
