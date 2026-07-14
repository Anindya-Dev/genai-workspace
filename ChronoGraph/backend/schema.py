"""
Graph schema definitions for ChronoGraph.

Defines all supported entity types and relationship types
used during knowledge graph extraction.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class EntityType(str, Enum):
    PERSON = "Person"
    TECHNOLOGY = "Technology"
    ORGANIZATION = "Organization"
    CONCEPT = "Concept"
    PROJECT = "Project"


class RelationshipType(str, Enum):
    ADVOCATED_FOR = "ADVOCATED_FOR"
    ARGUED_AGAINST = "ARGUED_AGAINST"
    MIGRATED_FROM = "MIGRATED_FROM"
    MIGRATED_TO = "MIGRATED_TO"
    COMMITTED_CODE = "COMMITTED_CODE"
    WORKS_ON = "WORKS_ON"



@dataclass
class GraphEntity:
    """
    Represents an entity extracted from enterprise documents.

    Attributes:
        id: Unique identifier for the entity.
        name: Human-readable entity name.
        type: Entity category.
    """

    id: str
    name: str
    type: EntityType


@dataclass
class GraphRelationship:
    """
    Represents a semantic relationship between two graph entities.

    Attributes:
        source: Source entity ID.
        target: Target entity ID.
        type: Relationship type.
        document_id: Source document from which the relationship was extracted.
        timestamp: Timestamp of the source document.
        confidence: Confidence score assigned by the extraction pipeline.
    """

    source: str
    target: str
    type: RelationshipType

    document_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    confidence: float = 1.0


@dataclass
class GraphExtractionResult:
    """
    Container for the output of the graph extraction process.

    Attributes:
        entities: Extracted graph entities.
        relationships: Extracted graph relationships.
    """

    entities: list[GraphEntity] = field(default_factory=list)
    relationships: list[GraphRelationship] = field(default_factory=list)