def chatgptQuery():
    query = f"""query {{
                  search(query: "chat.openai.com/share in:file,commits,body is:pr is:merged",
                    type: ISSUE,
                    first: 10) {{ 
                        pageInfo {{
                            endCursor
                            hasNextPage
                        }}
                        issueCount
                        edges {{
                            node {{
                                ... on PullRequest {{                                    
                                    url
                                    title
                                    createdAt
                                    mergedAt
                                    state   
                                    repository {{
                                        stargazerCount
                                        isFork
                                        primaryLanguage {{
                                            name
                                        }}
                                    }}
                                    files (first: 100) {{
                                        edges {{
                                            node {{
                                                path
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}"""
    return query


def geminiQuery():
    query = f"""query {{
                  search(query: "g.co/gemini/share in:file,commits,body is:pr is:merged",
                    type: ISSUE,
                    first: 100) {{
                        pageInfo {{
                            endCursor
                            hasNextPage
                        }}
                        issueCount
                        edges {{
                            node {{
                                ... on PullRequest {{                                    
                                    url
                                    title
                                    createdAt
                                    mergedAt
                                    state   
                                    repository {{
                                        stargazerCount
                                        isFork
                                        primaryLanguage {{
                                            name
                                        }}
                                    }}
                                    files (first: 100) {{
                                        edges {{
                                            node {{
                                                path
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}"""
    return query
