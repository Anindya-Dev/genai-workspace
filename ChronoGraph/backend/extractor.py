"""
Knowledge Graph Extractor.

Responsible for converting UnifiedDocument objects
into graph entities and relationships using an LLM.
"""
import json

from backend.normalizer import UnifiedDocument
from backend.schema import (
    EntityType,
    RelationshipType,
    GraphEntity,
    GraphRelationship,
    GraphExtractionResult,
)

from groq import Groq

from backend.config import GROQ_API_KEY

class GraphExtractor:
    """
    Extracts graph triples from normalized documents.
    """

    def __init__(self):
        """
        Initialize the graph extractor.

        TODO:
        - Configure LlamaIndex extraction pipeline
        """

        self.client = Groq(api_key=GROQ_API_KEY)

        self.model = "llama-3.3-70b-versatile"

    def extract(self, document: UnifiedDocument) -> GraphExtractionResult:
        """
        Extract graph entities and relationships
        from a normalized document.

        Returns:
            GraphExtractionResult
        """

        # Build prompt
        prompt = self._build_prompt(document)

        # Send prompt to the LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        llm_output = response.choices[0].message.content.strip()

        if llm_output.startswith("```"):
            llm_output = llm_output.strip("`")

            if llm_output.startswith("json"):
                llm_output = llm_output[4:]

            llm_output = llm_output.strip()

        # Print the raw JSON returned by the LLM
        print(json.dumps(json.loads(llm_output), indent=2))

        # Parse response
        result = self._parse_response(llm_output)

        # Validate result
        result = self._validate_result(result)

        return result

    def _build_prompt(self, document: UnifiedDocument) -> str:
        return f"""
        You are an enterprise knowledge graph extraction system.

        Extract:

        Entities:
        - Person
        - Technology
        - Organization
        - Concept
        - Project

        Relationships:
        - ADVOCATED_FOR
        - ARGUED_AGAINST
        - MIGRATED_FROM
        - MIGRATED_TO
        - COMMITTED_CODE
        - WORKS_ON

        Return ONLY a valid JSON object.

        Do not include:
        - Markdown
        - Triple backticks
        - Explanations
        - Comments
        - Any text before or after the JSON

        The response must begin with '{' and end with '}'.

        Use this exact structure:

        {{
        "entities": [
            {{
            "id": "...",
            "name": "...",
            "type": "Person"
            }}
        ],
        "relationships": [
            {{
            "source": "...",
            "target": "...",
            "type": "WORKS_ON",
            "confidence": 0.95
            }}
        ]
        }}

        Document:
        {document.content}
        """

    def _parse_response(self, response: str) -> GraphExtractionResult:
        """
        Parse the JSON response from the LLM into graph objects.

        Args:
            response: JSON string returned by the LLM.

        Returns:
            GraphExtractionResult containing extracted entities and relationships.
        """
        raise NotImplementedError("LLM response parsing will be implemented after the response schema is finalized.")

    def _validate_result(
        self,
        result: GraphExtractionResult
    ) -> GraphExtractionResult:
        """Validate extracted entities and relationships."""
        raise NotImplementedError