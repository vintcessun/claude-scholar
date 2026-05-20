#!/usr/bin/env python3
"""
Optional Semantic Scholar enrichment helper for survey-navigator.

Usage:
    python skills/survey-navigator/scripts/enrich_references_semantic_scholar.py \
        --input skills/survey-navigator/examples/sample-references.json \
        --output D:/tmp/enriched-references.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from copy import deepcopy
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


GRAPH_API_BASE = "https://api.semanticscholar.org/graph/v1"
REQUEST_FIELDS = (
    "title,authors,year,venue,abstract,citationCount,"
    "influentialCitationCount,externalIds,url,openAccessPdf,fieldsOfStudy"
)
DEFAULT_TIMEOUT = 15
DEFAULT_SLEEP_SECONDS = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Best-effort Semantic Scholar enrichment for survey references."
    )
    parser.add_argument("--input", required=True, help="Input references JSON path")
    parser.add_argument("--output", required=True, help="Output enriched JSON path")
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=DEFAULT_SLEEP_SECONDS,
        help="Sleep interval between requests in no-key mode (default: 1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds (default: 15)",
    )
    return parser.parse_args()


def load_references(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError("Input JSON must be a list of reference objects.")
    normalized: List[Dict[str, Any]] = []
    for item in payload:
        if isinstance(item, dict):
            normalized.append(item)
        else:
            normalized.append({"raw_reference": item})
    return normalized


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    return " ".join(text.split())


def similarity(a: Any, b: Any) -> float:
    left = normalize_text(a)
    right = normalize_text(b)
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def first_nonempty(*values: Any) -> Optional[Any]:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None


def normalize_arxiv_id(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    lowered = text.lower()
    for prefix in ("arxiv:", "arxiv.org/abs/", "https://arxiv.org/abs/", "http://arxiv.org/abs/"):
        if lowered.startswith(prefix):
            text = text[len(prefix):]
            lowered = text.lower()
    if "arxiv.org/abs/" in lowered:
        text = text.split("arxiv.org/abs/", 1)[1]
    return text.strip().rstrip("/")


def build_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "claude-scholar-survey-navigator/0.1",
    }
    api_key = os.environ.get("S2_API_KEY", "").strip()
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def http_get_json(url: str, headers: Dict[str, str], timeout: int) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[int]]:
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            payload = json.loads(response.read().decode("utf-8"))
            return payload, None, status
    except HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = str(exc)
        return None, f"HTTP {exc.code}: {body[:200]}", exc.code
    except URLError as exc:
        return None, f"URL error: {exc.reason}", None
    except TimeoutError:
        return None, "Timeout error", None
    except Exception as exc:
        return None, f"Unexpected error: {exc}", None


def fetch_by_paper_id(paper_id: str, headers: Dict[str, str], timeout: int) -> Tuple[Optional[Dict[str, Any]], str, Optional[int]]:
    encoded_id = quote(paper_id, safe=":")
    url = f"{GRAPH_API_BASE}/paper/{encoded_id}?fields={quote(REQUEST_FIELDS, safe=',')}"
    payload, error, status_code = http_get_json(url, headers=headers, timeout=timeout)
    if payload is not None:
        return payload, "", status_code
    return None, error or "Unknown API error", status_code


def fetch_by_title(title: str, headers: Dict[str, str], timeout: int) -> Tuple[Optional[List[Dict[str, Any]]], str, Optional[int]]:
    query = urlencode({"query": title, "limit": 5, "fields": REQUEST_FIELDS})
    url = f"{GRAPH_API_BASE}/paper/search?{query}"
    payload, error, status_code = http_get_json(url, headers=headers, timeout=timeout)
    if payload is None:
        return None, error or "Unknown API error", status_code
    data = payload.get("data")
    if isinstance(data, list):
        return data, "", status_code
    return [], "", status_code


def default_enriched_metadata() -> Dict[str, Any]:
    return {
        "title": "unknown",
        "authors": "unknown",
        "year": "unknown",
        "venue": "unknown",
        "abstract": "unknown",
        "citationCount": "unknown",
        "influentialCitationCount": "unknown",
        "externalIds": "unknown",
        "url": "unknown",
        "openAccessPdf": "unknown",
        "fieldsOfStudy": "unknown",
    }


def normalize_paper_metadata(paper: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    metadata = default_enriched_metadata()
    if not isinstance(paper, dict):
        return metadata

    title = first_nonempty(paper.get("title"))
    authors_raw = paper.get("authors")
    authors: Any = "unknown"
    if isinstance(authors_raw, list) and authors_raw:
        author_names = []
        for author in authors_raw:
            if isinstance(author, dict):
                name = first_nonempty(author.get("name"))
                if name:
                    author_names.append(name)
        if author_names:
            authors = author_names

    year = first_nonempty(paper.get("year"))
    venue = first_nonempty(paper.get("venue"))
    abstract = first_nonempty(paper.get("abstract"))
    citation_count = first_nonempty(paper.get("citationCount"))
    influential_citation_count = first_nonempty(paper.get("influentialCitationCount"))
    external_ids = first_nonempty(paper.get("externalIds"))
    url = first_nonempty(paper.get("url"))
    open_access_pdf = first_nonempty(paper.get("openAccessPdf"))
    fields_of_study = first_nonempty(paper.get("fieldsOfStudy"))

    metadata["title"] = title if title is not None else "unknown"
    metadata["authors"] = authors
    metadata["year"] = year if year is not None else "unknown"
    metadata["venue"] = venue if venue is not None else "unknown"
    metadata["abstract"] = abstract if abstract is not None else "unknown"
    metadata["citationCount"] = citation_count if citation_count is not None else "unknown"
    metadata["influentialCitationCount"] = (
        influential_citation_count if influential_citation_count is not None else "unknown"
    )
    metadata["externalIds"] = external_ids if external_ids is not None else "unknown"
    metadata["url"] = url if url is not None else "unknown"
    metadata["openAccessPdf"] = open_access_pdf if open_access_pdf is not None else "unknown"
    metadata["fieldsOfStudy"] = fields_of_study if fields_of_study is not None else "unknown"
    return metadata


def score_candidate(reference: Dict[str, Any], candidate: Dict[str, Any]) -> float:
    title_score = similarity(reference.get("title", ""), candidate.get("title", ""))
    candidate_year = candidate.get("year")
    ref_year = normalize_text(reference.get("year"))
    year_score = 0.0
    if ref_year and candidate_year is not None:
        try:
            year_score = 1.0 if int(ref_year) == int(candidate_year) else 0.0
        except (TypeError, ValueError):
            year_score = 0.0
    author_score = 0.0
    ref_authors = normalize_text(reference.get("authors", ""))
    candidate_authors = candidate.get("authors") or []
    if ref_authors and isinstance(candidate_authors, list):
        author_names = " ".join(
            author.get("name", "") for author in candidate_authors if isinstance(author, dict)
        )
        author_score = similarity(ref_authors, author_names)
    return title_score * 0.75 + year_score * 0.15 + author_score * 0.10


def enrich_reference(
    reference: Dict[str, Any],
    headers: Dict[str, str],
    timeout: int,
) -> Dict[str, Any]:
    result = deepcopy(reference)
    result["original_reference"] = deepcopy(reference)
    result["enriched_metadata"] = default_enriched_metadata()
    result["enrichment_status"] = "skipped"
    result["enrichment_source"] = "manual"
    result["confidence_note"] = "No enrichment attempt was made."

    doi = normalize_text(reference.get("doi"))
    arxiv_id = normalize_arxiv_id(reference.get("arxiv"))
    title = str(reference.get("title", "")).strip()

    if doi:
        paper, error, status_code = fetch_by_paper_id(f"DOI:{doi}", headers=headers, timeout=timeout)
        if paper is not None:
            result["enriched_metadata"] = normalize_paper_metadata(paper)
            result["enrichment_status"] = "matched"
            result["enrichment_source"] = "semantic_scholar"
            result["confidence_note"] = "Matched by DOI through Semantic Scholar Graph API."
            return result
        if status_code == 404:
            result["confidence_note"] = "DOI not found in Semantic Scholar. Proceeded to fallback lookup."
        elif status_code == 429:
            result["enrichment_status"] = "api_error"
            result["confidence_note"] = "Semantic Scholar rate limit (429) while resolving DOI; keep manual review."
            return result
        elif error:
            result["enrichment_status"] = "api_error"
            result["confidence_note"] = f"Semantic Scholar DOI lookup failed: {error}"
            return result

    if arxiv_id:
        paper, error, status_code = fetch_by_paper_id(f"ARXIV:{arxiv_id}", headers=headers, timeout=timeout)
        if paper is not None:
            result["enriched_metadata"] = normalize_paper_metadata(paper)
            result["enrichment_status"] = "matched"
            result["enrichment_source"] = "semantic_scholar"
            result["confidence_note"] = "Matched by arXiv ID through Semantic Scholar Graph API."
            return result
        if status_code == 404:
            result["confidence_note"] = "arXiv ID not found in Semantic Scholar. Proceeded to title lookup."
        elif status_code == 429:
            result["enrichment_status"] = "api_error"
            result["confidence_note"] = "Semantic Scholar rate limit (429) while resolving arXiv ID; keep manual review."
            return result
        elif error:
            result["enrichment_status"] = "api_error"
            result["confidence_note"] = f"Semantic Scholar arXiv lookup failed: {error}"
            return result

    if not title:
        result["enrichment_status"] = "skipped"
        result["confidence_note"] = "Missing DOI, arXiv ID, and title; skipped enrichment."
        return result

    candidates, error, status_code = fetch_by_title(title, headers=headers, timeout=timeout)
    if candidates is None:
        result["enrichment_status"] = "api_error"
        if status_code == 429:
            result["confidence_note"] = "Semantic Scholar rate limit (429) during title search; keep manual review."
        else:
            result["confidence_note"] = f"Semantic Scholar title search failed: {error}"
        return result

    if not candidates:
        result["enrichment_status"] = "not_found"
        result["confidence_note"] = "No Semantic Scholar title match found; keep manual review."
        return result

    scored: List[Tuple[float, Dict[str, Any]]] = [
        (score_candidate(reference, candidate), candidate) for candidate in candidates
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_candidate = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0

    if best_score < 0.75:
        result["enrichment_status"] = "not_found"
        result["confidence_note"] = (
            f"Title search returned only weak matches (best similarity {best_score:.2f}); keep manual review."
        )
        return result

    result["enriched_metadata"] = normalize_paper_metadata(best_candidate)
    result["enrichment_source"] = "semantic_scholar"

    if second_score >= 0.75 and abs(best_score - second_score) < 0.08:
        result["enrichment_status"] = "ambiguous"
        result["confidence_note"] = (
            f"Title search produced multiple plausible matches (best {best_score:.2f}, second {second_score:.2f}); manual review required."
        )
        return result

    result["enrichment_status"] = "matched"
    result["confidence_note"] = f"Matched by title search through Semantic Scholar (similarity {best_score:.2f})."
    return result


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        references = load_references(input_path)
    except Exception as exc:
        print(f"Error: failed to load input references: {exc}", file=sys.stderr)
        return 1

    ensure_parent_dir(output_path)

    headers = build_headers()
    no_key_mode = "x-api-key" not in headers
    enriched: List[Dict[str, Any]] = []

    for index, reference in enumerate(references, start=1):
        enriched.append(enrich_reference(reference, headers=headers, timeout=args.timeout))
        if no_key_mode and index < len(references):
            time.sleep(max(args.sleep_seconds, 0.0))

    output_payload = {
        "resolver": "semantic_scholar",
        "api_key_used": not no_key_mode,
        "request_fields": REQUEST_FIELDS.split(","),
        "generated_at_epoch": int(time.time()),
        "records": enriched,
    }

    try:
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(output_payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except OSError as exc:
        print(f"Error: failed to write output file '{output_path}': {exc}", file=sys.stderr)
        return 1

    status_counts: Dict[str, int] = {}
    for item in enriched:
        status = str(item.get("enrichment_status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"Saved enriched references to: {output_path}")
    print(f"Status counts: {json.dumps(status_counts, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
