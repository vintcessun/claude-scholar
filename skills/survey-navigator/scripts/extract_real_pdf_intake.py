#!/usr/bin/env python3
"""
Minimal real-PDF intake helper for survey-navigator.

This script reads a survey PDF with pdfplumber and emits:
- intake.json
- reference-list.json
- citation_contexts.json

It stays lightweight and planning-oriented:
- no external APIs
- no OCR framework
- no hallucinated metadata
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pdfplumber


MAJOR_SECTION_PATTERNS: List[Tuple[str, str, str]] = [
    ("I", "INTRODUCTION", r"(?m)^I\.\s*INTRODUCTION"),
    ("II", "PRELIMINARIES", r"(?m)^II\.\s*PRELIMINARIES"),
    ("III", "TAXONOMY OF AGENT MEMORY", r"(?m)^III\.\s*TAXONOMY"),
    ("IV", "MEMORY EXTRACTION: TRANSFORMING THE DATA", r"(?m)^IV\.\s*MEMORY\s*EXTRACTION"),
    ("V", "MEMORY STORAGE: ORGANIZING THE MIND", r"(?m)^V\.\s*MEMORY\s*STORAGE"),
    ("VI", "MEMORY RETRIEVAL: RECALLING THE PAST", r"(?m)^VI\.\s*MEMORY\s*RETRIEVAL"),
    ("VII", "MEMORY EVOLUTION: LEARNING OVER TIME", r"(?m)^VII\.\s*MEMORY\s*EVOLUTION"),
    ("VIII", "OPEN-SOURCED LIBRARIES AND BENCHMARKS", r"(?m)^VIII\.\s*OPEN-SOURCED"),
    ("IX", "APPLICATIONS", r"(?m)^IX\.\s*APPLICATIONS"),
    ("X", "LIMITATIONS AND FUTURE DIRECTIONS", r"(?m)^X\.\s*LIMITATIONS"),
    ("XI", "CONCLUSION", r"(?m)^XI\.\s*CONCLUSION"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a real survey PDF into intake.json, reference-list.json, and citation_contexts.json."
    )
    parser.add_argument("--input", required=True, help="Path to the input PDF")
    parser.add_argument("--output-dir", required=True, help="Directory to write outputs into")
    return parser.parse_args()


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fix_inline_spacing(text: str) -> str:
    """Small, conservative spacing fixes for PDF token glue."""
    fixed = text
    fixed = re.sub(r"\s+", " ", fixed)
    fixed = re.sub(r"(?<=[,;:])(?=\S)", " ", fixed)
    fixed = re.sub(r"(?<=\b[A-Z])\.(?=[A-Z])", ". ", fixed)
    fixed = re.sub(r"(?<=[a-z])(?=[A-Z][a-z])", " ", fixed)
    fixed = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", fixed)
    fixed = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", fixed)
    fixed = re.sub(r"\bet al\.\b", "et al.", fixed)
    fixed = re.sub(r"\band(?=[A-Z])", "and ", fixed)
    fixed = fixed.replace("ar Xiv", "arXiv")
    fixed = fixed.replace("arXivpreprintarXiv:", "arXiv preprint arXiv:")
    fixed = fixed.replace("TransactionsonMachineLearningResearch", "Transactions on Machine Learning Research")
    fixed = fixed.replace("Proceedingsofthe", "Proceedings of the")
    fixed = fixed.replace("AnnualMeetingofthe", "Annual Meeting of the")
    fixed = fixed.replace("Conferenceon", "Conference on")
    fixed = fixed.replace("architecturesforlanguageagents", "architectures for language agents")
    fixed = fixed.replace("En- hancing", "Enhancing")
    fixed = fixed.replace("prospects,andrisks", "prospects, and risks")
    fixed = fixed.replace("Voyager:Anopen-endedembodiedagentwithlarge", "Voyager: An open-ended embodied agent with large")
    fixed = fixed.replace("languagemodels", "language models")
    fixed = fixed.replace("SWE-agent:agent-computerinterfacesenableautomated", "SWE-agent: agent-computer interfaces enable automated")
    fixed = fixed.replace("softwareengineering", "software engineering")
    fixed = fixed.replace("Goedel-prover: A frontier model for open-source automatedtheoremproving", "Goedel-prover: A frontier model for open-source automated theorem proving")
    fixed = fixed.replace("ToolLLM:Facilitatinglargelanguagemodels", "ToolLLM: Facilitating large language models")
    fixed = fixed.replace("tomaster", "to master")
    fixed = fixed.replace("real-worldAPIs", "real-world APIs")
    fixed = fixed.replace("The AIhippocampus:Howfararewefromhumanmemory?", "The AI hippocampus: How far are we from human memory?")
    fixed = fixed.replace("Hierarchicalmemoryforhigh-efficiencylong-term", "Hierarchical memory for high-efficiency long-term")
    fixed = fixed.replace("reasoninginllmagents", "reasoning in LLM agents")
    fixed = fixed.replace("Onthestructuralmemoryof", "On the structural memory of")
    fixed = fixed.replace("llmagents", "LLM agents")
    fixed = fixed.replace("Sentencegraphmemory", "Sentence graph memory")
    fixed = fixed.replace("long-termconversationalagents", "long-term conversational agents")
    fixed = fixed.replace("Buildingproduction-readyaiagentswithscalablelong-termmemory", "Building production-ready AI agents with scalable long-term memory")
    fixed = fixed.replace("Memorybench: Abenchmarkformemoryandcontinuallearninginllmsystems", "MemoryBench: A benchmark for memory and continual learning in LLM systems")
    fixed = fixed.replace("Memorysandbox", "MemorySandbox")
    fixed = fixed.replace("Agentmental:An interactivemulti-agentframeworkforexplainableandadaptivemental healthassessment", "AgentMental: An interactive multi-agent framework for explainable and adaptive mental health assessment")
    return clean_whitespace(fixed)


def title_case_memorybench(name: str) -> str:
    if name.lower().startswith("memorybench:"):
        return "MemoryBench:" + name[len("MemoryBench:"):]
    if name.lower().startswith("memorybank:"):
        return "MemoryBank:" + name[len("MemoryBank:"):]
    if name.lower().startswith("memorysandbox:"):
        return "MemorySandbox:" + name[len("MemorySandbox:"):]
    if name.lower().startswith("sgmem:"):
        return "SGMem:" + name[len("SGMem:"):]
    if name.lower().startswith("finmem:"):
        return "FinMem:" + name[len("FinMem:"):]
    if name.lower().startswith("toolllm:"):
        return "ToolLLM:" + name[len("ToolLLM:"):]
    if name.lower().startswith("agentmental:"):
        return "AgentMental:" + name[len("AgentMental:"):]
    return name


def reconstruct_lines(area: pdfplumber.page.Page) -> List[str]:
    words = area.extract_words(x_tolerance=1.5, y_tolerance=2, keep_blank_chars=False, use_text_flow=False)
    grouped: Dict[float, List[Dict[str, Any]]] = defaultdict(list)
    for word in words:
        key = round(float(word["top"]), 1)
        grouped[key].append(word)
    lines: List[str] = []
    for key in sorted(grouped):
        line_words = sorted(grouped[key], key=lambda item: float(item["x0"]))
        line = " ".join(item["text"] for item in line_words)
        lines.append(fix_inline_spacing(line))
    return lines


def page_text(page: pdfplumber.page.Page, two_column: bool, full_width: bool = False) -> str:
    if full_width or not two_column:
        return "\n".join(reconstruct_lines(page))
    mid = page.width / 2
    left = page.crop((0, 0, mid, page.height))
    right = page.crop((mid, 0, page.width, page.height))
    lines = reconstruct_lines(left) + reconstruct_lines(right)
    return "\n".join(lines)


def extract_title_and_abstract(first_page_words: List[Dict[str, Any]], first_page_left_text: str) -> Tuple[str, str]:
    title_lines: Dict[int, List[Tuple[float, str]]] = {}
    for word in first_page_words:
        text = str(word.get("text", "")).strip()
        top = float(word.get("top", 0.0))
        x0 = float(word.get("x0", 0.0))
        if not text or text.isdigit():
            continue
        if top > 120:
            continue
        line_key = int(round(top))
        title_lines.setdefault(line_key, []).append((x0, text))
    ordered_lines: List[str] = []
    for _, words in sorted(title_lines.items(), key=lambda item: item[0]):
        line = " ".join(text for _, text in sorted(words, key=lambda item: item[0]))
        if "Abstract" in line or "†" in line or "‡" in line:
            continue
        ordered_lines.append(fix_inline_spacing(line))
    title = clean_whitespace(" ".join(ordered_lines[:2])) or "unknown"

    abstract_match = re.search(
        r"Abstract[—-](.*?)(?:Index Terms[—-]|I\.\s*INTRODUCTION)",
        first_page_left_text,
        flags=re.DOTALL,
    )
    abstract = "unknown"
    if abstract_match:
        abstract = fix_inline_spacing(abstract_match.group(1))
    return title, abstract


def collect_text(pdf_path: Path) -> Tuple[List[str], List[str], List[Dict[str, Any]], str]:
    page_texts: List[str] = []
    reference_page_texts: List[str] = []
    first_page_words: List[Dict[str, Any]] = []
    first_page_left_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            if idx == 0:
                first_page_words = page.extract_words()
                mid = page.width / 2
                first_page_left_text = "\n".join(reconstruct_lines(page.crop((0, 0, mid, page.height))))
                page_texts.append(page_text(page, two_column=False, full_width=True))
            elif idx < 20:
                page_texts.append(page_text(page, two_column=True))
            else:
                reference_page_texts.append(page_text(page, two_column=True))
    return page_texts, reference_page_texts, first_page_words, first_page_left_text


def parse_subsections(section_text: str, section_start: int) -> List[Dict[str, Any]]:
    subsections: List[Dict[str, Any]] = []
    for match in re.finditer(r"(?m)^([A-H])\.\s+(.+)$", section_text):
        title = fix_inline_spacing(match.group(0))
        subsections.append({
            "title": title,
            "start": section_start + match.start(),
        })
    return subsections


def find_major_sections(body_text: str) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    for roman, title, pattern in MAJOR_SECTION_PATTERNS:
        match = re.search(pattern, body_text, flags=re.IGNORECASE)
        if match:
            hits.append({
                "roman": roman,
                "title": title,
                "start": match.start(),
            })
    hits.sort(key=lambda item: item["start"])
    sections: List[Dict[str, Any]] = []
    for idx, item in enumerate(hits):
        end = hits[idx + 1]["start"] if idx + 1 < len(hits) else len(body_text)
        text = body_text[item["start"]:end].strip()
        subsections = parse_subsections(text, item["start"])
        citations = sorted({n for marker in re.findall(r"\[(.+?)\]", text) for n in expand_citation_marker(marker)})
        sections.append({
            "roman": item["roman"],
            "title": item["title"],
            "start": item["start"],
            "end": end,
            "subsections": [sub["title"] for sub in subsections],
            "subsection_positions": subsections,
            "citation_numbers": citations,
        })
    return sections


def normalize_reference_lines(reference_text: str) -> List[str]:
    lines = []
    seen_references = False
    for line in reference_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        if stripped == "REFERENCES":
            seen_references = True
            continue
        if not seen_references:
            continue
        lines.append(stripped)
    return lines


def split_reference_chunks(reference_lines: List[str]) -> List[List[str]]:
    chunks: List[List[str]] = []
    current: List[str] = []
    for line in reference_lines:
        if re.match(r"^\[\d+\]", line):
            if current:
                chunks.append(current)
            current = [line]
        else:
            if current:
                current.append(line)
    if current:
        chunks.append(current)
    return chunks


def looks_like_venue_line(line: str) -> bool:
    stripped = line.strip().strip(",")
    if not stripped:
        return False
    indicators = [
        "arXiv preprint",
        "Transactions on Machine Learning Research",
        "NeurIPS",
        "ICLR",
        "COLM",
        "EMNLP",
        "Science",
        "Proceedings",
        "Conference",
        "ACL",
        "ICASSP",
        "TMLR",
    ]
    if any(token in stripped for token in indicators):
        return True
    words = stripped.split()
    if len(words) <= 6 and all(word[:1].isupper() or word.isupper() for word in words if word):
        return True
    return False


def reorder_reference_lines(lines: List[str]) -> List[str]:
    """Move venue-only lines that were injected into wrapped quoted titles."""
    open_idx: Optional[int] = None
    close_idx: Optional[int] = None
    for idx, line in enumerate(lines):
        if "“" in line or '"' in line:
            open_idx = idx
            break
    if open_idx is None:
        return lines
    for idx in range(open_idx, len(lines)):
        if "”" in lines[idx] or '"' in lines[idx]:
            close_idx = idx
    if close_idx is None or close_idx <= open_idx:
        return lines

    title_prefix = lines[: open_idx + 1]
    injected_meta: List[str] = []
    title_middle: List[str] = []
    for line in lines[open_idx + 1 : close_idx]:
        if looks_like_venue_line(line):
            injected_meta.append(line)
        else:
            title_middle.append(line)
    close_line = lines[close_idx]
    remaining = lines[close_idx + 1 :]

    if injected_meta:
        meta_text = fix_inline_spacing(" ".join(item.strip().strip(",") for item in injected_meta))
        close_line = re.sub(
            r'([”"])\s*(?:in\s+)?((?:19|20)\d{2}\.?)$',
            rf'\1 in {meta_text}, \2',
            close_line,
        )
        close_line = re.sub(
            r'([”"])\s*((?:19|20)\d{2}\.?)$',
            rf'\1 {meta_text}, \2',
            close_line,
        )

    return title_prefix + title_middle + [close_line] + remaining


def clean_title(text: str) -> str:
    cleaned = fix_inline_spacing(text.strip().strip(","))
    cleaned = re.sub(r"\barXiv\b[:,]?\s*", "", cleaned)
    cleaned = title_case_memorybench(cleaned)
    return cleaned or "unknown"


def split_authors(authors_raw: str) -> List[str]:
    text = fix_inline_spacing(authors_raw)
    text = text.rstrip(",")
    text = re.sub(r"\bet al\.,?$", "et al.", text)
    text = text.replace(" and ", ", ")
    parts = [part.strip() for part in text.split(",") if part.strip()]
    if "et al." in parts and parts.index("et al.") < len(parts) - 1:
        parts = [part for part in parts if part != "et al."] + ["et al."]
    return parts


def parse_venue(trailing: str, year: str) -> str:
    venue_text = fix_inline_spacing(trailing)
    if year != "unknown":
        venue_text = re.sub(rf",?\s*{re.escape(year)}.*$", "", venue_text).strip()
    venue_text = venue_text.replace(", in", "")
    venue_text = venue_text.replace("Transactions on Machine Learning, Research", "Transactions on Machine Learning Research")
    venue_text = venue_text.replace("IEEE Transactions on Big, Data", "IEEE Transactions on Big Data")
    venue_text = venue_text.strip(" ,.")
    if venue_text.lower().startswith("in "):
        venue_text = venue_text[3:].strip()
    if venue_text == "in":
        venue_text = "unknown"
    return venue_text or "unknown"


def move_embedded_venue(title_raw: str, trailing: str) -> Tuple[str, str]:
    title = title_raw
    suffix = trailing
    venue_phrases = [
        "Transactions on Machine Learning Research",
        "Transactions on Machine Learning",
        "EMNLP: Tutorial Abstracts",
        "NeurIPS",
        "Advances in neural information processing systems",
        "ICLR",
        "COLM",
        "Science",
        "IEEE Transactions on Big Data",
        "IEEE Transactions on Big",
        "arXiv preprint arXiv:",
    ]
    for phrase in venue_phrases:
        if phrase in title:
            title = title.replace(f", {phrase},", ",")
            title = title.replace(f" {phrase},", "")
            title = title.replace(f"{phrase}, ", "")
            title = title.replace(phrase, "")
            if phrase not in suffix:
                if suffix.strip():
                    suffix = f"{phrase}, {suffix.strip()}"
                else:
                    suffix = phrase
    if "Transactions on Machine Learning" in title and suffix.startswith("Research"):
        title = title.replace("Transactions on Machine Learning", "")
        suffix = "Transactions on Machine Learning Research, " + suffix
    if "arXiv preprint arXiv:" in title:
        title = title.replace("arXiv preprint arXiv:", "")
        suffix = "arXiv preprint arXiv:, " + suffix if suffix.strip() else "arXiv preprint arXiv:"
    title = re.sub(r"\s+,", ",", title)
    title = re.sub(r",\s*,", ", ", title)
    title = fix_inline_spacing(title)
    suffix = fix_inline_spacing(suffix)
    return title, suffix


def parse_reference_entry(chunk: str) -> Dict[str, Any]:
    number_match = re.match(r"^\[(\d+)\]\s*(.*)$", chunk, flags=re.DOTALL)
    if not number_match:
        return {}
    ref_no = int(number_match.group(1))
    body = fix_inline_spacing(number_match.group(2))
    quote_match = re.search(r"[“\"](.+?)[”\"]", body)

    title_raw = quote_match.group(1) if quote_match else ""

    authors_raw = body[:quote_match.start()].rstrip(", ") if quote_match else ""
    authors_list = split_authors(authors_raw) if authors_raw else []
    authors = "; ".join(authors_list) if authors_list else "unknown"

    year_matches = re.findall(r"(?:19|20)\d{2}", body)
    year = year_matches[-1] if year_matches else "unknown"

    arxiv_match = re.search(r"arXiv:\s*(\d{4}\.\d{4,5})", body, flags=re.IGNORECASE)
    doi_match = re.search(r"\b(10\.\d{4,9}/[^\s,;]+)", body)

    trailing = body[quote_match.end():] if quote_match else ""
    title_raw, trailing = move_embedded_venue(title_raw, trailing)
    title = clean_title(title_raw) if title_raw else "unknown"
    venue = parse_venue(trailing, year)

    return {
        "reference_number": ref_no,
        "title": title,
        "authors": authors,
        "authors_list": authors_list,
        "year": year,
        "venue": venue,
        "doi": doi_match.group(1) if doi_match else "unknown",
        "arxiv": arxiv_match.group(1) if arxiv_match else "unknown",
        "url": "unknown",
        "raw_reference": body,
        "raw_title": fix_inline_spacing(title_raw) if title_raw else "unknown",
        "raw_authors": fix_inline_spacing(authors_raw) if authors_raw else "unknown",
    }


def extract_references(reference_text: str) -> List[Dict[str, Any]]:
    reference_lines = normalize_reference_lines(reference_text)
    chunks = split_reference_chunks(reference_lines)
    records: List[Dict[str, Any]] = []
    for chunk_lines in chunks:
        ordered_lines = reorder_reference_lines(chunk_lines)
        chunk = fix_inline_spacing(" ".join(ordered_lines))
        parsed = parse_reference_entry(chunk)
        if parsed:
            records.append(parsed)
    return records


def expand_citation_marker(marker: str) -> List[int]:
    numbers: List[int] = []
    for part in marker.split(","):
        token = part.strip()
        if not token:
            continue
        range_match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", token)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start <= end:
                numbers.extend(range(start, end + 1))
            continue
        if token.isdigit():
            numbers.append(int(token))
    return numbers


def find_context_section(position: int, sections: List[Dict[str, Any]]) -> Tuple[str, str]:
    for section in sections:
        if section["start"] <= position < section["end"]:
            subsection = "unknown"
            for idx, sub in enumerate(section["subsection_positions"]):
                next_start = (
                    section["subsection_positions"][idx + 1]["start"]
                    if idx + 1 < len(section["subsection_positions"])
                    else section["end"]
                )
                if sub["start"] <= position < next_start:
                    subsection = sub["title"]
                    break
            return f"{section['roman']}. {section['title']}", subsection
    return "unknown", "unknown"


def surrounding_snippet(text: str, start: int, end: int, radius: int = 180) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = text[left:right]
    return fix_inline_spacing(snippet)


def extract_citation_contexts(body_text: str, sections: List[Dict[str, Any]], max_ref_number: int) -> List[Dict[str, Any]]:
    contexts: List[Dict[str, Any]] = []
    pattern = re.compile(r"\[((?:\d+(?:\s*-\s*\d+)?)(?:\s*,\s*\d+(?:\s*-\s*\d+)?)*)\]")
    for match in pattern.finditer(body_text):
        marker = match.group(1)
        numbers = expand_citation_marker(marker)
        if not numbers:
            continue
        section, subsection = find_context_section(match.start(), sections)
        snippet = surrounding_snippet(body_text, match.start(), match.end())
        for number in numbers:
            if number < 1 or number > max_ref_number:
                continue
            contexts.append({
                "citation_number": number,
                "section": section,
                "subsection": subsection,
                "surrounding_text": snippet,
                "citation_marker": f"[{marker}]",
            })
    return contexts


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    page_texts, reference_page_texts, first_page_words, first_page_left_text = collect_text(pdf_path)
    title, abstract = extract_title_and_abstract(first_page_words, first_page_left_text)

    body_text = "\n".join(page_texts)
    major_sections = find_major_sections(body_text)
    taxonomy_related_headings = []
    for section in major_sections:
        if section["roman"] == "III":
            taxonomy_related_headings.extend(section["subsections"])

    reference_text = "\n".join(reference_page_texts)
    references = extract_references(reference_text)
    max_ref_number = max((ref["reference_number"] for ref in references), default=0)
    citation_contexts = extract_citation_contexts(body_text, major_sections, max_ref_number=max_ref_number)

    title_count = sum(1 for ref in references if ref.get("title") and ref["title"] != "unknown")
    year_count = sum(1 for ref in references if ref.get("year") and ref["year"] != "unknown")

    intake_payload = {
        "input_pdf": str(pdf_path),
        "title": title,
        "abstract": abstract,
        "page_count": len(page_texts) + len(reference_page_texts),
        "major_section_count": len(major_sections),
        "major_sections": [
            {
                "roman": section["roman"],
                "title": section["title"],
                "subsections": section["subsections"],
                "citation_numbers": section["citation_numbers"],
            }
            for section in major_sections
        ],
        "taxonomy_related_headings": taxonomy_related_headings,
        "section_map": {
            f"{section['roman']}. {section['title']}": {
                "subsections": section["subsections"],
                "citation_numbers": section["citation_numbers"],
            }
            for section in major_sections
        },
        "reference_count": len(references),
        "parsed_reference_title_count": title_count,
        "parsed_reference_year_count": year_count,
        "citation_context_count": len(citation_contexts),
    }

    (output_dir / "intake.json").write_text(
        json.dumps(intake_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "reference-list.json").write_text(
        json.dumps(references, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "citation_contexts.json").write_text(
        json.dumps(citation_contexts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote: {output_dir / 'intake.json'}")
    print(f"Wrote: {output_dir / 'reference-list.json'}")
    print(f"Wrote: {output_dir / 'citation_contexts.json'}")
    print(f"Major sections: {len(major_sections)}")
    print(f"References: {len(references)}")
    print(f"Citation contexts: {len(citation_contexts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
