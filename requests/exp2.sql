SELECT c.contract_reg_num,
    COUNT (s.subcontractor_inn) AS subcontractor_count
FROM t_team_amkld.contracts_docs_<tier> c
    LEFT JOIN t_team_amkld.subcontractors s ON c.contract_reg_num = s.contract_reg_num
GROUP BY c.contract_reg_num