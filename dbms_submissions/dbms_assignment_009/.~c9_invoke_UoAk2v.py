Q1="select avg(age) from player;"
Q2="select match_no,play_date from match where audience>50000 order by match_no asc;"
Q3="select team_id,count(win_lose) from matchteamdetails where win_lose=='W' group by team_id  order by count(win_lose) desc,team_id asc;"
Q4="select match_no,play_date from "