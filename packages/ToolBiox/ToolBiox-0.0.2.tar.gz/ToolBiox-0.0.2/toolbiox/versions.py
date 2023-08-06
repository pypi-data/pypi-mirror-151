def get_versions():
    return versions[0]["number"]


versions = [
    {
        "number": "0.0.2",
        "features": [
            "1. Get rid of the dependency on scikit-bio",
        ],
    },
    {
        "number": "0.0.1",
        "features": [
            "1. Separate the tools, libraries and api parts from the original Genome_work_tools and become ToolBiox",
        ],
    },
]