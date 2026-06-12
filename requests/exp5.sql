SELECT contract_reg_num,
    TO_DATE (dt_contract, 'yyyy-MM-dd') AS dt_contract_d,
    TO_DATE (start_dt_contract, 'yyyy-MM-dd') AS start_d,
    TO_DATE (end_dt_contract, 'yyyy-MM-dd') AS end_d,
    TO_DATE (dt_signing, 'yyyy-MM-dd') AS signing_d,
    TO_DATE (termination_dt, 'yyyy-MM-dd') AS termination_d
FROM t_team_amkld.contracts_docs_<tier>