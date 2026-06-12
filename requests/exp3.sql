SELECT c.contract_reg_num,
    COUNT (DISTINCT s.agg_key_id) AS stages_count
FROM t_team_amkld.contracts_docs_<tier> c
    LEFT JOIN t_team_amkld.stages s ON c.contract_reg_num = s.contract_reg_num
GROUP BY c.contract_reg_num
ORDER BY stages_count DESC