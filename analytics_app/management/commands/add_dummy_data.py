from django.core.management.base import BaseCommand
from analytics_app.models import Student, Subject, Mark
import random


class Command(BaseCommand):
    help = 'Add dummy students, subjects, and marks to the database'

    def handle(self, *args, **options):
        # List of subjects to add
        subjects_to_add = [
            'Wireless Technology',
            'Network Protocols',
            'Basic Circuits',
            'Big Data Analytics',
            'IoT Sensors'
        ]

        # Check if subjects already exist, if not, add them
        existing_subjects = Subject.objects.values_list('subject_name', flat=True)
        
        if existing_subjects.count() == 0:
            self.stdout.write(self.style.WARNING('No subjects found. Adding 5 subjects...'))
            
            for subject_name in subjects_to_add:
                subject, created = Subject.objects.get_or_create(subject_name=subject_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Created subject: {subject_name}'))
                else:
                    self.stdout.write(f'Subject already exists: {subject_name}')
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Found {existing_subjects.count()} existing subjects'))
            for subject in existing_subjects:
                self.stdout.write(f'  - {subject}')

        # Dummy student data
        dummy_students_data = [
            {'name': 'Aarav Kumar', 'roll_no': 'CS001', 'department': 'Computer Science'},
            {'name': 'Bhavna Singh', 'roll_no': 'CS002', 'department': 'Computer Science'},
            {'name': 'Chirag Patel', 'roll_no': 'CS003', 'department': 'Computer Science'},
            {'name': 'Diya Sharma', 'roll_no': 'CS004', 'department': 'Computer Science'},
            {'name': 'Eshaan Desai', 'roll_no': 'CS005', 'department': 'Computer Science'},
            {'name': 'Fiona Gupta', 'roll_no': 'CS006', 'department': 'Computer Science'},
            {'name': 'Gagan Roy', 'roll_no': 'CS007', 'department': 'Computer Science'},
            {'name': 'Hina Verma', 'roll_no': 'CS008', 'department': 'Computer Science'},
            {'name': 'Ishaan Khan', 'roll_no': 'CS009', 'department': 'Computer Science'},
            {'name': 'Jiya Nair', 'roll_no': 'CS010', 'department': 'Computer Science'},
        ]

        # Add dummy students
        self.stdout.write(self.style.WARNING('\nAdding 10 dummy students...'))
        created_students = []
        
        for student_data in dummy_students_data:
            student, created = Student.objects.get_or_create(
                roll_no=student_data['roll_no'],
                defaults={
                    'name': student_data['name'],
                    'department': student_data['department']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created student: {student.name} ({student.roll_no})'))
                created_students.append(student)
            else:
                self.stdout.write(f'Student already exists: {student.name}')
                created_students.append(student)

        # Add marks for students
        self.stdout.write(self.style.WARNING('\nAdding marks and attendance for students...'))
        
        all_subjects = Subject.objects.all()
        
        for student in created_students:
            for subject in all_subjects:
                # Check if mark already exists
                mark_exists = Mark.objects.filter(
                    student=student,
                    subject=subject
                ).exists()
                
                if not mark_exists:
                    # Generate random marks and attendance
                    marks = random.randint(30, 100)
                    attendance = random.uniform(50, 100)
                    
                    Mark.objects.create(
                        student=student,
                        subject=subject,
                        marks_obtained=marks,
                        attendance_percentage=round(attendance, 2)
                    )
                    
                    self.stdout.write(
                        f'✓ Added marks for {student.name} in {subject.subject_name}: '
                        f'{marks} marks, {round(attendance, 2)}% attendance'
                    )

        self.stdout.write(self.style.SUCCESS('\n✓ Dummy data added successfully!'))
