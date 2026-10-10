Use SEC EDGAR to compute Leverage Ratio, Interest Coverage Ratio, and Current Ratio

Analyze financial risk for equity investors and creditos

Do not use edgartools get total method (unrelaible fallbacks)


Data validation and concept selection

The project uses the official FASB U.S. GAAP taxonomy accepted by the SEC to define the financial amounts used in each ratio. Concept selection is based on published definitions, rather than statement labels, similar tag names, or a library’s automatic mappings.

The review established four primary concepts:

| Financial amount | Primary concept |
| Total assets | `us-gaap:Assets` |
| Total liabilities | `us-gaap:Liabilities` |
| Operating income or loss | `us-gaap:OperatingIncomeLoss` |
| Total interest expense | `us-gaap:InterestExpense` |

Related concepts were reviewed for differences in scope. For example, nonoperating interest expense is only part of total interest expense, while cash interest paid measures cash payments rather than recognized expense. Neither is treated as an interchangeable substitute. No synonymous alternatives were identified for the selected primary and component tags in the reviewed 2026 taxonomy.

When a primary amount is unavailable, a fallback is permitted only when an accounting equation and the official component definitions support the reconstruction. Examples include:

- Total assets = current assets + noncurrent assets.
- Total liabilities = current liabilities + noncurrent liabilities.
- Total interest expense = operating interest expense + nonoperating interest expense.

Reviewing equity definitions also identified a limitation in the earlier assets-minus-equity fallback: permanent equity excludes temporary equity. Any reconstruction using equity must account for that distinction. An absent component is not automatically treated as zero, because a missing tag may represent an omitted subtotal rather than an absent balance.

Extraction selects undimensioned facts for consolidated amounts and matches them to the relevant fiscal period. Balance-sheet amounts use the fiscal year-end date; income-statement amounts must share the same annual start and end dates. Required amounts that cannot be obtained through a supported method remain null. Ratios with a zero denominator also remain null.

Pilot runs check that filing retrieval, period selection, component extraction, and ratio calculations work together across companies and years. This validates the pipeline’s use of reported facts; it does not independently audit companies’ accounting or guarantee the accuracy of their filings. Company-specific custom tags are outside the current extraction scope.

The taxonomy review defines acceptable extraction rules. Additional fallbacks identified during that review are not considered implemented until they are added to the pipeline.