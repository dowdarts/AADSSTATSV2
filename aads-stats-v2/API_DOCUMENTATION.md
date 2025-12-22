# AADS Stats V2 - API Documentation

## Overview

The AADS Stats V2 platform provides both direct Supabase queries and custom PostgreSQL functions for data retrieval.

## Base Configuration

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

## 📊 Core Tables

### Players Table

**Read All Players**
```javascript
const { data, error } = await supabase
  .from('players')
  .select('*')
  .eq('is_active', true)
  .order('name')
```

**Get Single Player**
```javascript
const { data, error } = await supabase
  .from('players')
  .select('*')
  .eq('id', playerId)
  .single()
```

### Events Table

**Get All Events**
```javascript
const { data, error } = await supabase
  .from('events')
  .select('*')
  .order('event_number')
```

**Get Specific Event**
```javascript
const { data, error } = await supabase
  .from('events')
  .select(`
    *,
    winner:players (name)
  `)
  .eq('event_number', 1)
  .single()
```

### Matches Table

**Get Event Matches**
```javascript
const { data, error } = await supabase
  .from('matches')
  .select(`
    *,
    player_1:players!matches_player_1_id_fkey (name),
    player_2:players!matches_player_2_id_fkey (name),
    winner:players!matches_winner_id_fkey (name)
  `)
  .eq('event_id', eventId)
  .order('match_number')
```

**Get Round Robin Matches**
```javascript
const { data, error } = await supabase
  .from('matches')
  .select('*')
  .eq('event_id', eventId)
  .eq('phase', 'round_robin')
  .eq('group_name', 'A')  // or 'B'
```

**Get Knockout Matches**
```javascript
const { data, error } = await supabase
  .from('matches')
  .select('*')
  .eq('event_id', eventId)
  .in('phase', ['quarterfinal', 'semifinal', 'final'])
  .order('phase')
```

### Event Standings

**Get Event Standings**
```javascript
const { data, error } = await supabase
  .from('event_standings')
  .select(`
    *,
    players (name)
  `)
  .eq('event_id', eventId)
  .order('rank')
```

**Get Group Standings**
```javascript
const { data, error } = await supabase
  .from('event_standings')
  .select(`
    *,
    players (name)
  `)
  .eq('event_id', eventId)
  .eq('group_name', 'A')
  .order('rank')
```

### Series Leaderboard

**Get Full Leaderboard**
```javascript
const { data, error } = await supabase
  .from('series_leaderboard')
  .select(`
    *,
    players (name)
  `)
  .order('overall_rank')
```

**Get Top N Players**
```javascript
const { data, error } = await supabase
  .from('series_leaderboard')
  .select(`
    *,
    players (name)
  `)
  .order('overall_rank')
  .limit(10)
```

## 🔧 Custom Functions (RPC)

### get_player_stats

Get player statistics with filtering options.

**Parameters:**
- `p_player_id` (UUID): Player ID
- `p_filter` (string): Filter type - 'all', 'event_1', 'knockouts', 'series'

**JavaScript:**
```javascript
const { data, error } = await supabase.rpc('get_player_stats', {
  p_player_id: '123e4567-e89b-12d3-a456-426614174000',
  p_filter: 'series'  // 'all', 'event_1', 'knockouts', 'series'
})
```

**Python:**
```python
response = supabase.rpc('get_player_stats', {
    'p_player_id': '123e4567-e89b-12d3-a456-426614174000',
    'p_filter': 'series'
}).execute()
```

**Returns:**
```javascript
{
  player_name: "John Doe",
  total_matches: 25,
  total_wins: 18,
  total_losses: 7,
  legs_won: 95,
  legs_lost: 68,
  leg_difference: 27,
  average_3da: 85.5,
  highest_checkout: 170,
  total_180s: 12
}
```

### get_knockout_bracket

Get knockout bracket for an event.

**Parameters:**
- `p_event_id` (UUID): Event ID

**JavaScript:**
```javascript
const { data, error } = await supabase.rpc('get_knockout_bracket', {
  p_event_id: eventId
})
```

**Returns:**
```javascript
[
  {
    round: "quarterfinal",
    match_number: 1,
    player_1_name: "John Doe",
    player_2_name: "Jane Smith",
    player_1_score: 5,
    player_2_score: 3,
    winner_name: "John Doe"
  },
  // ... more matches
]
```

## 🔒 Admin-Only Operations

### Staging Matches

**Get Pending Staging Matches** (Admin Only)
```javascript
const { data, error } = await supabase
  .from('staging_matches')
  .select(`
    *,
    events (event_name, event_number)
  `)
  .eq('status', 'pending')
  .order('created_at', { ascending: false })
```

**Update Staging Match** (Admin Only)
```javascript
const { error } = await supabase
  .from('staging_matches')
  .update({
    player_1_name: 'Updated Name',
    player_1_average: 88.5
  })
  .eq('id', stagingMatchId)
```

**Approve Staging Match** (Use Python migration script)
```python
from scripts.data_migration import AADSDataMigration

migrator = AADSDataMigration(supabase_url, supabase_key)
result = migrator.approve_staging_match(staging_id)
```

### Create Match (Admin)

```javascript
const { data, error } = await supabase
  .from('matches')
  .insert({
    event_id: eventId,
    phase: 'round_robin',
    group_name: 'A',
    player_1_id: player1Id,
    player_2_id: player2Id,
    player_1_legs: 5,
    player_2_legs: 3,
    player_1_average: 85.5,
    player_2_average: 78.3,
    winner_id: player1Id,
    match_date: new Date().toISOString()
  })
```

### Create Event (Admin)

```javascript
const { data, error } = await supabase
  .from('events')
  .insert({
    event_number: 1,
    event_name: 'AADS Event 1 - January 2025',
    event_date: '2025-01-15',
    venue: 'Downtown Sports Bar',
    status: 'pending'
  })
```

### Create Player (Admin)

```javascript
const { data, error } = await supabase
  .from('players')
  .insert({
    name: 'John Doe',
    email: 'john@example.com'
  })
```

## 📈 Advanced Queries

### Player Match History

```javascript
const { data, error } = await supabase
  .from('matches')
  .select(`
    *,
    events (event_name, event_number),
    opponent:players!matches_player_2_id_fkey (name)
  `)
  .eq('player_1_id', playerId)
  .order('match_date', { ascending: false })
```

### Head-to-Head Record

```javascript
const { data, error } = await supabase
  .from('matches')
  .select('*')
  .or(`and(player_1_id.eq.${player1Id},player_2_id.eq.${player2Id}),and(player_1_id.eq.${player2Id},player_2_id.eq.${player1Id})`)
```

### Event Statistics

```javascript
// Total matches in event
const { count } = await supabase
  .from('matches')
  .select('*', { count: 'exact', head: true })
  .eq('event_id', eventId)

// Average 3DA across event
const { data } = await supabase
  .from('matches')
  .select('player_1_average, player_2_average')
  .eq('event_id', eventId)

const avgScore = data.reduce((acc, match) => 
  acc + match.player_1_average + match.player_2_average, 0
) / (data.length * 2)
```

### Top Performers

**Highest Average**
```javascript
const { data } = await supabase
  .from('series_leaderboard')
  .select(`
    *,
    players (name)
  `)
  .order('overall_3da', { ascending: false })
  .limit(10)
```

**Most 180s**
```javascript
const { data } = await supabase
  .from('series_leaderboard')
  .select(`
    *,
    players (name)
  `)
  .order('total_180s', { ascending: false })
  .limit(10)
```

**Highest Checkout**
```javascript
const { data } = await supabase
  .from('series_leaderboard')
  .select(`
    *,
    players (name)
  `)
  .order('highest_checkout', { ascending: false })
  .limit(10)
```

## 🔍 Search Operations

### Search Players by Name

```javascript
const { data, error } = await supabase
  .from('players')
  .select('*')
  .ilike('name', `%${searchTerm}%`)
  .limit(10)
```

### Filter Matches by Date Range

```javascript
const { data, error } = await supabase
  .from('matches')
  .select('*')
  .gte('match_date', startDate)
  .lte('match_date', endDate)
  .order('match_date')
```

## 📊 Real-time Subscriptions

### Listen to Match Updates

```javascript
const channel = supabase
  .channel('matches-changes')
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'matches'
  }, (payload) => {
    console.log('Match updated:', payload)
    // Refresh your UI
  })
  .subscribe()

// Cleanup
channel.unsubscribe()
```

### Listen to Leaderboard Changes

```javascript
const channel = supabase
  .channel('leaderboard-changes')
  .on('postgres_changes', {
    event: 'UPDATE',
    schema: 'public',
    table: 'series_leaderboard'
  }, (payload) => {
    console.log('Leaderboard updated:', payload)
  })
  .subscribe()
```

## 🔐 Authentication

### Sign In (Admin)

```javascript
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'admin@aads.com',
  password: 'your-password'
})
```

### Check Admin Status

```javascript
const { data: { user } } = await supabase.auth.getUser()

const { data: adminUser } = await supabase
  .from('admin_users')
  .select('role')
  .eq('email', user.email)
  .single()

const isAdmin = adminUser && adminUser.role
```

### Sign Out

```javascript
const { error } = await supabase.auth.signOut()
```

## 🚀 Performance Tips

### Use Select Specific Columns

Instead of `select('*')`, specify only needed columns:

```javascript
const { data } = await supabase
  .from('players')
  .select('id, name, series_average_3da')
```

### Use Pagination

```javascript
const pageSize = 20
const page = 1

const { data } = await supabase
  .from('matches')
  .select('*')
  .range((page - 1) * pageSize, page * pageSize - 1)
```

### Use Indexes

The schema includes indexes on commonly queried fields. Use them:
- `event_id` for filtering matches by event
- `player_1_id`, `player_2_id` for player matches
- `phase` for filtering by tournament phase

## 📝 Error Handling

```javascript
async function fetchPlayerStats(playerId) {
  try {
    const { data, error } = await supabase.rpc('get_player_stats', {
      p_player_id: playerId,
      p_filter: 'series'
    })
    
    if (error) throw error
    
    return data
  } catch (error) {
    console.error('Error fetching player stats:', error.message)
    return null
  }
}
```

## 🧪 Testing Queries

Use Supabase SQL Editor to test queries:

```sql
-- Test get_player_stats function
SELECT * FROM get_player_stats(
  '123e4567-e89b-12d3-a456-426614174000'::uuid,
  'series'
);

-- Test knockout bracket
SELECT * FROM get_knockout_bracket(
  'event-uuid-here'::uuid
);
```

## 📚 Additional Resources

- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript)
- [Supabase Python Client](https://supabase.com/docs/reference/python)
- [PostgreSQL Functions](https://www.postgresql.org/docs/current/plpgsql.html)
