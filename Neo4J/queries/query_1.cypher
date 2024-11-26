MATCH(s:Source)-[r:ATTACK_INITATED]->(l:Label)
where l.Label_Name='FTP-Patator'
RETURN s.Source_IP,s.Source_Port,l.Label_Name,r.count;
