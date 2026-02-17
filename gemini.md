# Project Constitution: Gemini (B.L.A.S.T. Protocol)

## Protocol 0: Discovery Questions (Step 1)
### North Star
Build a beautiful, interactive AI News Dashboard aggregating articles from newsletters (Ben's Bites, The AI Rundown) every 24 hours.

### Integrations
- **Source**: `https://www.bensbites.com/archive`, `https://www.therundown.ai/archive`
- **Destination**: Local JSON (Phase 1), Supabase (Phase 5)
- **Notifications**: None initially.

### Source of Truth
- **Primary**: The website's internal database (initially local JSON).
- **Secondary**: Newsletter archives.

### Delivery Payload
- **Format**: JSON Array of Article Objects.
- **Location**: `data/articles.json` (Local) -> Supabase (Production).
- **Frequency**: Every 24 hours.

### Behavioral Rules
- **Data-First**: Schema must be defined before coding.
- **Deterministic**: Standardized outputs.
- **Resilience**: Handle network failures with retries.
- **Aesthetic**: "Gorgeous", "Interactive", "Beautiful" UI (Phase 4).

## Data Schemas (Step 2)
```json
{
  "articles": [
    {
      "id": "uuid",
      "title": "string",
      "url": "string",
      "source": "string", // "BensBites" | "TheRundown"
      "published_at": "ISO8601",
      "summary": "string",
      "tags": ["string"],
      "saved": "boolean"
    }
  ],
  "metadata": {
    "last_run": "ISO8601",
    "status": "success"
  }
}
```

## Architectural Invariants
- **Layer 1 (Architecture)**: Logic defined in `architecture/*.md` SOPs.
- **Layer 2 (Navigation)**: Agent routes tasks.
- **Layer 3 (Tools)**: Deterministic Python scripts in `tools/`.
- **Golden Rule**: If logic changes, update SOP *before* code.

