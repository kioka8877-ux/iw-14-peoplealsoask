"""
IW-14 PeopleAlsoAsk — PAA + Related Searches Extractor
Iron Warrior #14 — Content research, questions.
"""
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import sys
sys.path.insert(0, '/home/user/iron_warriors/shared')
from base import create_app, fetch_html, clean_text, get_timestamp, measure_latency
import time

app = create_app("IW-14 PeopleAlsoAsk", "People Also Ask + related searches — content research")

class PAAQuestion(BaseModel):
    question: str
    answer: Optional[str] = None
    source_url: Optional[str] = None

class PAAResponse(BaseModel):
    query: str
    engine: str
    people_also_ask: List[PAAQuestion]
    related_searches: List[str]
    timestamp: str
    latency_ms: int

@app.get("/extract", response_model=PAAResponse)
async def extract_paa(
    q: str = Query(..., description="Search query"),
    gl: str = Query("us"),
    hl: str = Query("en"),
):
    start = time.time()
    url = f"https://www.google.com/search?q={quote_plus(q)}&gl={gl}&hl={hl}"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Google fetch failed: {e}")

    soup = BeautifulSoup(html, 'html.parser')
    paa = []

    # People Also Ask
    for pa_div in soup.find_all('div', class_='related-question-pair'):
        q_tag = pa_div.find('span', class_='CSY3tc') or pa_div.find('div', class_='JlqpRe')
        if q_tag:
            question = clean_text(q_tag.get_text())
            # Try to find answer snippet
            answer_tag = pa_div.find('div', class_='mod') or pa_div.find('div', class_='kCrYT')
            source_tag = pa_div.find('a', href=True)
            paa.append(PAAQuestion(
                question=question,
                answer=clean_text(answer_tag.get_text()) if answer_tag else None,
                source_url=source_tag['href'] if source_tag and source_tag.get('href', '').startswith('http') else None,
            ))

    # Fallback PAA via JS data
    if not paa:
        for span in soup.find_all('span', class_='CSY3tc'):
            question = clean_text(span.get_text())
            if question and not any(p.question == question for p in paa):
                paa.append(PAAQuestion(question=question))

    # Related searches
    related = []
    for rs in soup.find_all('a', class_='fl'):
        related.append(clean_text(rs.get_text()))
    if not related:
        for rs in soup.find_all('p', class_='BBwThe'):
            related.append(clean_text(rs.get_text()))
    if not related:
        for rs in soup.find_all('div', class_='BjW0mf'):
            related.append(clean_text(rs.get_text()))

    return PAAResponse(
        query=q, engine="google",
        people_also_ask=paa[:20], related_searches=related[:20],
        timestamp=get_timestamp(), latency_ms=measure_latency(start),
    )
