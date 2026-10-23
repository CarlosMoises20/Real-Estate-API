from fastapi import APIRouter, HTTPException
from backend.common.constants import DATA_SOURCES, SERIES_SOURCES, DATA_DISCLAIMERS

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


"""
Build the source metadata of a column of the final dataset, combining SERIES_SOURCES with DATA_SOURCES
This must be attached to every value exposed by the API, so that the attribution reaches the API consumers

    column: name of the column in the final dataset (e.g. "InflationGrowthRate")
    retrieved_at: optional date when the data was retrieved from the source

"""
def get_series_source(column, retrieved_at=None):

    series = SERIES_SOURCES.get(column)

    if series is None:
        raise KeyError(f"Column '{column}' has no source metadata in SERIES_SOURCES")

    source = DATA_SOURCES[series["source"]]

    return {
        "name": source["name"],
        "attribution": source["attribution"],
        "license": source["license"],
        "license_url": source["license_url"],
        "url": source["url"],
        "series": series["series"],
        "derived": series["derived"],
        "transformation": series["transformation"],
        "retrieved_at": retrieved_at
    }


@router.get("/")
def get_sources():
    """List every data source, the source of each series and the disclaimers."""
    return {
        "sources": DATA_SOURCES,
        "series": {column: get_series_source(column) for column in SERIES_SOURCES},
        "disclaimers": DATA_DISCLAIMERS
    }


@router.get("/series/{column}")
def get_series(column: str):
    """Retrieve the source metadata of a column of the final dataset (e.g. 'InflationGrowthRate')."""
    try:
        return get_series_source(column)
    except KeyError:
        raise HTTPException(status_code=404, detail="Series not found")


@router.get("/{source_id}")
def get_source(source_id: str):
    """Retrieve a specific data source by ID (e.g. 'ine', 'ecb')."""
    if source_id not in DATA_SOURCES:
        raise HTTPException(status_code=404, detail="Source not found")
    return DATA_SOURCES[source_id]
