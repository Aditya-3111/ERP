"""The React forms and tables must match the Django API exactly.

Reads every  frontend/src/modules/<module>/resources.js  (through Node) and checks, for every table:
  * each form field exists in the API and is writable
  * each REQUIRED API field is present in the form (otherwise nobody could save)
  * drop-down choices are values the API accepts
  * each table column exists in the API reply
  * each drop-down list ("lookup") points to an existing endpoint and existing fields
Skipped automatically when Node.js is not installed.
"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from tests.base import BaseAPITest

FRONTEND = Path(__file__).resolve().parents[2] / 'frontend' / 'src'
NODE = shutil.which('node')


def node_json(script):
    out = subprocess.run([NODE, '--input-type=module', '-e', script], capture_output=True, text=True, timeout=60)
    if out.returncode:
        raise AssertionError(out.stderr)
    return json.loads(out.stdout)


@unittest.skipUnless(NODE and FRONTEND.exists(), 'Node.js or the frontend folder is not available')
class FrontendContractTests(BaseAPITest):
    def load_resources(self):
        resources = []
        for path in sorted((FRONTEND / 'modules').glob('*/resources.js')):
            url = path.as_uri()
            data = node_json(f"import('{url}').then(m => console.log(JSON.stringify(m.resources)))")
            resources += [dict(r, module=path.parent.name) for r in data]
        return resources

    def options(self, endpoint):
        resp = self.client.options('/api' + endpoint)
        self.assertEqual(resp.status_code, 200, endpoint)
        return resp.json().get('actions', {}).get('POST', {})

    def test_every_resource_matches_its_api(self):
        lookups = node_json(f"import('{(FRONTEND / 'api' / 'lookups.js').as_uri()}').then(m => console.log(JSON.stringify(m.LOOKUPS)))")
        resources = self.load_resources()
        self.assertGreater(len(resources), 50)
        problems = []
        for r in resources:
            api = self.options(r['endpoint'])
            fields = r['fields'] if 'fields' in r else [f for s in r['sections'] for f in s['fields']]
            names = {f['name'] for f in fields}
            for f in fields:
                spec = api.get(f['name'])
                if spec is None:
                    problems.append(f"{r['endpoint']}: form field '{f['name']}' is not in the API")
                    continue
                if spec.get('read_only'):
                    problems.append(f"{r['endpoint']}: form field '{f['name']}' is read-only in the API")
                if f['type'] == 'select':
                    allowed = {c['value'] for c in spec.get('choices', [])}
                    extra = set(f['options']) - allowed
                    if extra:
                        problems.append(f"{r['endpoint']}.{f['name']}: choices {extra} not accepted by the API")
                if f['type'] == 'relation' and f['lookup'] not in lookups:
                    problems.append(f"{r['endpoint']}.{f['name']}: unknown lookup '{f['lookup']}'")
            for name, spec in api.items():
                if spec.get('required') and not spec.get('read_only') and name not in names:
                    problems.append(f"{r['endpoint']}: required API field '{name}' is missing in the form")
            for c in r['columns']:
                if c['key'] not in api:
                    problems.append(f"{r['endpoint']}: column '{c['key']}' is not in the API reply")
        self.assertEqual(problems, [], '\n' + '\n'.join(problems))

    def test_lookups_point_to_real_endpoints_and_fields(self):
        lookups = node_json(f"import('{(FRONTEND / 'api' / 'lookups.js').as_uri()}').then(m => console.log(JSON.stringify(m.LOOKUPS)))")
        problems = []
        for name, cfg in lookups.items():
            resp = self.client.get('/api' + cfg['endpoint'], {'page_size': 1})
            if resp.status_code != 200:
                problems.append(f"{name}: {cfg['endpoint']} -> HTTP {resp.status_code}")
                continue
            api = self.options(cfg['endpoint'])
            known = set(api)
            needed = set(re.findall(r'\$\{(\w+)\}', cfg['label'])) | {cfg.get('value', 'guid')}
            missing = {n for n in needed if n not in known and n != 'guid'}
            if missing:
                problems.append(f"{name}: label/value uses unknown fields {missing}")
        self.assertEqual(problems, [], '\n' + '\n'.join(problems))
