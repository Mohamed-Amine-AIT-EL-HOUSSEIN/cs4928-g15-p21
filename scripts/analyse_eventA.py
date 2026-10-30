"""Reproduce Event A agreement, consolidated labels and metrics.

From the group repository root:
    python scripts/analyse_eventA.py

Requires openpyxl. Reads the original A/B workbooks; never edits them or M2.
"""
from pathlib import Path
from collections import Counter
import argparse
import csv
import hashlib
import json
import re
from openpyxl import load_workbook

MANIFEST = {'application': 'spring-netflix-oss-microservices',
 'replication_commit': '1b8994471e9df0d32e22b31415eead8511078125',
 'inputs': [{'path': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt',
             'sha256': '72bc288f642f0530ff430c9596aa930cdd1fee09b040389180acc114cb071817',
             'localGitBlob': '0ed789dc702cf0538c30829b24859b40ed4b3f50',
             'url': 'https://raw.githubusercontent.com/M3SOulu/EMSE2025SAR-Replication/1b8994471e9df0d32e22b31415eead8511078125/tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt'},
            {'path': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json',
             'sha256': '32efda846decccba0cec9d184b4017905963d9acaf5a5d13377064e49236c06d',
             'localGitBlob': 'ba9ea7111901bba97657f7c74cac83a8407e0c2f',
             'url': 'https://raw.githubusercontent.com/M3SOulu/EMSE2025SAR-Replication/1b8994471e9df0d32e22b31415eead8511078125/tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json'}],
 'items': [{'id': 'G001',
            'characteristic': 'component',
            'item': 'config_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L2',
            'rationale': 'Same component as T006 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L2; JSON /microservices/5/servicename'},
           {'id': 'G002',
            'characteristic': 'component',
            'item': 'github_repository',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L3',
            'rationale': 'Same component as T010 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L3; JSON /external_components/0/name'},
           {'id': 'G003',
            'characteristic': 'component',
            'item': 'discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L4',
            'rationale': 'Same component as T004 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L4; JSON /microservices/3/servicename'},
           {'id': 'G004',
            'characteristic': 'component',
            'item': 'rabbitmq',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L5',
            'rationale': 'Same component as T009 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L5; JSON /microservices/8/servicename'},
           {'id': 'G005',
            'characteristic': 'component',
            'item': 'monitor_dashboard',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L6',
            'rationale': 'Same component as T001 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L6; JSON /microservices/0/servicename'},
           {'id': 'G006',
            'characteristic': 'component',
            'item': 'turbine',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L7',
            'rationale': 'Same component as T007 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L7; JSON /microservices/6/servicename'},
           {'id': 'G007',
            'characteristic': 'component',
            'item': 'statement_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L8',
            'rationale': 'Same component as T005 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L8; JSON /microservices/4/servicename'},
           {'id': 'G008',
            'characteristic': 'component',
            'item': 'card_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L9',
            'rationale': 'Same component as T003 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L9; JSON /microservices/2/servicename'},
           {'id': 'G009',
            'characteristic': 'component',
            'item': 'card_statement_composite',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L10',
            'rationale': 'Same component as T002 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L10; JSON /microservices/1/servicename'},
           {'id': 'G010',
            'characteristic': 'component',
            'item': 'edge_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L11',
            'rationale': 'Same component as T008 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L11; JSON /microservices/7/servicename'},
           {'id': 'G011',
            'characteristic': 'component',
            'item': 'user',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L12',
            'rationale': 'Same component as T011 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: GT L12; JSON /external_components/1/name'},
           {'id': 'G012',
            'characteristic': 'connection',
            'item': 'github_repository -> config_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L15',
            'rationale': 'Same sender, receiver and direction as T012 under frozen rules 2–3. Evidence: GT '
                         'L15; JSON /information_flows/0'},
           {'id': 'G013',
            'characteristic': 'connection',
            'item': 'config_server -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L16',
            'rationale': 'Same sender, receiver and direction as T016 under frozen rules 2–3. Evidence: GT '
                         'L16; JSON /information_flows/4'},
           {'id': 'G014',
            'characteristic': 'connection',
            'item': 'monitor_dashboard -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L17',
            'rationale': 'Same sender, receiver and direction as T023 under frozen rules 2–3. Evidence: GT '
                         'L17; JSON /information_flows/11'},
           {'id': 'G015',
            'characteristic': 'connection',
            'item': 'config_server -> monitor_dashboard',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L18',
            'rationale': 'Same sender, receiver and direction as T013 under frozen rules 2–3. Evidence: GT '
                         'L18; JSON /information_flows/1'},
           {'id': 'G016',
            'characteristic': 'connection',
            'item': 'turbine -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L19',
            'rationale': 'Same sender, receiver and direction as T022 under frozen rules 2–3. Evidence: GT '
                         'L19; JSON /information_flows/10'},
           {'id': 'G017',
            'characteristic': 'connection',
            'item': 'rabbitmq -> turbine',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L20',
            'rationale': 'Same sender, receiver and direction as T034 under frozen rules 2–3. Evidence: GT '
                         'L20; JSON /information_flows/32'},
           {'id': 'G018',
            'characteristic': 'connection',
            'item': 'config_server -> turbine',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L21',
            'rationale': 'Same sender, receiver and direction as T018 under frozen rules 2–3. Evidence: GT '
                         'L21; JSON /information_flows/6'},
           {'id': 'G019',
            'characteristic': 'connection',
            'item': 'turbine -> monitor_dashboard',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L22',
            'rationale': 'Same sender, receiver and direction as T033 under frozen rules 2–3. Evidence: GT '
                         'L22; JSON /information_flows/31'},
           {'id': 'G020',
            'characteristic': 'connection',
            'item': 'statement_service -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L23',
            'rationale': 'Same sender, receiver and direction as T025 under frozen rules 2–3. Evidence: GT '
                         'L23; JSON /information_flows/13'},
           {'id': 'G021',
            'characteristic': 'connection',
            'item': 'config_server -> statement_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L24',
            'rationale': 'Same sender, receiver and direction as T017 under frozen rules 2–3. Evidence: GT '
                         'L24; JSON /information_flows/5'},
           {'id': 'G022',
            'characteristic': 'connection',
            'item': 'card_service -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L25',
            'rationale': 'Same sender, receiver and direction as T026 under frozen rules 2–3. Evidence: GT '
                         'L25; JSON /information_flows/15'},
           {'id': 'G023',
            'characteristic': 'connection',
            'item': 'config_server -> card_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L26',
            'rationale': 'Same sender, receiver and direction as T015 under frozen rules 2–3. Evidence: GT '
                         'L26; JSON /information_flows/3'},
           {'id': 'G024',
            'characteristic': 'connection',
            'item': 'card_statement_composite -> discovery_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L27',
            'rationale': 'Same sender, receiver and direction as T027 under frozen rules 2–3. Evidence: GT '
                         'L27; JSON /information_flows/20'},
           {'id': 'G025',
            'characteristic': 'connection',
            'item': 'card_statement_composite -> card_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L28',
            'rationale': 'Reference edge is absent from information_flows with the same sender, receiver and '
                         'direction (rule 3). Evidence: GT L28; JSON /information_flows (all entries '
                         'checked)'},
           {'id': 'G026',
            'characteristic': 'connection',
            'item': 'card_statement_composite -> statement_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L29',
            'rationale': 'Reference edge is absent from information_flows with the same sender, receiver and '
                         'direction (rule 3). Evidence: GT L29; JSON /information_flows (all entries '
                         'checked)'},
           {'id': 'G027',
            'characteristic': 'connection',
            'item': 'config_server -> card_statement_composite',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L30',
            'rationale': 'Same sender, receiver and direction as T014 under frozen rules 2–3. Evidence: GT '
                         'L30; JSON /information_flows/2'},
           {'id': 'G028',
            'characteristic': 'connection',
            'item': 'card_statement_composite -> rabbitmq',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L31',
            'rationale': 'Reference edge is absent from information_flows with the same sender, receiver and '
                         'direction (rule 3). Evidence: GT L31; JSON /information_flows (all entries '
                         'checked)'},
           {'id': 'G029',
            'characteristic': 'connection',
            'item': 'discovery_service -> edge_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L32',
            'rationale': 'Same sender, receiver and direction as T024 under frozen rules 2–3. Evidence: GT '
                         'L32; JSON /information_flows/12'},
           {'id': 'G030',
            'characteristic': 'connection',
            'item': 'user -> edge_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L33',
            'rationale': 'Same sender, receiver and direction as T028 under frozen rules 2–3. Evidence: GT '
                         'L33; JSON /information_flows/26'},
           {'id': 'G031',
            'characteristic': 'connection',
            'item': 'edge_server -> user',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L34',
            'rationale': 'Same sender, receiver and direction as T029 under frozen rules 2–3. Evidence: GT '
                         'L34; JSON /information_flows/27'},
           {'id': 'G032',
            'characteristic': 'connection',
            'item': 'config_server -> edge_server',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L35',
            'rationale': 'Same sender, receiver and direction as T019 under frozen rules 2–3. Evidence: GT '
                         'L35; JSON /information_flows/7'},
           {'id': 'G033',
            'characteristic': 'connection',
            'item': 'edge_server -> card_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L36',
            'rationale': 'Same sender, receiver and direction as T030 under frozen rules 2–3. Evidence: GT '
                         'L36; JSON /information_flows/28'},
           {'id': 'G034',
            'characteristic': 'connection',
            'item': 'edge_server -> statement_service',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L37',
            'rationale': 'Same sender, receiver and direction as T031 under frozen rules 2–3. Evidence: GT '
                         'L37; JSON /information_flows/29'},
           {'id': 'G035',
            'characteristic': 'connection',
            'item': 'edge_server -> card_statement_composite',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L38',
            'rationale': 'Same sender, receiver and direction as T032 under frozen rules 2–3. Evidence: GT '
                         'L38; JSON /information_flows/30'},
           {'id': 'G036',
            'characteristic': 'endpoint',
            'item': 'card_service: /api',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L41',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L41; JSON '
                         '/microservices/2/tagged_values'},
           {'id': 'G037',
            'characteristic': 'endpoint',
            'item': 'card_service: /api/cards',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L41',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L41; JSON '
                         '/microservices/2/tagged_values'},
           {'id': 'G038',
            'characteristic': 'endpoint',
            'item': 'card_service: /api/card/{cardId}',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L41',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L41; JSON '
                         '/microservices/2/tagged_values'},
           {'id': 'G039',
            'characteristic': 'endpoint',
            'item': 'card_service: /api/new-card',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L41',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L41; JSON '
                         '/microservices/2/tagged_values'},
           {'id': 'G040',
            'characteristic': 'endpoint',
            'item': 'statement_service: /api',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L42',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L42; JSON '
                         '/microservices/4/tagged_values'},
           {'id': 'G041',
            'characteristic': 'endpoint',
            'item': 'statement_service: api/statement/{statementId}',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L42',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L42; JSON '
                         '/microservices/4/tagged_values'},
           {'id': 'G042',
            'characteristic': 'endpoint',
            'item': 'statement_service: /api/statement',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L42',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L42; JSON '
                         '/microservices/4/tagged_values'},
           {'id': 'G043',
            'characteristic': 'endpoint',
            'item': 'statement_service: /api/statements',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L42',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L42; JSON '
                         '/microservices/4/tagged_values'},
           {'id': 'G044',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G045',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/cards',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G046',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/card/{cardId}',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G047',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/new-card',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G048',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/statement-by-card',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G049',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/statement/{statementId}',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G050',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/statement',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G051',
            'characteristic': 'endpoint',
            'item': 'card_statement_composite: /api/statements',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L43',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L43; JSON '
                         '/microservices/1/tagged_values'},
           {'id': 'G052',
            'characteristic': 'endpoint',
            'item': 'monitor_dashboard: /',
            'source': 'tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt:L44',
            'rationale': 'Reference path is present; this service has no Endpoints entry in the raw JSON, so '
                         'no corresponding endpoint was reported (rule 3). Evidence: GT L44; JSON '
                         '/microservices/0/tagged_values'},
           {'id': 'T001',
            'characteristic': 'component',
            'item': 'monitor-dashboard',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/0/servicename',
            'rationale': 'Same component as G005 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/0/servicename; GT L6'},
           {'id': 'T002',
            'characteristic': 'component',
            'item': 'card-statement-composite',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/1/servicename',
            'rationale': 'Same component as G009 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/1/servicename; GT L10'},
           {'id': 'T003',
            'characteristic': 'component',
            'item': 'card-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/2/servicename',
            'rationale': 'Same component as G008 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/2/servicename; GT L9'},
           {'id': 'T004',
            'characteristic': 'component',
            'item': 'discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/3/servicename',
            'rationale': 'Same component as G003 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/3/servicename; GT L4'},
           {'id': 'T005',
            'characteristic': 'component',
            'item': 'statement-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/4/servicename',
            'rationale': 'Same component as G007 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/4/servicename; GT L8'},
           {'id': 'T006',
            'characteristic': 'component',
            'item': 'config-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/5/servicename',
            'rationale': 'Same component as G001 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/5/servicename; GT L2'},
           {'id': 'T007',
            'characteristic': 'component',
            'item': 'turbine',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/6/servicename',
            'rationale': 'Same component as G006 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/6/servicename; GT L7'},
           {'id': 'T008',
            'characteristic': 'component',
            'item': 'edge-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/7/servicename',
            'rationale': 'Same component as G010 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/7/servicename; GT L11'},
           {'id': 'T009',
            'characteristic': 'component',
            'item': 'rabbitmq',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/microservices/8/servicename',
            'rationale': 'Same component as G004 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/microservices/8/servicename; GT L5'},
           {'id': 'T010',
            'characteristic': 'component',
            'item': 'github-repository',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/external_components/0/name',
            'rationale': 'Same component as G002 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/external_components/0/name; GT L3'},
           {'id': 'T011',
            'characteristic': 'component',
            'item': 'user',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/external_components/1/name',
            'rationale': 'Same component as G011 under frozen rule 2 (case/separator normalisation). '
                         'Evidence: JSON #/external_components/1/name; GT L12'},
           {'id': 'T012',
            'characteristic': 'connection',
            'item': 'github-repository -> config-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/0',
            'rationale': 'Same sender, receiver and direction as G012 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/0; GT L15'},
           {'id': 'T013',
            'characteristic': 'connection',
            'item': 'config-server -> monitor-dashboard',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/1',
            'rationale': 'Same sender, receiver and direction as G015 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/1; GT L18'},
           {'id': 'T014',
            'characteristic': 'connection',
            'item': 'config-server -> card-statement-composite',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/2',
            'rationale': 'Same sender, receiver and direction as G027 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/2; GT L30'},
           {'id': 'T015',
            'characteristic': 'connection',
            'item': 'config-server -> card-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/3',
            'rationale': 'Same sender, receiver and direction as G023 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/3; GT L26'},
           {'id': 'T016',
            'characteristic': 'connection',
            'item': 'config-server -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/4',
            'rationale': 'Same sender, receiver and direction as G013 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/4; GT L16'},
           {'id': 'T017',
            'characteristic': 'connection',
            'item': 'config-server -> statement-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/5',
            'rationale': 'Same sender, receiver and direction as G021 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/5; GT L24'},
           {'id': 'T018',
            'characteristic': 'connection',
            'item': 'config-server -> turbine',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/6',
            'rationale': 'Same sender, receiver and direction as G018 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/6; GT L21'},
           {'id': 'T019',
            'characteristic': 'connection',
            'item': 'config-server -> edge-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/7',
            'rationale': 'Same sender, receiver and direction as G032 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/7; GT L35'},
           {'id': 'T020',
            'characteristic': 'connection',
            'item': 'monitor -> rabbitmq',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/8',
            'rationale': 'No monitor->rabbitmq reference edge. Treating monitor as an alias for '
                         'monitor_dashboard would still not provide that reference edge (rules 2–4). '
                         'Evidence: JSON #/information_flows/8; GT Connections section L15–38'},
           {'id': 'T021',
            'characteristic': 'connection',
            'item': 'turbine -> rabbitmq',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/9',
            'rationale': 'Reported turbine->rabbitmq is absent from the reference. Reverse G017 is '
                         'separately recovered by T034; this extra direction is FP (rule 4). Evidence: JSON '
                         '#/information_flows/9; GT G017/L20 and full Connections section'},
           {'id': 'T022',
            'characteristic': 'connection',
            'item': 'turbine -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/10',
            'rationale': 'Same sender, receiver and direction as G016 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/10; GT L19'},
           {'id': 'T023',
            'characteristic': 'connection',
            'item': 'monitor-dashboard -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/11',
            'rationale': 'Same sender, receiver and direction as G014 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/11; GT L17'},
           {'id': 'T024',
            'characteristic': 'connection',
            'item': 'discovery-service -> edge-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/12',
            'rationale': 'Same sender, receiver and direction as G029 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/12; GT L32'},
           {'id': 'T025',
            'characteristic': 'connection',
            'item': 'statement-service -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/13',
            'rationale': 'Same sender, receiver and direction as G020 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/13; GT L23'},
           {'id': 'T026',
            'characteristic': 'connection',
            'item': 'card-service -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/15',
            'rationale': 'Same sender, receiver and direction as G022 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/15; GT L25'},
           {'id': 'T027',
            'characteristic': 'connection',
            'item': 'card-statement-composite -> discovery-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/20',
            'rationale': 'Same sender, receiver and direction as G024 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/20; GT L27'},
           {'id': 'T028',
            'characteristic': 'connection',
            'item': 'user -> edge-server',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/26',
            'rationale': 'Same sender, receiver and direction as G030 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/26; GT L33'},
           {'id': 'T029',
            'characteristic': 'connection',
            'item': 'edge-server -> user',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/27',
            'rationale': 'Same sender, receiver and direction as G031 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/27; GT L34'},
           {'id': 'T030',
            'characteristic': 'connection',
            'item': 'edge-server -> card-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/28',
            'rationale': 'Same sender, receiver and direction as G033 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/28; GT L36'},
           {'id': 'T031',
            'characteristic': 'connection',
            'item': 'edge-server -> statement-service',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/29',
            'rationale': 'Same sender, receiver and direction as G034 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/29; GT L37'},
           {'id': 'T032',
            'characteristic': 'connection',
            'item': 'edge-server -> card-statement-composite',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/30',
            'rationale': 'Same sender, receiver and direction as G035 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/30; GT L38'},
           {'id': 'T033',
            'characteristic': 'connection',
            'item': 'turbine -> monitor-dashboard',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/31',
            'rationale': 'Same sender, receiver and direction as G019 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/31; GT L22'},
           {'id': 'T034',
            'characteristic': 'connection',
            'item': 'rabbitmq -> turbine',
            'source': 'tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json#/information_flows/32',
            'rationale': 'Same sender, receiver and direction as G017 under frozen rules 2–3. Evidence: JSON '
                         '#/information_flows/32; GT L20'}]}

def empty_link(value):
    return '' if value is None or str(value).strip().upper() in {'','N/A','NA'} else str(value).strip()

def read_rater(path, manifest):
    wb=load_workbook(path,data_only=False)
    sheet=wb[manifest['application'][:31]]
    rows={};normalised=[]
    expected={r['id']:r for r in manifest['items']}
    for values in sheet.iter_rows():
        rid=values[0].value
        if not isinstance(rid,str) or not re.fullmatch(r'[GT]\d+',rid):
            continue
        if rid in rows:raise ValueError(f'{path.name}: duplicate ID {rid}')
        row={'id':rid,'characteristic':values[1].value,'item':values[2].value,
             'label':values[3].value,'match_id':empty_link(values[4].value),'note':values[5].value or ''}
        if row['label'] not in ({'TP','FN'} if rid.startswith('G') else {'MATCH','FP'}):
            raise ValueError(f'{path.name} {rid}: blank or invalid label')
        if values[4].value not in (None,'') and not row['match_id']:
            normalised.append(rid)
        rows[rid]=row
    if set(rows)!=set(expected):raise ValueError(f'{path.name}: IDs differ from pinned inputs')
    for rid,r in rows.items():
        if (r['characteristic'],r['item'])!=(expected[rid]['characteristic'],expected[rid]['item']):
            raise ValueError(f'{path.name} {rid}: source item changed')
        if r['label'] in {'FN','FP'}:
            if r['match_id']:raise ValueError(f'{path.name} {rid}: unmatched item has matching ID')
        else:
            link=r['match_id'];other=rows.get(link)
            if not other or other['match_id']!=rid or other['characteristic']!=r['characteristic']:
                raise ValueError(f'{path.name} {rid}: invalid/nonreciprocal matching ID')
            if other['label']!=('MATCH' if rid.startswith('G') else 'TP'):
                raise ValueError(f'{path.name} {rid}: invalid paired label')
    return rows,normalised

def agreement(a,b,ids):
    pairs=[(a[i]['label'],b[i]['label']) for i in ids]
    n=len(pairs);ca=Counter(x for x,y in pairs);cb=Counter(y for x,y in pairs)
    po=sum(x==y for x,y in pairs)/n
    pe=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n)
    return {'n':n,'percent_agreement':100*po,'po':po,'pe':pe,
            'kappa':(po-pe)/(1-pe) if pe!=1 else None}

def write_csv(path,headers,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader();writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--rater-a',type=Path)
    parser.add_argument('--rater-b',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    root=args.root.resolve();event=root/'eventA';out=args.out or event/'results'
    manifest=MANIFEST
    a_path=args.rater_a or event/'rater1_counts.xlsx'
    b_path=args.rater_b or event/'rater2_counts.xlsx'
    a,na=read_rater(a_path,manifest);b,nb=read_rater(b_path,manifest)
    conflicts=[]
    for item in manifest['items']:
        rid=item['id']
        if (a[rid]['label'],a[rid]['match_id'])!=(b[rid]['label'],b[rid]['match_id']):
            conflicts.append({'id':rid,'characteristic':item['characteristic'],'item':item['item'],
                              'A_label':a[rid]['label'],'B_label':b[rid]['label'],
                              'A_match_id':a[rid]['match_id'],'B_match_id':b[rid]['match_id']})
    ag={table:agreement(a,b,[r['id'] for r in manifest['items'] if r['id'].startswith(table)]) for table in ['G','T']}
    out.mkdir(parents=True,exist_ok=True)
    inputs={name:{'path':str(p.relative_to(root)) if p.is_relative_to(root) else p.name,
                  'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for name,p in [('A',a_path),('B',b_path)]}
    result={'status':'complete' if not conflicts else 'unresolved_conflicts','application':manifest['application'],
            'inputs':inputs,'agreement':ag,'conflict_count':len(conflicts),
            'normalised_empty_matching_ids':{'A':na,'B':nb}}
    lines=['# Event A agreement and reconciliation','','Application: `'+manifest['application']+'`.',
           '','|Table|Items|Agreement|Observed Po|Chance Pe|Cohen kappa|','|---|---:|---:|---:|---:|---:|']
    for table,label in [('G','A: reference items (TP/FN)'),('T','B: tool items (MATCH/FP)')]:
        r=ag[table];k='n/a' if r['kappa'] is None else f"{r['kappa']:.6f}"
        lines.append(f"|{label}|{r['n']}|{r['percent_agreement']:.1f}%|{r['po']:.6f}|{r['pe']:.6f}|{k}|")
    lines += ['',f'Label or effective matching-ID conflicts: **{len(conflicts)}**.',
              '',f"N/A/NA matching-ID placeholders normalised to empty in memory: A={len(na)}, B={len(nb)}. Original workbooks are never edited.",
              '','Kappa quantifies agreement between the supplied labels; it does not by itself establish independence or validate the reference architecture.','','## Input versions','']
    for name,v in inputs.items():lines += [f"- {name}: `{v['path']}`",f"  SHA256 `{v['sha256']}`"]
    final_headers=['id','characteristic','item','label','match_id','evidence_source','rationale']
    metric_headers=['scope','TP','FP','FN','precision','recall','F1']
    if conflicts:
        lines += ['', '|ID|Type|Item|A label|B label|A match|B match|', '|---|---|---|---|---|---|---|']
        for c in conflicts:
            lines.append('|'+ '|'.join(str(c[k]) for k in ['id','characteristic','item','A_label','B_label','A_match_id','B_match_id'])+'|')
        write_csv(out/'final_labels.csv',final_headers,[])
        write_csv(out/'metrics.csv',metric_headers,[])
        lines += ['','## Reconciliation status','','Unresolved conflicts remain. No final labels or metrics have been generated. Resolve them with recorded reasons first.']
        (out/'agreement.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        raise SystemExit('Unresolved conflicts: final label and metric files contain headers only.')
    final=[]
    for item in manifest['items']:
        r=b[item['id']]
        final.append({k:r[k] for k in ['id','characteristic','item','label','match_id']}|
                     {'evidence_source':item['source'],'rationale':item['rationale']})
    metrics=[]
    for scope in ['component','connection','endpoint','all']:
        rows=[r for r in final if scope=='all' or r['characteristic']==scope]
        tp=sum(r['label']=='TP' for r in rows);fp=sum(r['label']=='FP' for r in rows);fn=sum(r['label']=='FN' for r in rows)
        metrics.append({'scope':scope,'TP':tp,'FP':fp,'FN':fn,
                        'precision':tp/(tp+fp) if tp+fp else None,
                        'recall':tp/(tp+fn) if tp+fn else None,
                        'F1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None})
    write_csv(out/'final_labels.csv',final_headers,final)
    write_csv(out/'metrics.csv',metric_headers,metrics)
    result['metrics']=metrics
    lines += ['','## Final-label rule','',
              'Both submitted labels and matching IDs agree for every item. No disputed decisions or tie-breaker actions were required. The consolidated labels are in [final_labels.csv](final_labels.csv); they do not replace the original A/B sheets.',
              '','Final labels preserve the decisions shared by the two submitted sheets. No independent adjudication was needed because no conflicting labels or matching IDs were found.',
              '','## Metric calculation','',
              'TP = reference-table TP count; FN = reference-table FN count; FP = tool-table FP count. MATCH is not counted as a second TP.',
              '','Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2TP/(2TP+FP+FN). Undefined denominators are empty in metrics.csv, not zero.',
              '','Re-run from repository root: `python scripts/analyse_eventA.py` (Python 3.10+ and openpyxl).']
    (out/'agreement.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'conflicts':len(conflicts),'agreement':ag,'metrics':metrics},indent=2))

if __name__=='__main__':main()
