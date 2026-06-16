"""Path / filename safety unit tests for the control-plane (path-traversal-runtime-01).

The runtime mission_store already has thorough traversal tests; the control-plane
equivalents are the dossier export helpers that build Content-Disposition
filenames and in-ZIP paths from ids that ultimately come from URL path params.
"""
from __future__ import annotations

from cadris_cp.routers.dossiers import (
    DOC_ID_TO_ZIP_PATH,
    _safe_filename_component,
    _safe_zip_path,
)


class TestSafeFilenameComponent:
    def test_strips_header_injection_chars(self):
        # Quotes / newlines / CR would otherwise allow Content-Disposition injection.
        assert _safe_filename_component('a"b\r\n../x') == "abx"

    def test_strips_path_separators_and_spaces(self):
        assert _safe_filename_component("evil; rm -rf /") == "evilrm-rf"

    def test_keeps_safe_chars(self):
        assert _safe_filename_component("mission_abc-123") == "mission_abc-123"

    def test_empty_or_all_unsafe_falls_back(self):
        assert _safe_filename_component("") == "dossier"
        assert _safe_filename_component("///...") == "dossier"


class TestSafeZipPath:
    def test_known_doc_id_maps_to_folder_path(self):
        assert _safe_zip_path("vision_produit", ".md") == DOC_ID_TO_ZIP_PATH["vision_produit"]

    def test_known_doc_id_respects_extension(self):
        md = DOC_ID_TO_ZIP_PATH["vision_produit"]
        assert _safe_zip_path("vision_produit", ".pdf") == md.replace(".md", ".pdf")

    def test_unknown_but_valid_id_is_flat_file(self):
        assert _safe_zip_path("validid", ".md") == "validid.md"

    def test_traversal_id_is_rejected(self):
        assert _safe_zip_path("../etc/passwd", ".md") is None
        assert _safe_zip_path("a/b", ".md") is None
        assert _safe_zip_path("UPPER", ".md") is None  # regex requires lowercase start
