SELECT contract_reg_num,
    regexp_extract (
        docs_done_stage,
        '(\\d{4}-\\d{2}-\\d{2})',
        1
    ) AS extracted_date
FROM t_team_amkld.contracts_docs_<tier>
WHERE docs_done_stage IS NOT NULL