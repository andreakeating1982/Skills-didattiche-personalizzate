#!/usr/bin/env python3
"""Test sintetici del validatore; non sono una revisione di alcun podcast reale."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verifica_fedelta import AuditError, audit, sha256


class TestFedelta(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pdf = self.root / 'SOURCE_TEST.bin'
        self.pdf.write_bytes(b'PDF identity fixture, not a real document')
        self.stem = self.root / 'STEM_TEST.bin'
        self.stem.write_bytes(b'stem identity fixture, not playable audio')
        self.video = self.root / 'MP4_TEST.bin'
        self.video.write_bytes(b'video identity fixture, not a real MP4')
        self.hash = sha256(self.pdf)
        self.pages = {
            'pdf_path': str(self.pdf), 'pdf_sha256': self.hash,
            'canonical_pages': [
                {'page': 1, 'text': 'Titolo.\nINDICE\nCapitolo 2', 'visually_checked': True},
                {'page': 2, 'text': 'CAPITOLO\nTesto.\nIN SINTESI\nRelazioni. Parole legame.', 'visually_checked': True},
            ], 'excluded_service_elements': []}
        self.manifest = {'mode': 'integral_from_current_pdf', 'pdf_sha256': self.hash, 'sections': [
            {'id': 'T01', 'pdf_pages': [1], 'source_text': 'Titolo.', 'speech_text': 'Titolo.', 'action': 'reuse_verified',
             'reuse_evidence': {'checked_against_current_pdf': True, 'source_text': 'Titolo.', 'speech_text': 'Titolo.', 'audio_path': str(self.stem), 'audio_sha256': sha256(self.stem)}},
            {'id': 'I01', 'pdf_pages': [1], 'source_text': 'INDICE\nCapitolo 2', 'speech_text': 'Indice. Capitolo. Pagina due.', 'action': 'generate'},
            {'id': 'U01', 'pdf_pages': [2], 'source_text': 'CAPITOLO\nTesto.', 'speech_text': 'Capitolo. Testo.', 'action': 'generate'},
            {'id': 'S01', 'pdf_pages': [2], 'source_text': 'IN SINTESI\nRelazioni. Parole legame.', 'speech_text': 'In sintesi. Relazioni. Parole legame.', 'action': 'generate'},
        ]}
        self.pages_file, self.manifest_file, self.review_file = [self.root / x for x in ['pages.json', 'manifest.json', 'review.json']]
        # Mock only pdfinfo here: these tests exercise coverage and hashes, not a PDF parser.
        mock = patch('verifica_fedelta.subprocess.run', return_value=subprocess.CompletedProcess([], 0, 'Pages: 2\n', ''))
        mock.start()
        self.addCleanup(mock.stop)

    def save(self):
        for path, data in [(self.pages_file, self.pages), (self.manifest_file, self.manifest)]:
            path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def check(self):
        self.save()
        return audit(self.pages_file, self.manifest_file)

    def review(self):
        self.save()
        sections = {s['id']: {'script_vs_pdf_checked': True, 'aac_transcript_compared': True, 'aac_listened': True, 'unresolved_differences': []} for s in self.manifest['sections']}
        return {'pdf_sha256': self.hash, 'manifest_sha256': sha256(self.manifest_file), 'mp4_sha256': sha256(self.video), 'sections': sections,
                'checks': {key: True for key in ['joins_listened', 'cover_start_mid_end_checked', 'final_sentence_checked', 'no_music_checked', 'speed_and_voices_checked', 'full_decode_passed', 'aac_peaks_measured']},
                'last_sentence_heard': 'Synthetic test only.', 'unresolved_issues': [], 'technical_pass': True}

    def final_check(self, review):
        self.review_file.write_text(json.dumps(review), encoding='utf-8')
        return audit(self.pages_file, self.manifest_file, self.video, self.review_file)

    def test_source_only_is_not_ready_for_delivery(self):
        r = self.check()
        self.assertTrue(r['source_coverage_pass'])
        self.assertFalse(r['ready_for_delivery'])

    def test_whitespace_only_is_allowed(self):
        self.manifest['sections'][2]['source_text'] = 'CAPITOLO  \n\nTesto.'
        self.assertTrue(self.check()['source_coverage_pass'])

    def test_old_extra_chapter_is_blocked(self):
        self.manifest['sections'].append({'id': 'OLD', 'pdf_pages': [2], 'source_text': 'ESEMPIO: LA FOTOSINTESI', 'speech_text': 'Esempio.', 'action': 'generate'})
        with self.assertRaises(AuditError): self.check()

    def test_obsolete_synthesis_row_is_blocked(self):
        self.manifest['sections'][3]['source_text'] += '\nRIEPILOGO. Riga della vecchia edizione.'
        with self.assertRaises(AuditError): self.check()

    def test_omission_is_blocked(self):
        self.manifest['sections'].pop()
        with self.assertRaises(AuditError): self.check()

    def test_stale_index_page_is_blocked(self):
        self.manifest['sections'][1]['source_text'] = 'INDICE\nCapitolo 4'
        with self.assertRaises(AuditError): self.check()

    def test_duplicate_id_is_blocked(self):
        self.manifest['sections'].append(copy.deepcopy(self.manifest['sections'][3]))
        with self.assertRaises(AuditError): self.check()

    def test_duplicate_content_with_new_id_is_blocked(self):
        duplicate = copy.deepcopy(self.manifest['sections'][3]); duplicate['id'] = 'DUPLICATE'
        self.manifest['sections'].append(duplicate)
        with self.assertRaises(AuditError): self.check()

    def test_wrong_page_order_is_blocked(self):
        self.manifest['sections'][0], self.manifest['sections'][2] = self.manifest['sections'][2], self.manifest['sections'][0]
        with self.assertRaises(AuditError): self.check()

    def test_wrong_intra_page_order_is_blocked(self):
        self.manifest['sections'][2], self.manifest['sections'][3] = self.manifest['sections'][3], self.manifest['sections'][2]
        with self.assertRaises(AuditError): self.check()

    def test_pdf_changed_under_same_name_is_blocked(self):
        self.pdf.write_bytes(b'New document, same filename')
        with self.assertRaises(AuditError): self.check()

    def test_manifest_from_another_pdf_is_blocked(self):
        self.manifest['pdf_sha256'] = '0' * 64
        with self.assertRaises(AuditError): self.check()

    def test_unverified_canonical_page_is_blocked(self):
        self.pages['canonical_pages'][1]['visually_checked'] = False
        with self.assertRaises(AuditError): self.check()

    def test_reuse_without_evidence_is_blocked(self):
        self.manifest['sections'][0].pop('reuse_evidence')
        with self.assertRaises(AuditError): self.check()

    def test_reused_old_script_is_blocked(self):
        self.manifest['sections'][0]['reuse_evidence']['speech_text'] += ' Old addition.'
        with self.assertRaises(AuditError): self.check()

    def test_changed_stem_is_blocked(self):
        self.stem.write_bytes(b'different stem')
        with self.assertRaises(AuditError): self.check()

    def test_multipage_section_requires_explicit_units(self):
        self.manifest['sections'] = [{'id': 'ALL', 'pdf_pages': [1, 2], 'source_text': '\n'.join(p['text'] for p in self.pages['canonical_pages']), 'speech_text': 'Whole reading.', 'action': 'generate'}]
        with self.assertRaises(AuditError): self.check()

    def test_explicit_multipage_units_pass(self):
        self.manifest['sections'] = [{'id': 'ALL', 'pdf_pages': [1, 2], 'source_text': '\n'.join(p['text'] for p in self.pages['canonical_pages']), 'speech_text': 'Whole reading.', 'action': 'generate',
                                    'source_units': [{'page': p['page'], 'text': p['text']} for p in self.pages['canonical_pages']]}]
        self.assertTrue(self.check()['source_coverage_pass'])

    def test_complete_review_record_passes_structure_check(self):
        self.assertTrue(self.final_check(self.review())['final_review_record_pass'])

    def test_partial_aac_review_is_blocked(self):
        r = self.review(); r['sections'].pop('S01')
        with self.assertRaises(AuditError): self.final_check(r)

    def test_unresolved_difference_is_blocked(self):
        r = self.review(); r['sections']['S01']['unresolved_differences'] = ['Needs listening']
        with self.assertRaises(AuditError): self.final_check(r)

    def test_stale_mp4_review_is_blocked(self):
        r = self.review(); self.video.write_bytes(b'Later export')
        with self.assertRaises(AuditError): self.final_check(r)

    def test_stale_manifest_review_is_blocked(self):
        r = self.review(); self.manifest['sections'][1]['speech_text'] += ' Changed.'; self.save()
        with self.assertRaises(AuditError): self.final_check(r)

    def test_missing_final_checks_are_blocked(self):
        r = self.review(); r['checks']['joins_listened'] = False
        with self.assertRaises(AuditError): self.final_check(r)

    def test_selective_revision_is_not_certified_as_integral(self):
        self.manifest['mode'] = 'selective_audio_repair'
        with self.assertRaises(AuditError): self.check()


if __name__ == '__main__':
    unittest.main(verbosity=2)

