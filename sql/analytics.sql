
-- QUERY 1: Total number of tickets
SELECT
    COUNT(*) AS total_tickets
FROM helpdesk_tickets;


-- QUERY 2: Tickets by status
SELECT
    status,
    COUNT(*) AS ticket_count
FROM helpdesk_tickets
GROUP BY status
ORDER BY ticket_count DESC;


-- QUERY 3: Tickets by priority
SELECT
    priority,
    COUNT(*) AS ticket_count
FROM helpdesk_tickets
GROUP BY priority
ORDER BY ticket_count DESC;


-- QUERY 4: Average resolution time by department
SELECT
    department,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM helpdesk_tickets
WHERE resolution_hours IS NOT NULL
GROUP BY department
ORDER BY avg_resolution_hours DESC;


-- QUERY 5: Technician workload
SELECT
    technician,
    COUNT(*) AS assigned_tickets,
    COUNT(*) FILTER (
        WHERE status IN ('Open', 'In Progress')
    ) AS unfinished_tickets
FROM helpdesk_tickets
GROUP BY technician
ORDER BY assigned_tickets DESC;
