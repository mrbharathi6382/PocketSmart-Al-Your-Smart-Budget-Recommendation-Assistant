import json
from google import genai
from google.genai import types
from ..config import get_settings
from ..schemas import RecommendationResponse

settings = get_settings()

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None
    def generate(self, planner_type, payload, image_bytes=None, image_mime=None):
        if not self.client: raise RuntimeError("Gemini API key is not configured")
        contents = [self._prompt(planner_type, payload)]
        if image_bytes and image_mime:
            contents += [types.Part.from_bytes(data=image_bytes, mime_type=image_mime),
                         "Use the uploaded outfit image only for visible style/color cues. Do not identify the person or infer sensitive attributes."]
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(temperature=0.35, max_output_tokens=5000, response_mime_type="application/json"),
        )
        raw = (response.text or "").strip()
        if not raw: raise RuntimeError("Gemini returned an empty response")
        try: data = json.loads(raw)
        except json.JSONDecodeError:
            start, end = raw.find("{"), raw.rfind("}")
            if start < 0 or end <= start: raise
            data = json.loads(raw[start:end+1])
        data["source"] = "gemini"
        return RecommendationResponse.model_validate(data)
    def _prompt(self, planner_type, payload):
        return f'''You are PocketSmart AI, a practical budget-aware recommendation assistant.\nPlanner: {planner_type}\nUser input:\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n\nReturn ONLY JSON with: title, summary, budget, currency, total_estimated, remaining_budget, budget_allocations (category, amount, percentage, note), recommendations (name, category, estimated_price, currency, platform, reason, search_url, priority), tips.\nRules: stay within budget; estimated prices are planning estimates, not live prices; never claim stock; use relevant platforms; create search URLs; be concise; for an uploaded image discuss only visible outfit style/colors; do not identify the person.'''

gemini_service = GeminiService()
