CREATE VIEW sector_leverage_rankings AS
SELECT
    c.ticker,
    c.company_name,
    c.sector,
    f.debt_to_assets_ratio,
    RANK() OVER (PARTITION BY c.sector ORDER BY f.debt_to_assets_ratio DESC) AS sector_rank
FROM financials f
JOIN companies c ON f.ticker = c.ticker;
