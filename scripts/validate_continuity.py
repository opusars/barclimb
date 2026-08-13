#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
 'RECOVERY_START_HERE.md','AGENTS.md','docs/specs/SPEC_MANIFEST.json',
 'docs/project/PROJECT_STATE.json','docs/project/PROJECT_HANDOFF.md','docs/project/BUILD_HISTORY.md',
 'docs/project/DECISION_LOG.md','docs/project/TEST_LEDGER.md','docs/project/PROVIDER_STATUS.md',
 'docs/project/CLIENT_PARITY.md','docs/project/RECOVERY_PLAYBOOK.md','docs/project/RELEASE_NOTES.md'
]
for rel in required:
 p=ROOT/rel
 if not p.exists() or p.stat().st_size==0: errors.append(f'missing/empty: {rel}')
try:
 m=json.loads((ROOT/'docs/specs/SPEC_MANIFEST.json').read_text())
 for spec in m.get('specifications',[]):
  p=ROOT/'docs/specs'/spec['filename']
  if not p.exists(): errors.append(f'missing spec: {spec["filename"]}'); continue
  got=hashlib.sha256(p.read_bytes()).hexdigest()
  if got!=spec['sha256']: errors.append(f'spec digest mismatch: {spec["filename"]}')
except Exception as e: errors.append(f'manifest error: {e}')
try:
 s=json.loads((ROOT/'docs/project/PROJECT_STATE.json').read_text())
 for k in ['schema_version','project','product_phase','active_launch_train','active_milestone','status','exact_next_task','last_verified_at']:
  if k not in s or s[k] in ['',None]: errors.append(f'PROJECT_STATE missing: {k}')
 if not isinstance(s.get('active_milestone'),int) or not 1<=s.get('active_milestone',0)<=10: errors.append('active_milestone must be 1..10')
except Exception as e: errors.append(f'PROJECT_STATE error: {e}')
handoff=(ROOT/'docs/project/PROJECT_HANDOFF.md').read_text() if (ROOT/'docs/project/PROJECT_HANDOFF.md').exists() else ''
if '## Exact next task' not in handoff: errors.append('PROJECT_HANDOFF lacks Exact next task section')
for marker in ['TODO-HANDOFF','UNKNOWN-CRITICAL']:
 for rel in required:
  p=ROOT/rel
  if p.exists() and marker in p.read_text(errors='ignore'): errors.append(f'unresolved marker {marker} in {rel}')
if errors:
 print('CONTINUITY VALIDATION FAILED')
 for e in errors: print('-',e)
 sys.exit(1)
print('CONTINUITY VALIDATION PASSED')
print('Authoritative specs and recovery package are structurally intact.')
