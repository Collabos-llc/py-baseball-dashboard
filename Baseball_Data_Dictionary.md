# ⚾ Complete Baseball Data Dictionary - PyBaseball Statcast Data

## 🎯 Your Data Advantage
**UmpScorecards Uses:** 5 basic columns  
**You Have Access To:** 118+ columns of MLB Statcast data

This comprehensive data dictionary explains every data point available through PyBaseball, giving you a massive competitive advantage for baseball analysis and betting.

---

## 📊 BASIC GAME INFORMATION

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `game_date` | Date of the game (YYYY-MM-DD) | Schedule analysis, trends |
| `game_year` | Year of the game | Season-long trends |
| `game_pk` | Unique game identifier | Game tracking |
| `game_type` | Type of game (R=Regular, P=Playoffs, etc.) | Stakes analysis |
| `home_team` | Home team abbreviation | Home field advantage |
| `away_team` | Away team abbreviation | Travel fatigue analysis |
| `home_score` | Home team score at time of pitch | Game situation |
| `away_score` | Away team score at time of pitch | Game situation |
| `post_home_score` | Home score after the play | Scoring impact |
| `post_away_score` | Away score after the play | Scoring impact |
| `bat_score` | Batting team score | Situational pressure |
| `fld_score` | Fielding team score | Defensive pressure |
| `post_bat_score` | Batting team score after play | Play impact |
| `post_fld_score` | Fielding team score after play | Play impact |

---

## ⚾ PITCH CHARACTERISTICS

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `pitch_type` | Type of pitch (FF, SL, CH, etc.) | Pitch sequencing |
| `pitch_name` | Full name of pitch type | Pitcher analysis |
| `release_speed` | Speed of pitch when released (mph) | Pitcher fatigue/health |
| `effective_speed` | Perceived speed based on extension | Batter difficulty |
| `release_pos_x` | Horizontal release point (feet) | Pitcher mechanics |
| `release_pos_y` | Distance from home plate at release | Extension analysis |
| `release_pos_z` | Vertical release point (feet) | Arm slot analysis |
| `release_extension` | How far pitcher extends toward plate | Deception factor |
| `release_spin_rate` | Spin rate at release (RPM) | Pitch movement |
| `spin_axis` | Axis of ball rotation (degrees) | Break direction |
| `spin_dir` | Direction of spin (deprecated) | Legacy metric |
| `spin_rate_deprecated` | Old spin rate measurement | Legacy metric |

---

## 🎯 PITCH LOCATION & STRIKE ZONE

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `plate_x` | Horizontal position at home plate (feet) | **Strike zone analysis** |
| `plate_z` | Vertical position at home plate (feet) | **Strike zone analysis** |
| `sz_top` | Top of batter's strike zone (feet) | **Ump tendencies** |
| `sz_bot` | Bottom of batter's strike zone (feet) | **Ump tendencies** |
| `zone` | Strike zone location (1-14) | **UmpScorecards style** |
| `type` | Result of pitch (S=Strike, B=Ball, X=InPlay) | **Call analysis** |
| `description` | Detailed pitch result | **Ump accuracy** |
| `des` | Play description text | Context |

---

## 🚀 BATTED BALL DATA (HUGE BETTING EDGE)

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `launch_speed` | Exit velocity (mph) | **Hit quality predictor** |
| `launch_angle` | Launch angle (degrees) | **Home run probability** |
| `hit_distance_sc` | Distance ball traveled (feet) | **Power analysis** |
| `hc_x` | Horizontal hit coordinate | **Spray chart analysis** |
| `hc_y` | Vertical hit coordinate | **Defensive positioning** |
| `hit_location` | Fielding position where ball went | **BABIP analysis** |
| `bb_type` | Batted ball type (ground_ball, line_drive, etc.) | **Expected outcomes** |

---

## 📈 EXPECTED STATISTICS (BETTING GOLDMINE)

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `estimated_ba_using_speedangle` | Expected batting average | **Value betting** |
| `estimated_woba_using_speedangle` | Expected weighted on-base average | **True performance** |
| `estimated_slg_using_speedangle` | Expected slugging percentage | **Power expectations** |
| `woba_value` | Actual weighted on-base average | **Compare to expected** |
| `woba_denom` | wOBA denominator | Statistical calculation |
| `babip_value` | Batting average on balls in play | **Luck factor** |
| `iso_value` | Isolated power (slugging - avg) | **Pure power metric** |
| `launch_speed_angle` | Launch speed + angle bucket | **Outcome probability** |

---

## 🎲 WIN PROBABILITY & LEVERAGE

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `delta_home_win_exp` | Change in home team win probability | **Live betting edge** |
| `delta_run_exp` | Change in expected runs | **Total betting** |
| `delta_pitcher_run_exp` | Impact on pitcher's run expectancy | **Pitcher performance** |
| `home_win_exp` | Home team win probability | **Game state** |
| `bat_win_exp` | Batting team win probability | **Leverage situations** |
| `home_score_diff` | Home team score differential | **Game flow** |
| `bat_score_diff` | Batting team score differential | **Momentum shifts** |

---

## 👥 PLAYER & MATCHUP DATA

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `player_name` | Name of the batter | Player identification |
| `batter` | Batter's player ID | Database linking |
| `pitcher` | Pitcher's player ID | Database linking |
| `stand` | Batter's handedness (L/R) | **Platoon advantages** |
| `p_throws` | Pitcher's handedness (L/R) | **Matchup analysis** |
| `umpire` | Home plate umpire name | **Ump tendencies** |

---

## 📊 GAME SITUATION

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `balls` | Ball count | **Count leverage** |
| `strikes` | Strike count | **Count leverage** |
| `outs_when_up` | Number of outs | **Situational pressure** |
| `inning` | Inning number | **Game progression** |
| `inning_topbot` | Top or bottom of inning | **Home field advantage** |
| `on_1b` | Runner on first base (player ID) | **RBI opportunities** |
| `on_2b` | Runner on second base (player ID) | **Scoring position** |
| `on_3b` | Runner on third base (player ID) | **High leverage** |
| `at_bat_number` | At-bat number in game | **Game flow** |
| `pitch_number` | Pitch number in at-bat | **Pitcher fatigue** |

---

## 🏃‍♂️ BASERUNNING & FIELDING

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `fielder_2` | Catcher player ID | Defensive alignment |
| `fielder_3` | First baseman player ID | Shift analysis |
| `fielder_4` | Second baseman player ID | Defensive positioning |
| `fielder_5` | Third baseman player ID | Hot corner defense |
| `fielder_6` | Shortstop player ID | Up-the-middle defense |
| `fielder_7` | Left fielder player ID | Outfield positioning |
| `fielder_8` | Center fielder player ID | Range analysis |
| `fielder_9` | Right fielder player ID | Arm strength |
| `if_fielding_alignment` | Infield alignment | **Shift analysis** |
| `of_fielding_alignment` | Outfield alignment | **Defensive strategy** |

---

## 🔬 ADVANCED PHYSICS DATA

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `vx0` | Initial velocity in x-direction | Physics modeling |
| `vy0` | Initial velocity in y-direction | Trajectory analysis |
| `vz0` | Initial velocity in z-direction | Ball flight path |
| `ax` | Acceleration in x-direction | Air resistance |
| `ay` | Acceleration in y-direction | Gravity effects |
| `az` | Acceleration in z-direction | Magnus force |
| `pfx_x` | Horizontal pitch movement (inches) | **Break analysis** |
| `pfx_z` | Vertical pitch movement (inches) | **Drop/rise** |

---

## ⏱️ FATIGUE & WORKLOAD METRICS

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `n_thruorder_pitcher` | Times through order for pitcher | **Fatigue analysis** |
| `n_priorpa_thisgame_player_at_bat` | Prior plate appearances this game | **Adjustment factor** |
| `pitcher_days_since_prev_game` | Days rest for pitcher | **Fresh vs tired** |
| `batter_days_since_prev_game` | Days rest for batter | **Rhythm analysis** |
| `pitcher_days_until_next_game` | Days until pitcher's next game | **Urgency factor** |
| `batter_days_until_next_game` | Days until batter's next game | **Rest motivation** |
| `age_pit` | Pitcher's age | **Decline curves** |
| `age_bat` | Batter's age | **Peak performance** |
| `age_pit_legacy` | Pitcher's age (legacy calc) | Historical data |
| `age_bat_legacy` | Batter's age (legacy calc) | Historical data |

---

## 🆕 CUTTING-EDGE METRICS

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `bat_speed` | Speed of bat through zone (mph) | **Contact quality** |
| `swing_length` | Length of bat's swing path | **Efficiency metric** |
| `hyper_speed` | Advanced speed calculation | **Next-gen metrics** |
| `attack_angle` | Bat's angle of attack | **Launch optimization** |
| `attack_direction` | Direction of bat attack | **Pull/opposite field** |
| `swing_path_tilt` | Tilt of swing plane | **Uppercut analysis** |
| `arm_angle` | Pitcher's arm angle | **Delivery mechanics** |
| `intercept_ball_minus_batter_pos_x_inches` | Bat-ball contact point X | **Contact precision** |
| `intercept_ball_minus_batter_pos_y_inches` | Bat-ball contact point Y | **Contact precision** |

---

## 🚫 LEGACY/DEPRECATED FIELDS

| Column | Description | Status |
|--------|-------------|---------|
| `break_angle_deprecated` | Old break angle measurement | Use pfx_x/pfx_z instead |
| `break_length_deprecated` | Old break length measurement | Use pfx_x/pfx_z instead |
| `tfs_deprecated` | Old timestamp | Use game_date |
| `tfs_zulu_deprecated` | Old UTC timestamp | Use game_date |
| `sv_id` | StatCast ID (deprecated) | Legacy identifier |

---

## 📈 API ENHANCEMENTS

| Column | Description | Betting Relevance |
|--------|-------------|-------------------|
| `api_break_z_with_gravity` | Gravity-adjusted vertical break | **True movement** |
| `api_break_x_arm` | Arm-side horizontal break | **Natural movement** |
| `api_break_x_batter_in` | Break toward/away from batter | **Batter comfort** |

---

## 🎯 KEY BETTING ADVANTAGES

### 1. **Strike Zone Analysis (Like UmpScorecards)**
- `plate_x`, `plate_z`, `sz_top`, `sz_bot`, `description`
- **Edge:** Identify umpire biases and call tendencies

### 2. **Expected vs Actual Performance**
- `estimated_woba_using_speedangle` vs `woba_value`
- **Edge:** Find overvalued/undervalued players

### 3. **Exit Velocity & Launch Angle**
- `launch_speed`, `launch_angle`, `hit_distance_sc`
- **Edge:** Predict home runs before they're obvious

### 4. **Win Probability Changes**
- `delta_home_win_exp`, `delta_run_exp`
- **Edge:** Live betting opportunities

### 5. **Pitcher Fatigue Indicators**
- `n_thruorder_pitcher`, `pitcher_days_since_prev_game`, `release_speed`
- **Edge:** Timing pitcher decline

### 6. **Defensive Positioning**
- `if_fielding_alignment`, `of_fielding_alignment`, `hit_location`
- **Edge:** BABIP and shift analysis

---

## 💡 CONTENT CREATION OPPORTUNITIES

1. **"The Hidden Stats UmpScorecards Doesn't Show You"**
2. **"Exit Velocity Leaders You've Never Heard Of"**
3. **"Umpire Bias Analysis Using 100+ Data Points"**
4. **"Pitcher Fatigue Indicators That Beat Vegas"**
5. **"Expected vs Actual: Finding Overvalued Players"**

---

## 🚀 GETTING STARTED

```python
import pybaseball as pyb

# Enable caching for faster queries
pyb.cache.enable()

# Get recent data
data = pyb.statcast('2024-07-01', '2024-07-10')

# See all 118+ columns
print(f"Total columns: {len(data.columns)}")
print(data.columns.tolist())
```

---

*This data dictionary represents your complete advantage over traditional baseball analytics. While others work with 5-10 basic stats, you have access to the same data that powers MLB front offices and the most sophisticated betting operations.*