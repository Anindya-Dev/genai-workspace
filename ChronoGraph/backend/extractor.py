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



class GraphExtractor:
    """
    Extracts graph triples from normalized documents.
    """

    def __init__(self):
        """
        Initialize the graph extractor.

        TODO:
        - Initialize Groq client
        - Configure LlamaIndex extraction pipeline
        """
        pass

    def extract(self, document: UnifiedDocument) -> GraphExtractionResult:
        """
        Extract graph entities and relationships
        from a normalized document.

        Returns:
            GraphExtractionResult
        """
        prompt = self._build_prompt(document)

        # TODO: Send prompt to LLM
         # TODO: Parse response
        # TODO: Validate result

        return GraphExtractionResult()

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

        Return ONLY valid JSON.

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