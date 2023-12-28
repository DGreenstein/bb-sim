import pytest
from bbsim.main import BaseballSimulator

@pytest.fixture
def test_sim():
    return BaseballSimulator()

def test_pitch(test_sim):
    expected_values = ["Strike", "Ball", "Out", "Three strikes! Batter is out!", "Ball Four! Batter, takes your base.", "It's a single!", "It's a double!", "It's a triple!", "It's a home run!"]
    pitch_value = []
    pitch_value.append(test_sim.pitch())
    print(pitch_value)
    assert any(item in pitch_value for item in expected_values)

def test_single(test_sim):
    test_sim.run_bases('single')
    assert test_sim.bases == [1,0,0]

def test_double(test_sim):
    test_sim.run_bases('double')
    assert test_sim.bases == [0,1,0]

def test_triple(test_sim):
    test_sim.run_bases('triple')
    assert test_sim.bases == [0,0,1]
    
def test_solo_home_run(test_sim):
    test_runs = test_sim.run_bases('home_run')
    assert test_sim.bases == [0,0,0]
    assert test_runs == 1

def test_two_run_home_run(test_sim):
    for i in range(len(test_sim.bases)):
        test_sim.bases[i] = 1
        test_runs = test_sim.run_bases('home_run')
        assert test_runs == 2
        test_sim.runs_scored = 0

def test_three_run_home_run(test_sim):
    for i in range(len(test_sim.bases)):
        test_sim.bases = [1,1,1]
        test_sim.bases[i] = 0
        test_runs = test_sim.run_bases('home_run')
        assert test_runs == 3
        test_sim.runs_scored = 0

def test_grand_slam(test_sim):
    test_sim.bases = [1,1,1]
    test_runs = test_sim.run_bases('home_run')
    assert test_runs == 4

