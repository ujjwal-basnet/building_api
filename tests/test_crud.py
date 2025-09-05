""" Testing SQLALchemy Helper function"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest 
from datetime import date 
from app import crud
from database import SessionLocal

## use a test date 4/1/2024 to test the main_last_changed_date
test_date= date(2024,4,1)

@pytest.fixture(scope="function")
def db_session():
    """Starts the database session and closes its when its done"""
    session= SessionLocal() 
    yield session 
    session.close() 


from datetime import date
import pytest
from app import crud

# Test date fixture

test_date= date(2024,4,1)

# Example DB session fixture (assuming you have one)
@pytest.fixture(scope="function")
def db_session():
    # setup: create a session, e.g., from SQLAlchemy
    from database import SessionLocal
    session = SessionLocal()
    yield session
    session.close()

# Tests

def test_get_player(db_session):
    """Test fetching a single player by ID"""
    player = crud.get_player(db_session, player_id=1001)
    assert player.player_id == 1001

def test_get_players(db_session):
    """Test fetching multiple players filtered by min_last_changed_date"""
    players = crud.get_players(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(players) == 1018

def test_get_players_by_name(db_session):
    """Test fetching players by first and last name"""
    players = crud.get_players(db_session, first_name="Bryce", last_name="Young")
    assert len(players) == 1
    assert players[0].player_id == 2009

def test_get_all_performances(db_session):
    """Test fetching all performances"""
    performances = crud.get_performances(db_session, skip=0, limit=18000)
    assert len(performances) == 17306

def test_get_new_performances(db_session):
    """Test fetching performances filtered by min_last_changed_date"""
    performances = crud.get_performances(db_session, skip=0, limit=18000, min_last_changed_date=test_date)
    # Example assertion (adjust according to expected count)
    assert len(performances) > 0

def test_get_player_count(db_session):
    """Test fetching the total player count"""
    player_count = crud.get_player_count(db_session)
    # Example assertion (adjust according to your data)
    assert player_count == 1018
