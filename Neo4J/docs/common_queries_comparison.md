The **common_queries_comparison.md** file should include a detailed comparison of the common queries between the two parts of your project: the **Redshift-based data warehouse analysis** and the **Neo4j-based graph database analysis**. Here's a suggested structure for the file:

---

# **Common Queries Comparison**

This document compares the common queries used across both the Redshift-based data warehouse and Neo4j graph database analysis. The comparison highlights the differences in query syntax, performance considerations, and how the same analytical tasks are approached using these two different technologies.

---

### **1. Overview**

Provide a brief overview of the purpose of the comparison. Explain that the goal is to compare how similar analytical tasks (e.g., aggregating data, joining tables, and filtering records) are handled differently in **Redshift (SQL)** and **Neo4j (Cypher)**.

---

### **2. Query 1: FTP-Patator Attack Frequency by Source Details**

**Redshift Query:**

```sql
SELECT s.source_ip, s.source_port, f.Label, COUNT(*)
FROM source_dim s
JOIN fact_table f ON s.surrogate_key = f.Source_ID_FK
GROUP BY s.source_ip, s.source_port, f.Label
HAVING f.Label = 'FTP-Patator';
```

**Neo4j Query:**

```cypher
MATCH (s:Source)-[r:ATTACK_INITATED]->(l:Label)
WHERE l.Label_Name = 'FTP-Patator'
RETURN s.Source_IP, s.Source_Port, COUNT(r)
```

**Explanation**:
- **Redshift** uses a standard SQL `JOIN` and `GROUP BY` operation to count the occurrences of a particular label for each source IP.
- **Neo4j** utilizes a `MATCH` query to find the nodes and relationships, then applies a `WHERE` clause to filter based on the label. The `COUNT(r)` function returns the number of relationships for the given label.

---

### **3. Query 2: Retrieving Top Source IP by Event Count for Each Label**

**Redshift Query:**

```sql
WITH labelcount AS (
    SELECT s.source_ip, s.source_port, f.Label, COUNT(*) AS cnt,
           ROW_NUMBER() OVER (PARTITION BY f.Label ORDER BY cnt DESC) AS row_rank
    FROM source_dim s
    JOIN fact_table f ON s.surrogate_key = f.Source_ID_FK
    GROUP BY s.source_ip, s.source_port, f.Label
)
SELECT source_ip, source_port, Label, cnt AS Max_Count
FROM labelcount
WHERE row_rank = 1;
```

**Neo4j Query:**

```cypher
MATCH (s:Source)-[r:ATTACK_INITATED]->(l:Label)
WITH l.Label_Name AS label, s.Source_IP AS SourceIP, s.Source_Port AS SourcePort, COUNT(r) AS Total_Count
ORDER BY Total_Count DESC
LIMIT 1
RETURN label, SourceIP, SourcePort, Total_Count AS Max_Count
```

**Explanation**:
- **Redshift** uses a window function `ROW_NUMBER()` to rank the source IPs for each label based on their event count, returning the top source IPs.
- **Neo4j** uses a `MATCH` query to find the sources and their associated labels, counting the occurrences of the `ATTACK_INITATED` relationships. It then orders the results by event count and limits the output to the top result.

---

### **4. Query 3: Identify Top 3 Destination IPs with Highest Traffic Count for Each Label**

**Redshift Query:**

```sql
with denserankcount as (
select d.destination_ip,f.Label,count(*) as Total_Count,dense_rank() over(partition by f.Label order by Total_Count desc) 
from dest_dim as d join fact_table as f on f.Dest_IP_FK=d.surrogate_key group by d.destination_ip,f.Label)

select destination_ip,Label,Total_Count from denserankcount where dense_rank<=3;

```

**Neo4j Query:**

```cypher
match(l:Label)-[r:ATTACKED]->(d:Destination)
with l.Label_Name as label,collect({Destination_IP:d.Destination_IP,Destination_Port:d.Destination_Port,EventCount:r.Count}) as collect_stats
unwind(collect_stats) as unwind_stats
with label,unwind_stats
order by unwind_stats.EventCount DESC
with label,collect(unwind_stats)[0..3] as final_combined_stats
UNWIND final_combined_stats AS top_stats
RETURN label, top_stats.Destination_IP, top_stats.EventCount;
```
**Explanation:**
**Redshift Query:**
The Redshift query uses a WITH clause to create a temporary result set (denserankcount) that computes the total count of attacks (COUNT(*)) for each destination IP grouped by attack label (Label).
It then applies a DENSE_RANK() window function to rank the destination IPs for each label based on their attack count in descending order.
Finally, it filters the results to return the top 3 destination IPs (where dense_rank <= 3) for each label.

**Neo4j Query:**
The Neo4j query begins by matching the Label and Destination nodes with the ATTACKED relationship.
It uses collect() to aggregate the destination IP, port, and attack count into a list for each label.
The UNWIND function is then used to break this list into individual records.
The results are ordered by the attack count (EventCount) in descending order.
It uses collect(unwind_stats)[0..3] to retrieve the top 3 destination nodes by attack count.
Finally, it returns the label along with the top 3 destination IPs and their corresponding attack counts.


### **5. Query 4: Average Packet Details for each attack type**

**Redshift Query:**

```sql
SELECT f.Label, AVG(p.Average_Packet_Size)
FROM fact_table f
JOIN packet_dim p ON p.surrogate_key = f.Packet_FK
GROUP BY f.Label;
```

**Neo4j Query:**

```cypher
MATCH (p:Packet)-[r:CLASSIFIED_AS]->(l:Label)
WITH l.Label_Name AS label, AVG(p.Average_Packet_Size) AS Average_Packet_Size
RETURN label, Average_Packet_Size;
```

**Explanation**:
- **Redshift** calculates the average packet size by joining the `fact_table` and `packet_dim` tables and grouping the results by label.
- **Neo4j** calculates the average packet size using `MATCH` and `WITH` clauses to group by label and apply the `AVG` function to the packet data.

---

# Query Performance Comparison

Below is a comparison of query execution times between Redshift and Neo4j for similar queries.

| Query Number | Redshift Time (Milliseconds) |Graph Time (Milliseconds) |
|--------------|------------------------------|--------------------------|
| 1            | 286                          | 32                       |
| 2            | 850                          | 3914                     |
| 3            | 473                          | 429                      |
| 4            | 4000                         | 326                      |

### Notes:
- Execution times may vary depending on the dataset size and infrastructure.
- The table above compares query execution times for similar queries executed on Redshift and Neo4j.

---

This **common_queries_comparison.md** file will provide a clear, structured way to showcase how both **Redshift** and **Neo4j** approach similar analytical tasks differently, while also addressing the performance and optimization strategies used in both cases.
