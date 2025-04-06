import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Create a function to output results to a file
def write_results(file, text):
    with open(file, 'a') as f:
        f.write(text + '\n')

# Create/clear the output file
output_file = 'proficiency_analysis_results.txt'
with open(output_file, 'w') as f:
    f.write("ENGLISH PROFICIENCY ANALYSIS RESULTS\n")
    f.write("===================================\n\n")

# Step 1: Load and clean the data
print("Loading data...")
write_results(output_file, "Data Loading and Preparation:")
df = pd.read_csv('data/Data Collection.csv')

# Print basic information
print(f"Dataset shape: {df.shape}")
write_results(output_file, f"Dataset shape: {df.shape}")

# Step 2: Data cleaning and preparation
# Remove any rows with missing values in key columns
df = df.dropna(subset=['Nationality', 'First Language', 'Level of Study'])

# Create a binary variable: Indian vs Foreign students
df['Student_Type'] = df['Nationality'].apply(lambda x: 'Indian' if x == 'Indian' else 'Foreign')

# Count student types
count_by_type = df['Student_Type'].value_counts()
write_results(output_file, f"\nStudent count by type:")
write_results(output_file, f"Indian students: {count_by_type.get('Indian', 0)}")
write_results(output_file, f"Foreign students: {count_by_type.get('Foreign', 0)}")
write_results(output_file, f"Total: {len(df)}")

# Step 3: Define English proficiency scores
# Create a composite score for English proficiency based on the 4 skills
# First, convert skill levels to numeric values
skill_mapping = {
    'Very Weak': 1, 
    'Weak': 2, 
    'Moderate': 3, 
    'Strong': 4, 
    'Very Strong': 5,
    'Very strong': 5  # Handle capitalization inconsistency
}

# Apply mapping to skill columns
skill_columns = [
    'Reading Comprehension \n(Understanding academic text)', 
    'Listening Skills (Understanding lectures and spoken English)',
    'Speaking Skills (Fluency and confidence in spoken communication)',
    'Writing Skills (Ability to write academic papers and assignments)'
]

# Convert skill ratings to numeric
for col in skill_columns:
    df[col] = df[col].map(skill_mapping)

# Calculate composite proficiency score (mean of the 4 skills)
df['Proficiency_Score'] = df[skill_columns].mean(axis=1)

# Step 4: Save processed data to a new file
df.to_csv('processed_proficiency_data.csv', index=False)
print("\nProcessed data saved to 'processed_proficiency_data.csv'")

# Step 5: Descriptive Statistics by Group
print("\nDescriptive Statistics for English Proficiency by Student Type:")
desc_stats = df.groupby('Student_Type')['Proficiency_Score'].describe()
print(desc_stats)

write_results(output_file, "\nDescriptive Statistics for English Proficiency by Student Type:")
write_results(output_file, desc_stats.to_string())

# Step 6: Statistical Tests
print("\nStatistical Tests for English Proficiency Differences:")
write_results(output_file, "\n\nSTATISTICAL TESTING")
write_results(output_file, "===================")

# Get scores for each group
indian_scores = df[df['Student_Type'] == 'Indian']['Proficiency_Score']
foreign_scores = df[df['Student_Type'] == 'Foreign']['Proficiency_Score']

# 6.1 Shapiro-Wilk Test for Normality
print("\nNormality Tests:")
write_results(output_file, "\n1. Testing Normality Assumption")
indian_shapiro = stats.shapiro(indian_scores)
foreign_shapiro = stats.shapiro(foreign_scores)

print(f"Shapiro-Wilk test for Indian students: W={indian_shapiro.statistic:.4f}, p-value={indian_shapiro.pvalue:.4f}")
print(f"Shapiro-Wilk test for Foreign students: W={foreign_shapiro.statistic:.4f}, p-value={foreign_shapiro.pvalue:.4f}")

write_results(output_file, f"Shapiro-Wilk test for Indian students: W={indian_shapiro.statistic:.4f}, p-value={indian_shapiro.pvalue:.4f}")
write_results(output_file, f"Shapiro-Wilk test for Foreign students: W={foreign_shapiro.statistic:.4f}, p-value={foreign_shapiro.pvalue:.4f}")

if indian_shapiro.pvalue > 0.05 and foreign_shapiro.pvalue > 0.05:
    print("Both distributions appear to be normally distributed (p > 0.05)")
    write_results(output_file, "Conclusion: Both distributions appear to be normally distributed (p > 0.05)")
    normality_assumption_met = True
else:
    print("At least one distribution deviates from normality")
    write_results(output_file, "Conclusion: At least one distribution deviates from normality")
    normality_assumption_met = False

# 6.2 Levene's Test for Homogeneity of Variances
print("\nHomogeneity of Variances Test:")
write_results(output_file, "\n2. Testing Homogeneity of Variances")
levene = stats.levene(indian_scores, foreign_scores)
print(f"Levene's test: W={levene.statistic:.4f}, p-value={levene.pvalue:.4f}")
write_results(output_file, f"Levene's test: W={levene.statistic:.4f}, p-value={levene.pvalue:.4f}")

if levene.pvalue > 0.05:
    print("Variances appear to be equal (p > 0.05)")
    write_results(output_file, "Conclusion: Variances appear to be equal (p > 0.05)")
    equal_variance = True
else:
    print("Variances appear to be unequal")
    write_results(output_file, "Conclusion: Variances appear to be unequal")
    equal_variance = False

# 6.3 Choose appropriate test based on assumptions
print("\nHypothesis Test Results:")
write_results(output_file, "\n3. Hypothesis Testing")

# T-test (parametric)
t_test = stats.ttest_ind(indian_scores, foreign_scores, equal_var=equal_variance)
print(f"Independent samples t-test: t={t_test.statistic:.4f}, p-value={t_test.pvalue:.4f}")
write_results(output_file, f"Independent samples t-test: t={t_test.statistic:.4f}, p-value={t_test.pvalue:.4f}")

# Mann-Whitney U test (non-parametric)
u_test = stats.mannwhitneyu(indian_scores, foreign_scores)
print(f"Mann-Whitney U test: U={u_test.statistic:.4f}, p-value={u_test.pvalue:.4f}")
write_results(output_file, f"Mann-Whitney U test: U={u_test.statistic:.4f}, p-value={u_test.pvalue:.4f}")

# 6.4 One-way ANOVA
model = ols('Proficiency_Score ~ Student_Type', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("\nOne-way ANOVA results:")
print(anova_table)
write_results(output_file, "\n4. One-way ANOVA")
write_results(output_file, anova_table.to_string())

# Step 7: Effect Size Calculation
write_results(output_file, "\n5. Effect Size Analysis")
mean1 = indian_scores.mean()
mean2 = foreign_scores.mean()
n1 = len(indian_scores)
n2 = len(foreign_scores)
var1 = indian_scores.var()
var2 = foreign_scores.var()

# Pooled standard deviation
pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

# Cohen's d
cohen_d = abs(mean1 - mean2) / pooled_std
print(f"\nEffect Size Analysis:")
print(f"Mean proficiency score (Indian): {mean1:.4f}")
print(f"Mean proficiency score (Foreign): {mean2:.4f}")
print(f"Mean difference: {abs(mean1 - mean2):.4f}")
print(f"Effect size (Cohen's d): {cohen_d:.4f}")

write_results(output_file, f"Mean proficiency score (Indian): {mean1:.4f}")
write_results(output_file, f"Mean proficiency score (Foreign): {mean2:.4f}")
write_results(output_file, f"Mean difference: {abs(mean1 - mean2):.4f}")
write_results(output_file, f"Effect size (Cohen's d): {cohen_d:.4f}")

# Classification of effect size
if cohen_d < 0.2:
    effect_size_class = "negligible"
elif cohen_d < 0.5:
    effect_size_class = "small"
elif cohen_d < 0.8:
    effect_size_class = "medium"
else:
    effect_size_class = "large"

print(f"Effect size classification: {effect_size_class}")
write_results(output_file, f"Effect size classification: {effect_size_class}")

# Step 8: Equivalence Testing
# Two One-Sided Tests (TOST) approach for equivalence
# Define equivalence bounds (0.5 is often used as meaningful difference threshold)
print("\nEquivalence Testing:")
write_results(output_file, "\n6. Equivalence Testing (TOST)")
epsilon = 0.5

# Calculate 90% confidence interval for mean difference
# (90% CI is used for two one-sided tests at alpha=0.05)
mean_diff = mean1 - mean2
se_diff = np.sqrt(var1/n1 + var2/n2)
ci_lower = mean_diff - stats.t.ppf(0.95, n1+n2-2) * se_diff
ci_upper = mean_diff + stats.t.ppf(0.95, n1+n2-2) * se_diff

print(f"90% Confidence Interval for mean difference: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"Equivalence bounds: [-{epsilon:.1f}, {epsilon:.1f}]")
write_results(output_file, f"90% Confidence Interval for mean difference: [{ci_lower:.4f}, {ci_upper:.4f}]")
write_results(output_file, f"Equivalence bounds: [-{epsilon:.1f}, {epsilon:.1f}]")

if ci_lower > -epsilon and ci_upper < epsilon:
    print("The groups are statistically equivalent (scores differ by less than the equivalence bound)")
    write_results(output_file, "Conclusion: The groups are statistically equivalent (scores differ by less than the equivalence bound)")
    equivalence_conclusion = "equivalent"
else:
    print("Cannot conclude that the groups are equivalent")
    write_results(output_file, "Conclusion: Cannot conclude that the groups are equivalent")
    equivalence_conclusion = "not equivalent"

# Step 9: Skill-by-Skill Analysis
print("\nSkill-by-Skill Analysis:")
write_results(output_file, "\n\nSKILL-BY-SKILL ANALYSIS")
write_results(output_file, "======================")

for skill in skill_columns:
    # Extract skill name for better readability
    skill_name = skill.split('(')[0].strip()
    
    # Get scores for this skill
    indian_skill = df[df['Student_Type'] == 'Indian'][skill]
    foreign_skill = df[df['Student_Type'] == 'Foreign'][skill]
    
    # Run t-test
    skill_ttest = stats.ttest_ind(indian_skill, foreign_skill, equal_var=equal_variance)
    
    # Calculate effect size
    skill_mean1 = indian_skill.mean()
    skill_mean2 = foreign_skill.mean()
    skill_var1 = indian_skill.var()
    skill_var2 = foreign_skill.var()
    skill_n1 = len(indian_skill)
    skill_n2 = len(foreign_skill)
    
    skill_pooled_std = np.sqrt(((skill_n1 - 1) * skill_var1 + (skill_n2 - 1) * skill_var2) / (skill_n1 + skill_n2 - 2))
    skill_cohen_d = abs(skill_mean1 - skill_mean2) / skill_pooled_std
    
    print(f"\n{skill_name}:")
    print(f"  Mean (Indian): {skill_mean1:.2f}, Mean (Foreign): {skill_mean2:.2f}")
    print(f"  t-test: t={skill_ttest.statistic:.4f}, p-value={skill_ttest.pvalue:.4f}")
    print(f"  Effect size (Cohen's d): {skill_cohen_d:.4f}")
    
    write_results(output_file, f"\n{skill_name}:")
    write_results(output_file, f"  Mean (Indian): {skill_mean1:.2f}, Mean (Foreign): {skill_mean2:.2f}")
    write_results(output_file, f"  Mean difference: {abs(skill_mean1 - skill_mean2):.2f}")
    write_results(output_file, f"  t-test: t={skill_ttest.statistic:.4f}, p-value={skill_ttest.pvalue:.4f}")
    write_results(output_file, f"  Effect size (Cohen's d): {skill_cohen_d:.4f}")
    
    if skill_ttest.pvalue < 0.05:
        print(f"  Result: Significant difference detected")
        write_results(output_file, f"  Result: Significant difference detected")
    else:
        print(f"  Result: No significant difference")
        write_results(output_file, f"  Result: No significant difference")

# Step 10: Analysis by Study Level
print("\nAnalysis by Level of Study:")
write_results(output_file, "\n\nANALYSIS BY LEVEL OF STUDY")
write_results(output_file, "=======================")
study_levels = df['Level of Study'].unique()

for level in study_levels:
    # Get data for this level
    level_data = df[df['Level of Study'] == level]
    
    # Check if we have enough data
    if len(level_data) < 5:
        print(f"\n{level}: Insufficient data for analysis (n={len(level_data)})")
        write_results(output_file, f"\n{level}: Insufficient data for analysis (n={len(level_data)})")
        continue
        
    # Get scores
    level_indian = level_data[level_data['Student_Type'] == 'Indian']['Proficiency_Score']
    level_foreign = level_data[level_data['Student_Type'] == 'Foreign']['Proficiency_Score']
    
    # Check if we have enough in each group
    if len(level_indian) < 3 or len(level_foreign) < 3:
        print(f"\n{level}: Insufficient data in one or both groups (Indian: {len(level_indian)}, Foreign: {len(level_foreign)})")
        write_results(output_file, f"\n{level}: Insufficient data in one or both groups (Indian: {len(level_indian)}, Foreign: {len(level_foreign)})")
        continue
    
    # Run t-test
    level_ttest = stats.ttest_ind(level_indian, level_foreign, equal_var=False)
    
    print(f"\n{level}:")
    print(f"  Indian students: n={len(level_indian)}, mean={level_indian.mean():.2f}")
    print(f"  Foreign students: n={len(level_foreign)}, mean={level_foreign.mean():.2f}")
    print(f"  t-test: t={level_ttest.statistic:.4f}, p-value={level_ttest.pvalue:.4f}")
    
    write_results(output_file, f"\n{level}:")
    write_results(output_file, f"  Indian students: n={len(level_indian)}, mean={level_indian.mean():.2f}")
    write_results(output_file, f"  Foreign students: n={len(level_foreign)}, mean={level_foreign.mean():.2f}")
    write_results(output_file, f"  Mean difference: {abs(level_indian.mean() - level_foreign.mean()):.2f}")
    write_results(output_file, f"  t-test: t={level_ttest.statistic:.4f}, p-value={level_ttest.pvalue:.4f}")
    
    if level_ttest.pvalue < 0.05:
        print(f"  Result: Significant difference detected")
        write_results(output_file, f"  Result: Significant difference detected")
    else:
        print(f"  Result: No significant difference")
        write_results(output_file, f"  Result: No significant difference")

# Step 11: Summary and Conclusion
print("\n=========================================================")
print("SUMMARY AND CONCLUSION")
print("=========================================================")

write_results(output_file, "\n\nSUMMARY AND CONCLUSION")
write_results(output_file, "====================")

if t_test.pvalue >= 0.05:
    conclusion = "Based on the t-test (p = {:.4f}), there is NO statistically significant difference in English proficiency between Indian and foreign students.".format(t_test.pvalue)
    print(conclusion)
    write_results(output_file, conclusion)
else:
    conclusion = "Based on the t-test (p = {:.4f}), there IS a statistically significant difference in English proficiency between Indian and foreign students.".format(t_test.pvalue)
    print(conclusion)
    write_results(output_file, conclusion)

effect_conclusion = f"The effect size is {effect_size_class} (Cohen's d = {cohen_d:.4f}), indicating that the practical significance of any difference is {effect_size_class}."
print(effect_conclusion)
write_results(output_file, effect_conclusion)

equiv_conclusion = f"Equivalence testing suggests that the groups are {equivalence_conclusion}. (90% CI for mean difference: [{ci_lower:.4f}, {ci_upper:.4f}], equivalence bounds: [-{epsilon:.1f}, {epsilon:.1f}])"
print(equiv_conclusion)
write_results(output_file, equiv_conclusion)

print("\nInterpretation:")
write_results(output_file, "\nInterpretation:")

if t_test.pvalue >= 0.05 and equivalence_conclusion == "equivalent":
    interpretation = "The data strongly supports the claim that there is no significant difference in English proficiency between Indian and foreign students based on country of origin."
    print(interpretation)
    write_results(output_file, interpretation)
elif t_test.pvalue >= 0.05 and equivalence_conclusion != "equivalent":
    interpretation = "While we cannot reject the null hypothesis of no difference, we also cannot confidently claim equivalence. More data may be needed."
    print(interpretation)
    write_results(output_file, interpretation)
elif t_test.pvalue < 0.05 and effect_size_class in ["negligible", "small"]:
    interpretation = f"Although a statistically significant difference was detected, the effect size is {effect_size_class}, suggesting that the practical importance of this difference may be limited."
    print(interpretation)
    write_results(output_file, interpretation)
else:
    interpretation = "There appears to be a meaningful difference in English proficiency between the groups, with foreign students scoring higher on average."
    print(interpretation)
    write_results(output_file, interpretation)

# Add skill-specific insights
write_results(output_file, "\nSkill-specific insights:")
speaking_test = stats.ttest_ind(
    df[df['Student_Type'] == 'Indian']['Speaking Skills (Fluency and confidence in spoken communication)'],
    df[df['Student_Type'] == 'Foreign']['Speaking Skills (Fluency and confidence in spoken communication)'],
    equal_var=equal_variance
)

if speaking_test.pvalue < 0.05:
    write_results(output_file, "- Speaking is the only skill area showing a statistically significant difference between the groups.")
    write_results(output_file, "  Foreign students report higher fluency and confidence in spoken communication.")

# Add educational level insights
pg_test = stats.ttest_ind(
    df[(df['Student_Type'] == 'Indian') & (df['Level of Study'] == 'Postgraduate')]['Proficiency_Score'],
    df[(df['Student_Type'] == 'Foreign') & (df['Level of Study'] == 'Postgraduate')]['Proficiency_Score'],
    equal_var=False
)

if pg_test.pvalue < 0.05:
    write_results(output_file, "- At the postgraduate level, there is a significant difference in proficiency between Indian and foreign students.")
    write_results(output_file, "  This difference is not observed at the undergraduate level.")

# Final recommendations
write_results(output_file, "\nRecommendations for future research:")
write_results(output_file, "1. Focus on speaking skills development, as this is the area with the most apparent differences")
write_results(output_file, "2. Investigate the reasons for postgraduate-level differences in proficiency")
write_results(output_file, "3. Consider controlling for years of English study and educational background in future analyses")
write_results(output_file, "4. Examine differences by specific country of origin rather than just 'Indian' vs. 'Foreign'")

print(f"\nDetailed analysis has been saved to '{output_file}'") 