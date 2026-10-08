CREATE OR REPLACE VIEW sector_leverage_rankings AS
SELECT
    c.ticker,
    c.company_name,
    c.sector,
    f.debt_to_assets_ratio,
    CASE
        WHEN f.debt_to_assets_ratio IS NOT NULL THEN
            RANK() OVER (
                PARTITION BY c.sector
                ORDER BY f.debt_to_assets_ratio DESC
            )
    END AS sector_rank,
    f.fiscal_period_end
FROM companies c
LEFT JOIN financials f ON c.ticker = f.ticker;
