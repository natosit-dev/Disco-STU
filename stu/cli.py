"""CLI is an argument parser over the identical application API used by Streamlit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .application import StuApplication
from .contracts import CATEGORIES
from .fixtures import FIXTURES
from .adaption_api import SUPPORTED_MODELS, TEXT_ONLY_MODELS, LEGACY_MODELS


def smoke(app: StuApplication, fixture_id='F01') -> dict:
    """End-to-end synthetic SERA→STU→Review setup, no human judgment fabricated."""
    fixture = FIXTURES[fixture_id]
    capture = app.capture
    sample = capture.create_sample(fixture['source'], title='SYNTHETIC ' + fixture_id,
                                   origin='fixture', domain='technical')
    sid = sample['sample_id']
    capture.save_intention(sid, 'SYNTHETIC ORACLE TEST REFERENCE: ' + fixture['meaning'])
    capture.save_categories(sid, {key: fixture['meaning'] if key == 'claims' else '' for key in CATEGORIES})
    capture.save_units(sid, [{'unit_id': 'H-U1', 'kind': 'claim', 'text': fixture['meaning'],
                              'importance': 'essential', 'polarity': 'affirmed',
                              'source_support': fixture['source'], 'notes': 'synthetic fixture'}])
    capture.freeze(sid)
    study = app.create_study(sid, fixture_id=fixture_id)
    run = app.run_sample(study['study_id'])
    return {'study_id': study['study_id'], 'sample_id': sid, 'run_id': run['run_id'],
            'run_status': run['status'], 'verification': app.validate(study['study_id']),
            'results': app.get_results(study['study_id'])}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog='python -m stu.cli')
    p.add_argument('--data-root', default=os.environ.get('SERA_DATA_DIR', 'data'))
    commands = p.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor')
    s = commands.add_parser('smoke')
    s.add_argument('--adapter', choices=['fixture'], default='fixture')
    s.add_argument('--fixture', choices=sorted(FIXTURES), default='F01')
    r = commands.add_parser('run')
    r.add_argument('--study', required=True)
    r.add_argument('--adapter', choices=['fixture', 'adaption'], default=None)
    r.add_argument('--mode', choices=['synthetic_test', 'live'], default=None)
    for command in ('validate', 'analyze', 'export'):
        sub = commands.add_parser(command)
        sub.add_argument('--study', required=True)
        if command == 'export':
            sub.add_argument('--privacy-level', choices=('full', 'safe'), default='full')
    args = p.parse_args(argv)
    app = StuApplication(args.data_root)
    try:
        if args.command == 'doctor':
            result = {'adapters': ['deterministic_fixture', 'adaption'],
                      'new_study_text_models': list(TEXT_ONLY_MODELS),
                      'historical_supported_models': list(LEGACY_MODELS),
                      'hosted_models': list(SUPPORTED_MODELS),
                      'adaption_key_configured': bool(os.environ.get('ADAPTION_API_KEY')),
                      'data_root': str(Path(args.data_root)),
                      'modes': ['live', 'synthetic_test'],
                      'note': 'Live inference requires a frozen SERA source and API key.'}
        elif args.command == 'smoke':
            result = smoke(app, args.fixture)
        elif args.command == 'run':
            result = app.run_sample(args.study, adapter=args.adapter, mode=args.mode)
        elif args.command == 'validate':
            result = app.validate(args.study)
        elif args.command == 'analyze':
            result = app.get_results(args.study)
        else:
            result = app.export_study(args.study, privacy_level=args.privacy_level)
    except (ValueError, RuntimeError, FileNotFoundError, KeyError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
