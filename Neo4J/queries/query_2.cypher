MATCH(s:Source)-[r:ATTACK_INITATED]->(l:Label)
WITH l.Label_Name as label,collect({SourceIP:s.Source_IP,SourcePort:s.Source_Port,Event_Count:r.count}) as Stats
unwind(Stats) as unwind_stats
with label,unwind_stats
order by unwind_stats.Event_Count DESC
with label,collect(unwind_stats)[0] as top_source
return label,top_source.SourceIP as Source_IP,top_source.Event_Count as MaxCount;
