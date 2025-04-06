# Statistical Analysis: Testing English Proficiency Differences Between Indian and Foreign Students

## Research Question
Is there a significant difference in English language proficiency between foreign and Indian students based on their country of origin?

## Data Summary
- **Dataset**: Survey of 100 students (50 Indian, 50 Foreign) at Indian universities
- **Measure**: Self-rated English proficiency across four skills (reading, listening, speaking, writing)
- **Proficiency Scale**: 1 (Very Weak) to 5 (Very Strong)

## Key Descriptive Statistics

| Student Type | Count | Mean Proficiency | Std Dev | Min | 25% | Median | 75% | Max |
|-------------|-------|-----------------|---------|-----|-----|--------|-----|-----|
| Indian      | 50    | 3.63            | 0.75    | 2.25| 3.00| 3.75   | 4.19| 5.0 |
| Foreign     | 50    | 3.86            | 0.76    | 2.25| 3.25| 4.00   | 4.44| 5.0 |

## Statistical Testing

### Assumption Testing
1. **Normality Test (Shapiro-Wilk)**:
   - Indian students: W=0.9680, p-value=0.1911
   - Foreign students: W=0.9563, p-value=0.0624
   - **Conclusion**: Both distributions appear to be normally distributed (p > 0.05)

2. **Homogeneity of Variances (Levene's Test)**:
   - W=0.0000, p-value=1.0000
   - **Conclusion**: Variances appear to be equal (p > 0.05)

### Hypothesis Testing

1. **Independent Samples t-test**:
   - t=-1.5309, p-value=0.1290
   - **Conclusion**: Fail to reject null hypothesis; no statistically significant difference

2. **Mann-Whitney U Test** (non-parametric alternative):
   - U=1034.5000, p-value=0.1360
   - **Conclusion**: Consistent with t-test; no significant difference

3. **One-way ANOVA**:
   - F=2.342, p-value=0.129
   - **Conclusion**: Consistent with other tests; no significant difference

### Effect Size Analysis
- Mean difference: 0.2300
- Cohen's d = 0.3062
- **Classification**: Small effect size

### Equivalence Testing (TOST)
- 90% CI for mean difference: [-0.4795, 0.0195]
- Equivalence bounds: [-0.5, 0.5]
- **Conclusion**: The groups are statistically equivalent (scores differ by less than the equivalence bound)

## Skill-by-Skill Analysis

| Skill Area | Indian Mean | Foreign Mean | Difference | t-statistic | p-value | Effect Size (d) | Significant? |
|------------|-------------|--------------|------------|-------------|---------|-----------------|--------------|
| Reading    | 3.82        | 4.04         | 0.22       | -1.33       | 0.188   | 0.27           | No           |
| Listening  | 3.76        | 3.94         | 0.18       | -0.94       | 0.350   | 0.19           | No           |
| Speaking   | 3.24        | 3.66         | 0.42       | -2.19       | 0.031   | 0.44           | Yes          |
| Writing    | 3.70        | 3.80         | 0.10       | -0.62       | 0.539   | 0.12           | No           |

## Analysis by Level of Study

| Level of Study  | Indian Students |              | Foreign Students |              | t-statistic | p-value | Significant? |
|-----------------|-----------------|--------------|------------------|--------------|-------------|---------|--------------|
|                 | n               | Mean         | n                | Mean         |             |         |              |
| Postgraduate    | 37              | 3.64         | 22               | 4.07         | -2.38       | 0.022   | Yes          |
| Undergraduate   | 13              | 3.60         | 28               | 3.70         | -0.35       | 0.728   | No           |

## Summary and Conclusion

Based on the t-test (p = 0.1290), there is NO statistically significant difference in overall English proficiency between Indian and foreign students. The effect size is small (Cohen's d = 0.3062), indicating that the practical significance of any difference is minimal. Equivalence testing further supports that the groups are statistically equivalent.

## Key Insights

1. **Overall Proficiency**: No significant difference between Indian and foreign students in overall English proficiency.

2. **Skill-Specific Findings**: 
   - Speaking is the only skill area showing a statistically significant difference (p = 0.031)
   - Foreign students report higher fluency and confidence in spoken communication
   - No significant differences in reading, listening, or writing skills

3. **Educational Level Differences**:
   - At the postgraduate level, there is a significant difference in proficiency (p = 0.022)
   - No significant difference at the undergraduate level
   - This suggests that differences may emerge at higher academic levels

## Recommendations for Future Research

1. Focus on speaking skills development, as this is the area with the most apparent differences
2. Investigate the reasons for postgraduate-level differences in proficiency
3. Consider controlling for years of English study and educational background
4. Examine differences by specific country of origin rather than just "Indian" vs. "Foreign" 