# Excel Risk Register Structure Guide

**Purpose:** Guide for creating a professional Excel Risk Register using Claude's xlsx skill

**Target File:** Risk-Register.xlsx  
**Complexity:** Medium (formulas, conditional formatting, data validation)

---

## Sheet Structure

### Create 3 Sheets:
1. **Risk Register** (main sheet)
2. **Lookup Tables** (support data)
3. **Dashboard** (executive summary)

---

## Sheet 1: Risk Register (Main Data)

### Column Definitions

| Column | Header | Type | Width | Notes |
|--------|--------|------|-------|-------|
| A | Risk ID | Text | 10 | Format: R-001, R-002, etc. |
| B | Risk Description | Text | 50 | Wrap text enabled |
| C | Category | Dropdown | 15 | From Lookup Tables sheet |
| D | Probability | Dropdown | 12 | Very Low, Low, Medium, High, Very High |
| E | Probability Score | Formula | 8 | =VLOOKUP(D2,LookupTables!$A$2:$B$6,2,FALSE) |
| F | Impact | Dropdown | 10 | 1, 2, 3, 4, 5 |
| G | Risk Score | Formula | 8 | =E2*F2 |
| H | Risk Level | Formula | 12 | See formula below |
| I | Response Strategy | Dropdown | 15 | Avoid, Transfer, Mitigate, Accept |
| J | Mitigation Plan | Text | 40 | Wrap text enabled |
| K | Owner | Text | 20 | |
| L | Status | Dropdown | 12 | Open, Mitigated, Closed |
| M | Last Reviewed | Date | 12 | Format: YYYY-MM-DD |
| N | Target Close Date | Date | 12 | Format: YYYY-MM-DD |
| O | Cost Impact ($) | Currency | 12 | Format: $#,##0 |

### Row 1: Headers
- Font: Bold, 11pt, Calibri
- Fill: Dark Blue (RGB: 68, 114, 196)
- Font Color: White
- Alignment: Center
- Borders: All borders
- **Freeze panes after Row 1**

### Data Rows (Row 2 onward)
- Font: 11pt, Calibri
- Alternating row colors:
  - Even rows: White
  - Odd rows: Light Gray (RGB: 242, 242, 242)
- Text wrap ON for columns B, J
- Borders: Light gray grid

---

## Formulas

### E2: Probability Score
```excel
=VLOOKUP(D2,LookupTables!$A$2:$B$6,2,FALSE)
```
**Explanation:** Converts text probability (High) to numeric score (4)

### G2: Risk Score
```excel
=E2*F2
```
**Explanation:** Probability Score × Impact Score

### H2: Risk Level
```excel
=IF(G2>=20,"Critical",IF(G2>=15,"High",IF(G2>=8,"Medium","Low")))
```
**Explanation:** 
- Score 20-25: Critical
- Score 15-19: High
- Score 8-14: Medium
- Score 1-7: Low

Copy formulas in E2, G2, H2 down to all data rows.

---

## Conditional Formatting

### Column H: Risk Level
**Rule 1 - Critical (Red):**
- Formula: `=$H2="Critical"`
- Format: Fill Red (RGB: 255, 0, 0), Font White, Bold
- Applies to: $H$2:$H$100

**Rule 2 - High (Orange):**
- Formula: `=$H2="High"`
- Format: Fill Orange (RGB: 255, 192, 0), Font Black, Bold
- Applies to: $H$2:$H$100

**Rule 3 - Medium (Yellow):**
- Formula: `=$H2="Medium"`
- Format: Fill Yellow (RGB: 255, 255, 0), Font Black
- Applies to: $H$2:$H$100

**Rule 4 - Low (Green):**
- Formula: `=$H2="Low"`
- Format: Fill Green (RGB: 146, 208, 80), Font Black
- Applies to: $H$2:$H$100

### Column G: Risk Score
**Color Scale (3-Color):**
- Minimum (1): Green (RGB: 146, 208, 80)
- Midpoint (13): Yellow (RGB: 255, 255, 0)
- Maximum (25): Red (RGB: 255, 0, 0)
- Applies to: $G$2:$G$100

---

## Data Validation

### Column C: Category
- Type: List
- Source: `=LookupTables!$D$2:$D$11`
- Input Message: "Select risk category"
- Error Alert: "Invalid category"

### Column D: Probability
- Type: List
- Source: `LookupTables!$A$2:$A$6`
- Input Message: "Select probability level"

### Column F: Impact
- Type: List
- Source: `1,2,3,4,5`
- Input Message: "Select impact score (1=Very Low, 5=Very High)"

### Column I: Response Strategy
- Type: List
- Source: `Avoid,Transfer,Mitigate,Accept`
- Input Message: "Select response strategy"

### Column L: Status
- Type: List
- Source: `Open,Mitigated,Closed`
- Input Message: "Select current status"

### Columns M, N: Dates
- Type: Date
- Format: `YYYY-MM-DD`

---

## Sheet 2: Lookup Tables

### Table 1: Probability Mapping (A1:B6)

| Probability (Text) | Score |
|-------------------|-------|
| **Probability** | **Score** |
| Very Low | 1 |
| Low | 2 |
| Medium | 3 |
| High | 4 |
| Very High | 5 |

**Name this range:** `ProbabilityTable`

### Table 2: Risk Categories (D1:D11)

| Category |
|----------|
| **Category** |
| Technical |
| Vendor/3rd Party |
| Resource |
| Financial |
| Schedule |
| Scope |
| Change Management |
| Compliance/Legal |
| External |
| Operational |

**Formatting:**
- Header: Bold, Dark Blue fill
- Data: Light blue fill (RGB: 217, 225, 242)

---

## Sheet 3: Dashboard (Executive Summary)

### Layout

**A1:F1** - Title
- Merge cells
- "Risk Register Dashboard"
- Font: 18pt, Bold, Center
- Fill: Dark Blue

**A3:B3** - Summary Stats Section

**Create Summary Table (A3:B8):**

| Metric | Value |
|--------|-------|
| **Total Risks** | =COUNTA(RiskRegister!A:A)-1 |
| **Critical Risks** | =COUNTIF(RiskRegister!H:H,"Critical") |
| **High Risks** | =COUNTIF(RiskRegister!H:H,"High") |
| **Medium Risks** | =COUNTIF(RiskRegister!H:H,"Medium") |
| **Low Risks** | =COUNTIF(RiskRegister!H:H,"Low") |
| **Total Exposure ($)** | =SUM(RiskRegister!O:O) |

**Formatting:**
- Column A: Bold, Right-aligned
- Column B: Center-aligned, larger font (14pt)
- Critical/High numbers: Red/Orange font
- Total Exposure: Currency format

### Risk Distribution Pie Chart (D3:F10)

**Chart Type:** Pie Chart

**Data Range:** 
- Categories: Critical, High, Medium, Low
- Values: From summary table B4:B7

**Chart Formatting:**
- Title: "Risk Distribution by Level"
- Colors: Red, Orange, Yellow, Green
- Show percentages
- Legend: Bottom

### Top 5 Risks Table (A12:D17)

**Headers:** Risk ID | Description | Score | Level

**Formula for Row 13:**
```excel
=INDEX(RiskRegister!$A:$A,MATCH(LARGE(RiskRegister!$G:$G,1),RiskRegister!$G:$G,0))
```

Create similar formulas for Top 2, Top 3, Top 4, Top 5 (using LARGE with 1,2,3,4,5)

**Formatting:** Match risk level colors

---

## Named Ranges (Recommended)

Create these for easier formula writing:

- **RiskData:** RiskRegister!$A$2:$O$100
- **RiskScores:** RiskRegister!$G$2:$G$100
- **RiskLevels:** RiskRegister!$H$2:$H$100
- **RiskStatus:** RiskRegister!$L$2:$L$100

---

## Example Formulas for Analysis

### Count Open Critical Risks
```excel
=COUNTIFS(RiskRegister!H:H,"Critical",RiskRegister!L:L,"Open")
```

### Average Risk Score
```excel
=AVERAGE(RiskRegister!G2:G100)
```

### Total Exposure for Open Risks
```excel
=SUMIF(RiskRegister!L:L,"Open",RiskRegister!O:O)
```

### Percentage of High/Critical Risks
```excel
=(COUNTIF(RiskRegister!H:H,"Critical")+COUNTIF(RiskRegister!H:H,"High"))/(COUNTA(RiskRegister!H:H)-1)*100
```

---

## Heat Map (Optional Advanced Feature)

**Create 5x5 grid (H12:L16):**

Rows: Impact (5 to 1)  
Columns: Probability (Very Low to Very High)

**Formula for H12 (Probability=Very Low, Impact=5):**
```excel
=COUNTIFS(RiskRegister!D:D,"Very Low",RiskRegister!F:F,5)
```

**Conditional Formatting on H12:L16:**
- Color scale: White (0) to Dark Red (5+)
- Center text
- Bold

**Labels:**
- Row headers (G12:G16): 5, 4, 3, 2, 1
- Column headers (H11:L11): Very Low, Low, Medium, High, Very High

---

## Protection & Security

### Protect Sheet
- Unlock: Data entry cells (B2:D100, F2:F100, I2:O100)
- Lock: Formula cells (E2:E100, G2:H100)
- Lock: Headers (Row 1)
- Password protect: Optional

---

## Printing Setup

### Risk Register Sheet
- Orientation: Landscape
- Fit to: 1 page wide
- Print Titles: Row 1 (repeat on all pages)
- Header: Project name and date
- Footer: Page X of Y

### Dashboard Sheet
- Orientation: Portrait
- Fit to: 1 page
- Header: "Risk Dashboard - [Project Name]"

---

## Example Data (For Testing)

Add 5 sample risks to demonstrate:

| Risk ID | Description | Category | Probability | Impact | Status |
|---------|-------------|----------|-------------|--------|--------|
| R-001 | Vendor delays by 3+ months | Vendor/3rd Party | High | 5 | Open |
| R-002 | Data migration accuracy <95% | Technical | High | 4 | Open |
| R-003 | Key developer departure | Resource | Medium | 3 | Mitigated |
| R-004 | Budget overrun >15% | Financial | Low | 5 | Open |
| R-005 | Low user adoption (<80%) | Change Management | Medium | 4 | Open |

---

## Best Practices

1. **Start with Row 2:** Leave Row 1 for headers only
2. **Use consistent ID format:** R-001, R-002 (not R1, RISK-001)
3. **Keep descriptions concise:** 1-2 sentences max
4. **Update Last Reviewed:** Every risk review meeting
5. **Archive closed risks:** Move to separate sheet after 90 days
6. **Version control:** Save copies weekly with date in filename
7. **Review formulas:** Before distributing, verify all formulas copy correctly
8. **Test data validation:** Ensure dropdowns work before distributing

---

## Common Issues & Solutions

**Issue:** VLOOKUP returning #N/A  
**Solution:** Check spelling in Probability column matches LookupTables exactly

**Issue:** Conditional formatting not working  
**Solution:** Ensure formula references absolute columns ($H2) and relative rows (H2)

**Issue:** Risk Level formula showing wrong level  
**Solution:** Verify thresholds match your organization's standards

**Issue:** Dropdowns not appearing  
**Solution:** Check Data Validation source ranges are correct

---

## Maintenance

### Weekly
- Update risk status
- Add new risks
- Review and update mitigation plans

### Monthly
- Generate Dashboard report
- Analyze trends
- Archive closed risks

### Quarterly
- Review formulas and formatting
- Update thresholds if needed
- Train new users

---

**File Complexity:** Medium  
**Estimated Build Time:** 30-45 minutes  
**Prerequisites:** Basic Excel formula knowledge  
**Maintenance:** Low (primarily data entry)
