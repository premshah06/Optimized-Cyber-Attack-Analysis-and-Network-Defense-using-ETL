MATCH(p:Packet)-[r:CLASSIFIED_AS]->(l:Label)
with l.Label_Name as label,avg(p.Average_Packet_Size) as Average
return label,Average;
