import pytest

from tartiflette import Engine, Resolver


@Resolver("Query.viewer", schema_name="test_issue72_1")
async def resolver_query_viewer(*_, **__):
    return {
        "viewer": {
            "name": "N1",
            "stats": {
                "views": {
                    "total": 1
                }
            }
        }
    }


_TTFTT_ENGINE = Engine("""
    type UserStatsViews {
      total: Int
    }
    
    type UserStats {
      views: UserStatsViews
    }
    
    type User {
      name: String
      stats: UserStats
    }
    
    type Query {
      viewer: User
    }
    """,
    schema_name="test_issue72_1",
)


@pytest.mark.asyncio
async def test_issue71_raw():
    query = """
    query {
      viewer {
        name
        stats {
          views {
            total
            unknownField4
          }
          unknownField3
        }
        unknownField2
      }
      unknownField1
    }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "field `UserStatsViews.unknownField4` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "stats",
                    "views",
                    "unknownField4"
                ],
                "locations": [
                    {
                        "line": 8,
                        "column": 13
                    }
                ]
            },
            {
                "message": "field `UserStats.unknownField3` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "stats",
                    "unknownField3"
                ],
                "locations": [
                    {
                        "line": 10,
                        "column": 11
                    }
                ]
            },
            {
                "message": "field `User.unknownField2` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "unknownField2"
                ],
                "locations": [
                    {
                        "line": 12,
                        "column": 9
                    }
                ]
            },
            {
                "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                "path": [
                    "unknownField1"
                ],
                "locations": [
                    {
                        "line": 14,
                        "column": 7
                    }
                ]
            }
        ]
    }


@pytest.mark.asyncio
async def test_issue71_fragment():
    query = """
    fragment UserStatsViewsFields on UserStatsViews {
      total
      unknownField4
    }
    
    fragment UserStatsFields on UserStats {
      views {
        ...UserStatsViewsFields
      }
      unknownField3
    }
    
    fragment UserFields on User {
      name
      stats {
        ...UserStatsFields
      }
      unknownField2
    }
    
    query {
      viewer {
        ...UserFields
      }
      unknownField1
    }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "field `UserStatsViews.unknownField4` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "stats",
                    "views",
                    "unknownField4"
                ],
                "locations": [
                    {
                        "line": 4,
                        "column": 7
                    }
                ]
            },
            {
                "message": "field `UserStats.unknownField3` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "stats",
                    "unknownField3"
                ],
                "locations": [
                    {
                        "line": 11,
                        "column": 7
                    }
                ]
            },
            {
                "message": "field `User.unknownField2` was not found in GraphQL schema.",
                "path": [
                    "viewer",
                    "unknownField2"
                ],
                "locations": [
                    {
                        "line": 19,
                        "column": 7
                    }
                ]
            },
            {
                "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                "path": [
                    "unknownField1"
                ],
                "locations": [
                    {
                        "line": 26,
                        "column": 7
                    }
                ]
            }
        ]
    }
