"""Convert the Marshal spec sheet (MS_Spec.xlsx) into assets/js/specs.js.

Usage: python3 build/specs.py path/to/MS_Spec.xlsx
Writes window.MT_SPECS = { MF41: [...], ML41: [...], MH41: [...], MU41: [...] }, one row per size,
in the same shape the size accordion in assets/js/main.js reads.
"""
import json, pathlib, sys
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
ws = openpyxl.load_workbook(sys.argv[1], data_only=True).worksheets[0]
head = [str(h or '').strip() for h in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
col = lambda name: head.index(name)

def num(v, nd=1):
    try: return round(float(v), nd)
    except (TypeError, ValueError): return v

out = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    line = r[col('PTTN')]
    if not line: continue
    out.setdefault(line, []).append({
        'code': r[col('Code')], 'size': str(r[col('Tire Size')]).strip(), 'svc': str(r[col('Service Desc.')]).strip(),
        'cons': r[col('Construction')], 'side': r[col('Sidewall')], 'utqg': r[col('UTQG')], 'rim': r[col('Rim Width Range (in.)')],
        'secw': r[col('Section Width on Measured Rim Width')], 'od': num(r[col('Overall Diameter')]), 'wt': num(r[col('Tire Weight(lb)')]),
        'slr': str(r[col('Static Loaded Radius')]), 'rpm': round(float(r[col('RPM')])), 'tread': num(r[col('Tread Depth (1/32")')]),
        'ls': r[col('Max Load Single')], 'ld': r[col('Max Load Double')] or '', 'psi': r[col('Max Inflation (psi)')],
        'upc': str(r[col('UPC')]), 'war': r[col('Mileage Warranty')], 'pmsf': r[col('3PMS')] == '3PMSF',
        'segment': r[col('Segment')],
    })

js = '/* Marshal tire sizes for every line, generated from MS_Spec.xlsx by build/specs.py. */\nwindow.MT_SPECS = ' + json.dumps(out, separators=(',', ':')) + ';\nwindow.MF41 = window.MT_SPECS.MF41;\n'
(ROOT / 'assets/js/specs.js').write_text(js)
for k, v in out.items():
    rims = sorted({int(''.join(c for c in s['size'].split('R')[-1][:2] if c.isdigit())) for s in v})
    print(k, len(v), 'sizes', f'{rims[0]}-{rims[-1]}"', 'warranty', sorted({s["war"] for s in v}), v[0]['segment'])
