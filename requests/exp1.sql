SELECT contract_reg_num,
    supplier_inn,
    customer_inn,
    price,
    dt_contract,
    status
FROM t_team_amkld.contracts_docs_<tier>
WHERE dt_contract >= ’ 2023 -01 -01 ’
    AND dt_contract < ’ 2023 -04 -01 ’
    AND status = 'Исполнение'