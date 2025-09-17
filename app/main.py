import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session ## session will be used when program class curd 
from datetime import date 
from typing import Optional
from app import crud, schemas 
from database import SessionLocal ## retrives the shared SessionLocal to connect to SQLIte data base

api_description = """
                        This API provides read-only access to info from the SportsWorldCentral
                        (SWC) Fantasy Football API.
                        The endpoints are grouped into the following categories:
                        ## Analytics
                        Get information about the health of the API and counts of leagues, teams,
                        and players.

                        ## Player
                        You can get a list of NFL players, or search for an individual player by
                        player_id.


                        ## Scoring
                        You can get a list of NFL player performances, including the fantasy points
                        they scored using SWC league scoring.


                        ## Membership
                        Get information about all the SWC fantasy football leagues and the teams in
                        them.

                        ## fastapi construction with addition detials for OpenAPI Specificationapp
                        specficationapp= FastAPI(
                            description= api_description, 
                            title= "SportsWordCenter (SWC) Fantasy football API ",
                            version= "0.1"
                        )
"""




## fastapi contstruction with additional detials added for openAI specification
app=FastAPI(
    description= api_description, 
    title= "SportsWordCenter (SWC) Fantasy football API ",
    version= "0.1"
)

#dependency 
def get_db():
    db= SessionLocal()
    try:
        yield db 
    finally:
        db.close()

    
@app.get("/",
         summary="API health check", ## improved summary

         ## detailed descritption to help developers and ai use it correctly
         description="Returns a simple message confirming that the API is running correctly.", 

         ## improved response description 
         response_description="Health check status message",

         ## custom operation id to repalce auto-generated one 
         operation_id="get_api_health",

         ##tags to group related endpoints together in the documentation
         tags=["Analytics"])
async def root():
    return {"message": "This is an API health check (status:successful)"}


@app.get("/v0/players",
         response_model=list[schemas.Player],
         summary="Get a list of NFL players",
         description="""Retrieve players with optional filters such as first name, last name, 
         or last_changed_date.""",
         response_description="List of NFL player records",
         operation_id="get_players",
         tags=["Player"])
def read_players(skip: int = Query(0,   description= "The number of items to skip at the begining fo API call"),
                 limit: int = Query(100,  description= "The numbers of records to reutnr after skipped records"),
                 minimum_last_changed_date: date = Query(None, description= "Minimum date of changed that you want to records"),
                first_name: str = Query(None , description= "First name of the player you want to search"),
                 last_name: str = Query(None , description=""),
                 db: Session = Depends(get_db)):
    players = crud.get_players(db,
                               skip=skip,
                               limit=limit,
                               min_last_changed_date=minimum_last_changed_date,
                               first_name=first_name,
                               last_name=last_name)
    return players


@app.get("/v0/players/{player_id}",
         response_model=schemas.Player,
         summary="Get a player by player_id, which is internal to SWC",
         description="""If you have an SWC player_id from another API call 
         (such as `v0_get_players`), you can call this endpoint using that ID.""",
         response_description="One NFL player record",
         operation_id="get_player_by_id",
         tags=["Player"])

def read_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    return player


@app.get("/v0/performances/",
         response_model=list[schemas.Performance],
         summary="Get NFL player performances",
         description="""Retrieve performance data for NFL players, 
         including fantasy points scored. Supports pagination and filtering by last_changed_date.""",
         response_description="List of NFL player performance records",
         operation_id="get_performances",
         tags=["Scoring"])
def read_performance(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(100, description="Maximum number of records to return"),
        minimum_last_changed_date: Optional[date] = Query(None, description="Filter records updated on or after this date"),
        db: Session = Depends(get_db)
    ):
        
    performances = crud.get_performances(db,
                                         skip=skip,
                                         limit=limit,
                                         min_last_changed_date=minimum_last_changed_date)
    return performances


@app.get("/v0/leagues/{league_id}/",
         response_model=schemas.League,
         summary="Get a league by league_id",
         description="Retrieve details of a specific NFL league by its league_id.",
         response_description="One NFL league record",
         operation_id="get_league_by_id",
         tags=["Membership"])
def read_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="league not found")
    return league


@app.get("/v0/leagues/",
         response_model=list[schemas.League],
         summary="Get a list of NFL leagues",
         description="""Retrieve multiple leagues with optional filters 
         such as league_name or last_changed_date. Supports pagination.""",
         response_description="List of NFL league records",
         operation_id="get_leagues",
         tags=["Membership"])

def read_leagues(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    minimum_last_changed_data = Query(None, description="Filter records updated on or after this date"),
    league_name: str= Query(None, description="Filter leagues by name"),
    db: Session = Depends(get_db)
):



    leagues = crud.get_leagues(db,
                               skip=skip,
                               limit=limit,
                               min_last_changed_date=minimum_last_changed_data,
                               league_name=league_name)
    return leagues


@app.get("/v0/teams/",
         response_model=list[schemas.Team],
         summary="Get a list of NFL teams",
         description="""Retrieve multiple teams with optional filters such as team_name, 
         league_id, or last_changed_date. Supports pagination.""",
         response_description="List of NFL team records",
         operation_id="get_teams",
         tags=["Membership"])

def read_teams(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    minimum_last_changed_date: Optional[date] = Query(None, description="Filter records updated on or after this date"),
    team_name: str = Query(None, description="Filter teams by name"),
    league_id: int = Query(None, description="Filter teams by league ID"),
    db: Session = Depends(get_db)
):
    

    teams = crud.get_teams(db,
                           skip=skip,
                           limit=limit,
                           min_last_changed_date=minimum_last_changed_date,
                           team_name=team_name,
                           league_id=league_id)
    return teams


@app.get("/v0/counts/",
         response_model=schemas.Counts,
         summary="Get counts of leagues, teams, and players",
         description="Retrieve aggregated counts for leagues, teams, and players across the database.",
         response_description="Counts of leagues, teams, and players",
         operation_id="get_counts",
         tags=["Analytics"])
def get_count(db: Session = Depends(get_db)):
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count=crud.get_team_count(db),
        player_count=crud.get_player_count(db),
    )
    return counts