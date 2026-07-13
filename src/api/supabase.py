from typing import Union, Dict, Any, List, Optional, TypedDict, Literal
from typing_extensions import NotRequired

# Type alias for JSON values
Json = Union[
    str,
    int,
    float,
    bool,
    None,
    Dict[str, Union['Json', None]],
    List['Json']
]


class GraphQLArgs(TypedDict):
    extensions: NotRequired[Json]
    operationName: NotRequired[str]
    query: NotRequired[str]
    variables: NotRequired[Json]


class GraphQLFunction(TypedDict):
    Args: GraphQLArgs
    Returns: Json


class StudyRow(TypedDict):
    comments: Optional[str]
    created_at: str
    end_date: Optional[str]
    id: int
    name: str
    protocol_visits: int
    sponsor: str
    start_date: str


class StudyInsert(TypedDict, total=False):
    comments: Optional[str]
    created_at: str
    end_date: Optional[str]
    id: int
    name: str
    protocol_visits: int
    sponsor: str
    start_date: str


class StudyUpdate(TypedDict, total=False):
    comments: Optional[str]
    created_at: str
    end_date: Optional[str]
    id: int
    name: str
    protocol_visits: int
    sponsor: str
    start_date: str


class StudyTable(TypedDict):
    Row: StudyRow
    Insert: StudyInsert
    Update: StudyUpdate
    Relationships: List[Any]


class PublicSchema(TypedDict):
    Tables: Dict[Literal["study"], StudyTable]
    Views: Dict[str, Any]
    Functions: Dict[str, Any]
    Enums: Dict[str, Any]
    CompositeTypes: Dict[str, Any]


class GraphQLPublicSchema(TypedDict):
    Tables: Dict[str, Any]
    Views: Dict[str, Any]
    Functions: Dict[Literal["graphql"], GraphQLFunction]
    Enums: Dict[str, Any]
    CompositeTypes: Dict[str, Any]


class InternalSupabase(TypedDict):
    PostgrestVersion: Literal["14.5"]


class Database(TypedDict):
    __InternalSupabase: InternalSupabase
    graphql_public: GraphQLPublicSchema
    public: PublicSchema


# Constants
CONSTANTS = {
    "graphql_public": {
        "Enums": {},
    },
    "public": {
        "Enums": {},
    },
}
