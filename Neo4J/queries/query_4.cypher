match(l:Label)-[r:ATTACKED]->(d:Destination)
with l.Label_Name as label,collect({Destination_IP:d.Destination_IP,Destination_Port:d.Destination_Port,EventCount:r.Count}) as collect_stats
unwind(collect_stats) as unwind_stats
with label,unwind_stats
order by unwind_stats.EventCount DESC
with label,collect(unwind_stats)[0..3] as final_combined_stats
UNWIND final_combined_stats AS top_stats
RETURN label, top_stats.Destination_IP, top_stats.EventCount;
