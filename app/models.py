"""Defines the SQLAlchemy classe for fantasy DataBase """

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship 
from  database import Base #declarative base linking Python class to database table

class Player(Base):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, index=True)
    gsis_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    # One-to-many relationship: Player → Performance
    performances = relationship("Performance", back_populates="player")

    # Many-to-many relationship: Player ↔ Team
    teams = relationship(
        "Team", # many to many relationship with team
                # Player can join many teams; a team can have many players
    
        secondary="team_player", ## Uses the link table 'team_player' to store player-team pairs : 
                                 # Example: (player_id, team_id)

        back_populates="players" ## Allows Team to access its players (bi-directional)
                                #     # Example: team.players returns all players in the team
    )

class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Float, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    
    player_id = Column(Integer, ForeignKey("player.player_id")) ## links the columns to the player_id columns in the player table 
    player = relationship("Player", back_populates="performances")


class League(Base):
    __tablename__ = "league"
    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "team"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"))
    league = relationship("League", back_populates="teams")
    players = relationship("Player", secondary="team_player", back_populates="teams")


class TeamPlayer(Base):
    __tablename__ = "team_player"
    team_id = Column(Integer, ForeignKey("team.team_id"),
    primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.player_id"),
    primary_key=True, index=True)
    last_changed_date = Column(Date, nullable=False)





