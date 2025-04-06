import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')

# Load the processed data
print("Loading processed data...")
df = pd.read_csv('processed_proficiency_data.csv')

# Create directory for plots if it doesn't exist
import os
if not os.path.exists('plots'):
    os.makedirs('plots')

# Define skill columns for reference
skill_columns = [
    'Reading Comprehension \n(Understanding academic text)', 
    'Listening Skills (Understanding lectures and spoken English)',
    'Speaking Skills (Fluency and confidence in spoken communication)',
    'Writing Skills (Ability to write academic papers and assignments)'
]

# Simplified names for plotting
skill_names = {
    'Reading Comprehension \n(Understanding academic text)': 'Reading',
    'Listening Skills (Understanding lectures and spoken English)': 'Listening',
    'Speaking Skills (Fluency and confidence in spoken communication)': 'Speaking',
    'Writing Skills (Ability to write academic papers and assignments)': 'Writing'
}

# Plot 1: Overall Proficiency Distribution
plt.figure(figsize=(12, 6))

# Boxplot
plt.subplot(1, 2, 1)
sns.boxplot(x='Student_Type', y='Proficiency_Score', data=df)
plt.title('English Proficiency by Student Type')
plt.xlabel('Student Type')
plt.ylabel('Proficiency Score (1-5 scale)')
plt.ylim(1, 5.5)

# Violin plot
plt.subplot(1, 2, 2)
sns.violinplot(x='Student_Type', y='Proficiency_Score', data=df, inner='quartile')
plt.title('Proficiency Distribution Comparison')
plt.xlabel('Student Type')
plt.ylabel('Proficiency Score (1-5 scale)')
plt.ylim(1, 5.5)

plt.tight_layout()
plt.savefig('plots/overall_proficiency.png', dpi=300)
print("Saved overall proficiency plot")

# Plot 2: Skill-by-Skill Comparison
plt.figure(figsize=(12, 8))

# Prepare data
skill_data = []
for skill in skill_columns:
    for student_type in ['Indian', 'Foreign']:
        subset = df[df['Student_Type'] == student_type]
        skill_data.append({
            'Skill': skill_names[skill],
            'Student_Type': student_type,
            'Mean': subset[skill].mean(),
            'SE': subset[skill].std() / np.sqrt(len(subset)),
            'SD': subset[skill].std()
        })

skill_df = pd.DataFrame(skill_data)

# Bar plot with error bars
plt.subplot(2, 1, 1)
sns.barplot(x='Skill', y='Mean', hue='Student_Type', data=skill_df, errorbar=('ci', 95))
plt.title('Comparison of English Skills by Student Type with 95% CI')
plt.xlabel('Skill Area')
plt.ylabel('Mean Score (1-5 scale)')
plt.ylim(1, 5)
plt.legend(title='Student Type')

# Radar chart for skills comparison
plt.subplot(2, 1, 2)

# Prepare data for radar chart
categories = list(skill_names.values())
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Close the loop

indian_means = [skill_df[(skill_df['Student_Type'] == 'Indian') & (skill_df['Skill'] == skill)]['Mean'].values[0] 
                for skill in categories]
indian_means += indian_means[:1]  # Close the loop

foreign_means = [skill_df[(skill_df['Student_Type'] == 'Foreign') & (skill_df['Skill'] == skill)]['Mean'].values[0] 
                 for skill in categories]
foreign_means += foreign_means[:1]  # Close the loop

# Create radar chart
ax = plt.subplot(2, 1, 2, polar=True)
plt.xticks(angles[:-1], categories, color='grey', size=10)
plt.yticks(np.arange(1, 6), ['1', '2', '3', '4', '5'], color='grey', size=8)
plt.ylim(0, 5)

# Plot data
ax.plot(angles, indian_means, linewidth=1, linestyle='solid', label='Indian')
ax.fill(angles, indian_means, alpha=0.25)
ax.plot(angles, foreign_means, linewidth=1, linestyle='solid', label='Foreign')
ax.fill(angles, foreign_means, alpha=0.25)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.title('Skills Radar Chart: Indian vs Foreign Students')

plt.tight_layout()
plt.savefig('plots/skill_comparison.png', dpi=300)
print("Saved skill comparison plot")

# Plot 3: Analysis by Education Level
plt.figure(figsize=(14, 6))

# Boxplot
plt.subplot(1, 2, 1)
sns.boxplot(x='Level of Study', y='Proficiency_Score', hue='Student_Type', data=df)
plt.title('Proficiency by Level of Study')
plt.xlabel('Level of Study')
plt.ylabel('Proficiency Score (1-5 scale)')
plt.ylim(1, 5.5)
plt.legend(title='Student Type')

# Group barplot
level_data = []
for level in df['Level of Study'].unique():
    for student_type in ['Indian', 'Foreign']:
        subset = df[(df['Level of Study'] == level) & (df['Student_Type'] == student_type)]
        if len(subset) > 0:
            level_data.append({
                'Level': level,
                'Student_Type': student_type,
                'Mean': subset['Proficiency_Score'].mean(),
                'SE': subset['Proficiency_Score'].std() / np.sqrt(len(subset)),
                'Count': len(subset)
            })

level_df = pd.DataFrame(level_data)

plt.subplot(1, 2, 2)
barplot = sns.barplot(x='Level', y='Mean', hue='Student_Type', data=level_df, errorbar=('ci', 95))
plt.title('Mean Proficiency by Level of Study with 95% CI')
plt.xlabel('Level of Study')
plt.ylabel('Mean Proficiency Score (1-5 scale)')
plt.ylim(1, 5)

# Add sample size as text on bars
for i, level in enumerate(['Postgraduate', 'Undergraduate']):
    for j, st in enumerate(['Indian', 'Foreign']):
        count = level_df[(level_df['Level'] == level) & (level_df['Student_Type'] == st)]['Count'].values[0]
        barplot.text(i + (j-0.5)*0.4, 1.2, f'n={count}', ha='center')

plt.tight_layout()
plt.savefig('plots/study_level_comparison.png', dpi=300)
print("Saved study level comparison plot")

# Plot 4: Focus on Speaking Skills
plt.figure(figsize=(10, 8))

# Distribution of speaking scores
speaking_col = 'Speaking Skills (Fluency and confidence in spoken communication)'
plt.subplot(2, 1, 1)
for student_type, color in zip(['Indian', 'Foreign'], ['blue', 'green']):
    subset = df[df['Student_Type'] == student_type]
    sns.kdeplot(subset[speaking_col], fill=True, alpha=0.5, label=student_type, color=color)

plt.title('Distribution of Speaking Skills Scores')
plt.xlabel('Speaking Score (1-5 scale)')
plt.ylabel('Density')
plt.xlim(1, 5.5)
plt.legend(title='Student Type')

# Comparison of skills for Indian students
plt.subplot(2, 1, 2)
indian_df = df[df['Student_Type'] == 'Indian']
indian_skills = pd.melt(indian_df, 
                        id_vars=['Student_Type'], 
                        value_vars=skill_columns,
                        var_name='Skill', 
                        value_name='Score')
indian_skills['Skill'] = indian_skills['Skill'].map(skill_names)

sns.boxplot(x='Skill', y='Score', data=indian_skills)
plt.title('Comparison of Skills Among Indian Students')
plt.xlabel('Skill Area')
plt.ylabel('Score (1-5 scale)')
plt.ylim(1, 5.5)

plt.tight_layout()
plt.savefig('plots/speaking_skills_focus.png', dpi=300)
print("Saved speaking skills focus plot")

print("All visualizations have been created and saved to the 'plots' directory") 