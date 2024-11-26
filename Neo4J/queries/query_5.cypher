MATCH (p:Packet)-[r:CLASSIFIED_AS]->(l:Label)
MATCH (pr:Protocol)-[r2:COMMONLY_ATTACKED_BY]->(l)
WITH l.Label_Name AS label, pr.Protocol_Name AS protocol, COUNT(r) AS Attack_Count
RETURN label, protocol, Attack_Count
ORDER BY Attack_Count DESC;
