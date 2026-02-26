# Feature Reference & Analytics Guide

## Analytics Features Overview

### 1. Performance Analysis Module (`/analytics/performance/`)

#### Accessible By:
- Admin (all classes)
- Teacher (assigned classes)
- Student (own performance in class context)

#### Features:

**Class Filter**
```
Dropdown: Class 9, Class 10, Class 11, Class 12
Behavior: Dynamically updates all statistics below
```

**Statistics Cards**
```
┌─────────────────────┬──────────────────┬─────────────────┐
│ Total Students      │ Average Score    │ Pass Rate       │
│ (from filtered data)│ (class average)  │ (percentage)    │
└─────────────────────┴──────────────────┴─────────────────┘
```

**Charts Displayed:**
1. **Pass/Fail Doughnut Chart**
   - Splits students into Pass vs Fail
   - Color: Green (Pass), Red (Fail)
   - Threshold: 40 marks

2. **Score Distribution Bar Chart**
   - Bins: 0-10, 10-20, ... 90-100
   - Shows number of students in each range
   - Helps identify performance levels

**Top 10 Performers Table**
- Columns: Rank, Name, Roll No, Average Score
- Sorted: Highest to lowest
- Criteria: Average across all subjects

**Low Performers Table** (Average < 50)
- Columns: Name, Roll No, Average Score, Status
- Sorted: Lowest to highest
- Status: "Needs Support"
- Action: Direct intervention needed

**Students Table**
- Columns: Name, Roll No, Class, Department, Email, Action
- Sortable: Click headers
- Searchable: Via browser's find function

---

### 2. Reports Module (`/analytics/reports/`)

#### Features:

**Filters:**
- Class Filter (dropdown)
- Subject Filter (dropdown)
- Combined filtering (class + subject)

**Statistics Cards:**
- Overall Average Score
- Total Mark Records
- Subject-specific stats (if filtered)

**Subject Statistics Display** (when subject selected):
```
Card shows:
├─ Subject Name
├─ Average Score
├─ Pass Rate (%)
├─ Passed Count
└─ Failed Count
```

**Charts:**
- **Subject-wise Distribution**: Line chart of scores per subject

**Detailed Marks Table:**
- Columns:
  - Student Name
  - Roll Number
  - Subject
  - Marks (0-100)
  - Grade (A+/A/B/C/D/F)
  - Attendance (%)
  - Status (Pass/Fail)

**Export Feature:**
- Button: "Export CSV"
- Downloads: `student_marks_report.csv`
- Format: Compatible with Excel/Sheets
- Includes: All visible table data

---

### 3. Suggestions Module (`/analytics/suggestions/`)

#### Key Metrics Displayed:
```
Average Score     │  Attendance %    │  Performance Status
──────────────────┼──────────────────┼────────────────────
Calculated avg    │  Current level   │  Visual indicator
```

#### Primary Recommendation (Dynamic):
Based on performance and attendance:

**If Average >= 80 AND Attendance >= 85%:**
✅ "Good performance. Keep it up!"
- Maintain current study routine
- Help struggling peers
- Challenge yourself with advanced topics

**If Average 60-80 OR Attendance 75-85%:**
⚠️ "Practice more & improve attendance"
- Practice question papers
- Review previous exams
- Create study plan

**If Average 40-60 AND Attendance < 75%:**
⚠️ "Focus on weak subjects & attendance"
- Increase study hours
- Focus on specific subjects
- Seek tutoring help

**If Average < 40 AND Attendance < 75%:**
🔴 "Critical: Immediate action needed"
- Increase study hours to 3-4 hours
- Attend extra classes
- Get professional tutoring

#### Academic Performance Analysis:
- Average Score Status: Excellent/Good/Average/Poor
- Subject-wise breakdown (if available)
- Actionable steps (customized list)

#### Attendance Guidance:
- Status: Excellent (≥85%) / Good (≥75%) / Below Target (<75%)
- Recommendations (customized)

#### Subject-Specific Insights:
- Tips for weak areas
- Focused learning strategies
- Group study suggestions
- Practice test recommendations

#### Goal Setting:
**Short-term (1 month):**
- Review current performance
- Identify weak areas
- Create revision schedule
- Increase study hours by 25%

**Long-term (1 semester):**
- Improve overall average by 10%
- Maintain 90%+ attendance
- Master difficult subjects
- Achieve consistent performance

---

### 4. Student Dashboard (`/analytics/student-dashboard/`)

#### Student Information Card:
```
Name: John Doe
Roll No: 001
Class: Class 10
Department: Science
Email: john@example.com
```

#### Performance Summary Stats:
```
┌──────────────────┬──────────────────┬──────────────────┐
│ Average Score    │ Subjects Passed  │ Pass Percentage  │
│ (overall)        │ (count / total)  │ (%)              │
└──────────────────┴──────────────────┴──────────────────┘
```

#### Charts:
1. **Subject-wise Performance Bar Chart**
   - X-axis: Subject names
   - Y-axis: Marks (0-100)
   - Color-coded: A+=Green, A=Blue, B=Orange, F=Red

2. **Pass/Fail Pie Chart**
   - Shows count of passed vs failed

3. **Performance Trend Line Chart** (if available)
   - X-axis: Terms
   - Y-axis: Score progression
   - Shows improvement/decline

#### Subject Details Table:
- Columns:
  - Subject Name
  - Score (marks obtained)
  - Grade (A+/A/B/C/D/F)
  - Status (Passed/Failed)
  - Performance (Excellent/Good/Average/Needs Work)

#### Personalized Recommendations:

**If Average >= 80:**
- Excellent Performance! Badge 🏆
- Maintain current study habits
- Help others in class

**If Average 60-80:**
- Good Performance! Badge ✅
- Focus on weak areas
- Achieve excellence

**If Average 40-60:**
- Average Performance! Badge ⚠️
- Increase study effort
- Seek teacher help

**If Average < 40:**
- Poor Performance! Badge 🚨
- Immediate action needed
- Consider tutoring

---

## Analytics Functions (services.py)

### Available Calculations:

```python
### Basic Analytics
calculate_average(marks)
    Returns: Float (average score)
    Input: QuerySet of Mark objects

get_suggestions(average, attendance)
    Returns: String (recommendation)
    Input: Float average, Float attendance

### Class-Level Analytics
get_class_statistics(class_name)
    Returns: Dict {
        'total_students': int,
        'average_score': float,
        'total_marks': int
    }

get_pass_fail_ratio(class_name)
    Returns: Dict {
        'pass': int,
        'fail': int,
        'pass_percentage': float
    }

get_top_performers(class_name, limit=10)
    Returns: List[Dict] [
        {
            'name': str,
            'roll_no': str,
            'average_score': float
        }
    ]

get_low_performers(class_name, limit=10)
    Returns: List[Dict] (same structure)

get_subject_wise_distribution(class_name, subject_id=None)
    Returns: Dict {
        'subject_name': [list of marks]
    }

### Subject Analytics
get_subject_statistics(subject_id)
    Returns: Dict {
        'subject_name': str,
        'average_score': float,
        'pass_rate': float,
        'pass_count': int,
        'fail_count': int
    }

### Student Analytics
get_student_performance(student_id)
    Returns: Dict {
        'average_score': float,
        'subject_scores': {subject: mark},
        'pass_count': int,
        'total_subjects': int,
        'pass_percentage': float
    }

get_trend_analysis(student_id, subject_id=None)
    Returns: List[Dict] [
        {
            'term': str,
            'score': float,
            'grade': str
        }
    ]
```

---

## Grade System

### Automatic Grade Calculation:

```python
Marks Range    Grade    Descriptor
90-100         A+       Excellent
80-89          A        Very Good
70-79          B        Good
60-69          C        Satisfactory
50-59          D        Passing
< 40           F        Failing

Default Passing Marks: 40
```

### Grade Assignment Logic:
```python
if marks >= 90:
    grade = 'A+'
elif marks >= 80:
    grade = 'A'
elif marks >= 70:
    grade = 'B'
elif marks >= 60:
    grade = 'C'
elif marks >= 50:
    grade = 'D'
else:
    grade = 'F'  # Fail
```

---

## Filtering Capabilities

### Performance Page:
```
Primary Filter: Class (dropdown)
Auto-updates:
  ├─ Class statistics
  ├─ Top performers list
  ├─ Low performers list
  ├─ Charts and graphs
  └─ Students table
```

### Reports Page:
```
Filter 1: Class (dropdown)
Filter 2: Subject (dropdown)
Combined: Both filters work together
Export: CSV of filtered results

Examples:
- Class 10 + Mathematics → All Class 10 Maths marks
- Class 11 + All → All Class 11 marks
- All + Physics → Physics marks across all classes
```

---

## Data Export Features

### CSV Export:
```
File: student_marks_report.csv
When: Click "Export CSV" button on Reports page
Contents: All visible table data
Headers:
  - Student Name
  - Roll No
  - Subject
  - Marks
  - Grade
  - Attendance
  - Status
```

### Export Workflow:
1. Apply filters (optional)
2. Click "Export CSV" button
3. Browser downloads CSV file
4. Open in Excel/Google Sheets
5. Analyze locally or print

---

## Role-Based View Differences

### Admin Views:
- All students across all classes
- All subjects
- All terms
- System-wide analytics
- User management
- Bulk operations

### Teacher Views:
- Students in assigned classes
- Assigned subjects
- Class-specific analytics
- Can record marks
- Bulk upload functionality
- Class reports

### Student Views:
- Own performance only
- Personal dashboards
- Comparison with class average
- Self-assessment tools
- Personal recommendations
- Progress tracking

---

## Performance Indicators

### Color Coding:

**Grades:**
- A+/A = Green (Excellent)
- B = Blue (Good)
- C = Orange (Satisfactory)
- D = Yellow (Passing)
- F = Red (Failing)

**Badges:**
- ✅ Pass = Green badge
- ❌ Fail = Red badge
- ⭐ Top 10 = Gold badge
- ⚠️ Needs Support = Red badge

**Charts:**
- Green = Positive metrics
- Red = Negative metrics
- Blue = Primary color
- Orange/Yellow = Warning zones

---

## Dashboard Navigation

### From Performance:
- Filter by class
- Click student name → View details
- View top/low performers
- Export data → CSV

### From Reports:
- Filter by subject/class
- View detailed marks
- Download CSV report
- Analyze subject stats

### From Suggestions:
- Review recommendations
- Check action items
- Set goals
- Go to Performance for details

### From Student Dashboard:
- Review personal scores
- Check trends
- Read recommendations
- Compare with class (if available)

---

## Data Relationships

```
User (Django)
  ├─ Profile (accounts)
  │   ├─ Role: admin/teacher/student
  │   └─ Department
  │
  └─ Student (analytics) [if student]
      ├─ Name
      ├─ Class
      └─ Marks (many)
          ├─ Subject
          ├─ Term
          ├─ Score
          ├─ Grade (auto-calculated)
          └─ Attendance
```

---

## Customization Points

### Easy to Modify:
1. Grade thresholds (in Mark model)
2. Passing marks (in Subject model)
3. Colors (in CSS variables)
4. Class choices (in Student model)
5. Analytics functions (in services.py)
6. Chart types and options (in templates)

### Moderate Changes:
1. Add new fields to models
2. Create custom filters
3. Add new analytics functions
4. Create new chart types

### Complex Changes:
1. Change database schema
2. Modify authentication system
3. Add API endpoints
4. Implement caching system

---

## Performance Optimization Tips

1. **For Large Datasets:**
   - Use pagination on tables
   - Cache aggregated data
   - Index frequently filtered fields

2. **For Slow Charts:**
   - Reduce data points
   - Pre-calculate values
   - Load asynchronously

3. **For Better UX:**
   - Add loading indicators
   - Implement pagination
   - Cache computed results
   - Use AJAX for filters

---

This guide covers all major features and analytics in the Student Performance System. For more technical details, refer to IMPLEMENTATION_GUIDE.md.
