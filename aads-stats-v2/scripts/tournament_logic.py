"""
AADS Tournament Logic Utilities
Handles ranking, seeding, and knockout bracket generation
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class Phase(Enum):
    """Tournament phases"""
    ROUND_ROBIN = "round_robin"
    QUARTERFINAL = "quarterfinal"
    SEMIFINAL = "semifinal"
    FINAL = "final"


@dataclass
class Player:
    """Player with stats"""
    id: str
    name: str
    wins: int = 0
    losses: int = 0
    legs_won: int = 0
    legs_lost: int = 0
    average_3da: float = 0.0
    
    @property
    def leg_difference(self) -> int:
        return self.legs_won - self.legs_lost


class TournamentLogic:
    """
    AADS Tournament Logic Engine
    Handles ranking and seeding according to AADS rules
    """
    
    @staticmethod
    def rank_round_robin_group(players: List[Player]) -> List[Player]:
        """
        Rank players in a Round Robin group according to AADS rules:
        1. Wins
        2. Leg Difference
        3. Head-to-Head (not implemented in this version)
        4. 3-Dart Average
        
        Args:
            players: List of Player objects
            
        Returns:
            Sorted list of players
        """
        return sorted(
            players,
            key=lambda p: (
                -p.wins,                    # More wins is better (negative for descending)
                -p.leg_difference,           # Better leg difference
                -p.average_3da               # Higher average
            )
        )
    
    @staticmethod
    def get_top_n(ranked_players: List[Player], n: int = 4) -> List[Player]:
        """
        Get top N players from ranked list
        
        Args:
            ranked_players: Already ranked list
            n: Number of players to return
            
        Returns:
            Top N players
        """
        return ranked_players[:n]
    
    @staticmethod
    def generate_knockout_seeding(group_a_ranked: List[Player], 
                                   group_b_ranked: List[Player]) -> List[Tuple[Player, Player]]:
        """
        Generate knockout bracket seeding using AADS crossover rules:
        - A1 vs B4
        - B2 vs A3
        - B1 vs A4
        - A2 vs B3
        
        Args:
            group_a_ranked: Top 4 from Group A (already ranked)
            group_b_ranked: Top 4 from Group B (already ranked)
            
        Returns:
            List of (player1, player2) tuples for quarterfinals
        """
        if len(group_a_ranked) < 4 or len(group_b_ranked) < 4:
            raise ValueError("Need top 4 from each group")
        
        # Get top 4 from each group
        a1, a2, a3, a4 = group_a_ranked[:4]
        b1, b2, b3, b4 = group_b_ranked[:4]
        
        # AADS Crossover Seeding
        quarterfinals = [
            (a1, b4),  # QF1
            (b2, a3),  # QF2
            (b1, a4),  # QF3
            (a2, b3)   # QF4
        ]
        
        return quarterfinals
    
    @staticmethod
    def generate_semifinal_seeding(qf_winners: List[Player]) -> List[Tuple[Player, Player]]:
        """
        Generate semifinal matchups from quarterfinal winners
        Standard bracket: QF1 winner vs QF2 winner, QF3 winner vs QF4 winner
        
        Args:
            qf_winners: List of 4 quarterfinal winners in order
            
        Returns:
            List of 2 semifinal matchups
        """
        if len(qf_winners) != 4:
            raise ValueError("Need exactly 4 quarterfinal winners")
        
        return [
            (qf_winners[0], qf_winners[1]),  # SF1: QF1 winner vs QF2 winner
            (qf_winners[2], qf_winners[3])   # SF2: QF3 winner vs QF4 winner
        ]
    
    @staticmethod
    def generate_toc_bracket(event_winners: List[Player]) -> Dict:
        """
        Generate Tournament of Champions bracket (Event 7)
        - 6 players (winners of Events 1-6)
        - Round Robin within single group
        - Top 4 advance to semifinals (1v4, 2v3)
        
        Args:
            event_winners: List of 6 event winners
            
        Returns:
            Dictionary with round robin and knockout structure
        """
        if len(event_winners) != 6:
            raise ValueError("Tournament of Champions requires exactly 6 players")
        
        # Generate Round Robin matchups (all vs all)
        rr_matches = []
        for i in range(len(event_winners)):
            for j in range(i + 1, len(event_winners)):
                rr_matches.append((event_winners[i], event_winners[j]))
        
        return {
            'round_robin_matches': rr_matches,
            'total_matches': len(rr_matches),
            'note': 'Top 4 advance to semifinals based on RR standings'
        }
    
    @staticmethod
    def generate_toc_semifinals(ranked_players: List[Player]) -> List[Tuple[Player, Player]]:
        """
        Generate ToC semifinal matchups (1v4, 2v3)
        
        Args:
            ranked_players: Top 4 from ToC Round Robin
            
        Returns:
            List of 2 semifinal matchups
        """
        if len(ranked_players) < 4:
            raise ValueError("Need top 4 players")
        
        return [
            (ranked_players[0], ranked_players[3]),  # 1 vs 4
            (ranked_players[1], ranked_players[2])   # 2 vs 3
        ]


class MatchGenerator:
    """Generate complete match schedules"""
    
    @staticmethod
    def generate_round_robin_schedule(group_players: List[Player]) -> List[Tuple[Player, Player]]:
        """
        Generate round robin schedule for a group
        Each player plays every other player once
        
        Args:
            group_players: List of players in the group
            
        Returns:
            List of (player1, player2) matchups
        """
        matches = []
        for i in range(len(group_players)):
            for j in range(i + 1, len(group_players)):
                matches.append((group_players[i], group_players[j]))
        return matches
    
    @staticmethod
    def generate_event_schedule(group_a: List[Player], group_b: List[Player]) -> Dict:
        """
        Generate complete event schedule (Events 1-6)
        
        Args:
            group_a: 5 players in Group A
            group_b: 5 players in Group B
            
        Returns:
            Dictionary with round robin and knockout phases
        """
        if len(group_a) != 5 or len(group_b) != 5:
            raise ValueError("Each group must have exactly 5 players")
        
        # Round Robin
        rr_a = MatchGenerator.generate_round_robin_schedule(group_a)
        rr_b = MatchGenerator.generate_round_robin_schedule(group_b)
        
        return {
            'round_robin': {
                'group_a': rr_a,
                'group_b': rr_b,
                'total_matches': len(rr_a) + len(rr_b)
            },
            'note': 'Top 4 from each group advance to quarterfinals with crossover seeding'
        }


def calculate_3dart_average(total_score: int, darts_thrown: int) -> float:
    """
    Calculate 3-dart average
    
    Args:
        total_score: Total score accumulated
        darts_thrown: Total darts thrown
        
    Returns:
        3-dart average
    """
    if darts_thrown == 0:
        return 0.0
    return round((total_score / darts_thrown) * 3, 2)


def main():
    """Example usage and testing"""
    
    # Example: Rank a Round Robin group
    group_a_players = [
        Player("p1", "Alice", wins=4, losses=0, legs_won=20, legs_lost=8, average_3da=85.5),
        Player("p2", "Bob", wins=3, losses=1, legs_won=18, legs_lost=10, average_3da=82.3),
        Player("p3", "Charlie", wins=2, losses=2, legs_won=15, legs_lost=15, average_3da=78.1),
        Player("p4", "Diana", wins=1, losses=3, legs_won=10, legs_lost=18, average_3da=75.5),
        Player("p5", "Eve", wins=0, losses=4, legs_won=5, legs_lost=20, average_3da=70.2)
    ]
    
    # Rank the group
    ranked = TournamentLogic.rank_round_robin_group(group_a_players)
    
    print("Group A Rankings:")
    for i, player in enumerate(ranked, 1):
        print(f"{i}. {player.name} - W: {player.wins}, L: {player.losses}, "
              f"Leg +/-: {player.leg_difference:+d}, 3DA: {player.average_3da}")
    
    # Get top 4
    top_4 = TournamentLogic.get_top_n(ranked, 4)
    print(f"\nTop 4 advancing: {[p.name for p in top_4]}")
    
    # Example: Generate knockout seeding
    group_b_players = [
        Player("p6", "Frank", wins=3, losses=1, legs_won=19, legs_lost=11, average_3da=83.0),
        Player("p7", "Grace", wins=3, losses=1, legs_won=17, legs_lost=12, average_3da=80.5),
        Player("p8", "Henry", wins=2, losses=2, legs_won=14, legs_lost=14, average_3da=77.8),
        Player("p9", "Iris", wins=2, losses=2, legs_won=13, legs_lost=15, average_3da=76.0),
        Player("p10", "Jack", wins=0, losses=4, legs_won=8, legs_lost=20, average_3da=72.1)
    ]
    
    ranked_b = TournamentLogic.rank_round_robin_group(group_b_players)
    
    # Generate quarterfinals
    qf_matches = TournamentLogic.generate_knockout_seeding(ranked, ranked_b)
    
    print("\nQuarterfinal Matchups (AADS Crossover):")
    for i, (p1, p2) in enumerate(qf_matches, 1):
        print(f"QF{i}: {p1.name} vs {p2.name}")


if __name__ == '__main__':
    main()
