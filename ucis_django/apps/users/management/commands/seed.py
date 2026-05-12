from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserProfile, Education, WorkExperience
from apps.feed.models import Post, Reaction, Comment, Story
from apps.announcements.models import Announcement
from apps.events.models import Event
from apps.jobs.models import JobOpportunity
from apps.campus.models import CampusLocation
from apps.academics.models import Deadline, AlmanacEvent
from apps.notifications.models import Notification
from apps.connections.models import Connection, Message
from apps.news.models import News
from apps.emergency_contacts.models import EmergencyContact


class Command(BaseCommand):
    help = 'Seed the database with dummy data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # ── Users ──────────────────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults=dict(email='admin@ucis.ac.tz', role='system_admin', first_name='System', last_name='Admin', is_staff=True, is_superuser=True),
        )
        if not admin.has_usable_password():
            admin.set_password('Admin1234!')
            admin.save()

        cadmin, _ = User.objects.get_or_create(
            username='college_admin',
            defaults=dict(email='cadmin@coict.ac.tz', role='college_admin', college='CoICT', first_name='College', last_name='Admin'),
        )
        if not cadmin.has_usable_password():
            cadmin.set_password('Admin1234!')
            cadmin.save()

        students_data = [
            ('alice', 'alice@students.ac.tz', 'Alice', 'Mwangi', 'CoICT'),
            ('bob', 'bob@students.ac.tz', 'Bob', 'Kimani', 'CoET'),
            ('carol', 'carol@students.ac.tz', 'Carol', 'Osei', 'CoNAS'),
        ]
        students = []
        for uname, email, fn, ln, col in students_data:
            u, _ = User.objects.get_or_create(username=uname, defaults=dict(email=email, role='student', college=col, first_name=fn, last_name=ln))
            if not u.has_usable_password():
                u.set_password('Pass1234!')
                u.save()
            students.append(u)

        alumni_data = [
            ('david_alumni', 'david@alumni.ac.tz', 'David', 'Nkrumah', 'CoICT'),
            ('eve_alumni', 'eve@alumni.ac.tz', 'Eve', 'Achebe', 'CoET'),
        ]
        alumni = []
        for uname, email, fn, ln, col in alumni_data:
            u, _ = User.objects.get_or_create(username=uname, defaults=dict(email=email, role='alumni', college=col, first_name=fn, last_name=ln))
            if not u.has_usable_password():
                u.set_password('Pass1234!')
                u.save()
            alumni.append(u)

        all_users = [admin, cadmin] + students + alumni
        self.stdout.write(f'  Users: {len(all_users)}')

        # ── Profiles / Education / Work ────────────────────────────────────
        for u in students:
            Education.objects.get_or_create(
                user=u,
                defaults=dict(degree_course='BSc Computer Science', college='CoICT', start_year=2021),
            )

        for u in alumni:
            Education.objects.get_or_create(
                user=u,
                defaults=dict(degree_course='BSc Engineering', college=u.college, start_year=2016, end_year=2020),
            )
            WorkExperience.objects.get_or_create(
                user=u,
                company='TechCorp Africa',
                defaults=dict(job_title='Software Engineer', industry='Technology', start_date='2020-07-01', current=True),
            )

        # ── Posts ──────────────────────────────────────────────────────────
        posts_data = [
            (students[0], 'Looking for study group', 'Anyone interested in forming a DSA study group for the upcoming exams? Drop a comment!', ['student'], ['study', 'DSA']),
            (students[1], 'CoET Lab computers down', 'The computers in Lab 3 are not working. Reported to the technician already.', ['student', 'college_admin'], ['lab', 'CoET']),
            (alumni[0], 'Career tip: internships matter', 'Landing my first job was much easier because of my internship at Vodacom. Start early!', ['student', 'alumni'], ['career', 'tips']),
            (alumni[1], 'Open source contribution guide', "I wrote a beginner's guide to contributing to open source. Link in comments.", ['student', 'alumni'], ['opensource', 'github']),
            (students[2], 'Research paper released', 'Our team published a paper on machine learning in agriculture. Really proud of this one.', ['student', 'alumni'], ['research', 'ML']),
        ]
        posts = []
        for author, title, content, roles, tags in posts_data:
            p, _ = Post.objects.get_or_create(
                title=title,
                defaults=dict(content=content, posted_by=author, target_roles=roles, tags=tags, college=author.college),
            )
            posts.append(p)

        # Reactions & comments
        if posts:
            Reaction.objects.get_or_create(post=posts[0], user=students[1], defaults={'reaction_type': 'like'})
            Reaction.objects.get_or_create(post=posts[0], user=alumni[0], defaults={'reaction_type': 'celebrate'})
            Reaction.objects.get_or_create(post=posts[2], user=students[0], defaults={'reaction_type': 'celebrate'})
            Reaction.objects.get_or_create(post=posts[2], user=students[2], defaults={'reaction_type': 'support'})

            Comment.objects.get_or_create(post=posts[0], user=students[1], defaults={'content': "I'm in! Let's meet at the library tomorrow."})
            Comment.objects.get_or_create(post=posts[0], user=students[2], defaults={'content': 'Count me in too, struggling with graphs.'})
            Comment.objects.get_or_create(post=posts[2], user=students[0], defaults={'content': 'This is so motivating, thank you!'})

        self.stdout.write(f'  Posts: {len(posts)}')

        # ── Stories ────────────────────────────────────────────────────────
        Story.objects.get_or_create(
            posted_by=students[0],
            defaults=dict(content='Just submitted my final year project proposal! 🎉', media_type='text', background_color='#1a1a2e', expires_at=timezone.now() + timedelta(hours=20)),
        )
        Story.objects.get_or_create(
            posted_by=alumni[0],
            defaults=dict(content='Attending a tech summit in Nairobi this week. Networking hard!', media_type='text', background_color='#16213e', expires_at=timezone.now() + timedelta(hours=18)),
        )

        # ── Announcements ──────────────────────────────────────────────────
        ann_data = [
            (admin, 'System Maintenance on Saturday', 'The portal will be down for maintenance on Saturday 18 May from 02:00–06:00 EAT.', ['student', 'alumni', 'college_admin'], 'general'),
            (cadmin, 'CoICT Final Exam Timetable Released', 'The timetable for semester 2 finals is now available on the student portal.', ['student'], 'academic'),
            (admin, 'New Mentorship Programme Open', 'Applications for the 2026 mentorship programme are now open. Apply before 30 May.', ['student', 'alumni'], 'general'),
            (cadmin, 'Lab Booking System Update', 'The new online lab booking system goes live Monday. Check your email for login details.', ['student', 'college_admin'], 'academic'),
        ]
        for author, title, content, roles, cat in ann_data:
            Announcement.objects.get_or_create(
                title=title,
                defaults=dict(content=content, created_by=author, target_roles=roles, category=cat, is_published=True,
                              expires_at=timezone.now() + timedelta(days=30)),
            )
        self.stdout.write(f'  Announcements: {len(ann_data)}')

        # ── News ───────────────────────────────────────────────────────────
        news_data = [
            (admin, 'UDSM Ranks Top 10 in Africa', 'The University of Dar es Salaam has been ranked among the top 10 universities in Africa according to the 2026 QS Rankings.'),
            (admin, 'New Engineering Building Inaugurated', 'The state-of-the-art CoET building was officially opened by the Vice Chancellor yesterday.'),
            (cadmin, 'CoICT Partners with Google', 'CoICT has signed an MoU with Google to provide cloud credits and training to students and staff.'),
        ]
        for author, title, content in news_data:
            News.objects.get_or_create(title=title, defaults=dict(content=content, created_by=author, category='technology'))
        self.stdout.write(f'  News: {len(news_data)}')

        # ── Events ─────────────────────────────────────────────────────────
        events_data = [
            (admin, 'Tech Career Fair 2026', 'Annual career fair connecting students with top tech employers across East Africa.', 'conference', 'UDSM Career Office', 'Main Hall, CoICT'),
            (cadmin, 'Hackathon: Smart Campus', '24-hour hackathon focused on building smart campus solutions.', 'workshop', 'CoICT', 'Innovation Hub'),
            (admin, 'Alumni Homecoming Day', 'Annual event welcoming alumni back to campus for networking and reunions.', 'seminar', 'Alumni Office', 'University Grounds'),
        ]
        events = []
        for i, (author, title, desc, cat, organizer, loc) in enumerate(events_data):
            e, _ = Event.objects.get_or_create(
                title=title,
                defaults=dict(description=desc, created_by=author, category=cat, organizer=organizer, location=loc,
                              date=(timezone.now() + timedelta(days=10 + i * 10)).date(),
                              start_time='09:00', max_attendees=100, target_roles=['student', 'alumni'], status='active'),
            )
            events.append(e)
        if events:
            events[0].attendees.add(students[0], students[1])
            events[1].attendees.add(students[0], students[2])
        self.stdout.write(f'  Events: {len(events)}')

        # ── Jobs ───────────────────────────────────────────────────────────
        jobs_data = [
            (alumni[0], 'Junior Software Engineer', 'Vodacom Tanzania', 'Build and maintain mobile and web applications.', 'Technology', 'full_time', 'Dar es Salaam', '800,000 – 1,200,000 TZS'),
            (alumni[1], 'Data Analyst Intern', 'CRDB Bank', 'Analyse transactional data and produce insights for the business team.', 'Finance', 'internship', 'Dar es Salaam', '400,000 TZS'),
            (cadmin, 'UI/UX Designer', 'Azam Media', 'Design intuitive user experiences for our streaming platform.', 'Media', 'contract', 'Dar es Salaam', '600,000 – 900,000 TZS'),
        ]
        for author, title, company, desc, industry, jtype, loc, salary in jobs_data:
            JobOpportunity.objects.get_or_create(
                title=title, company=company,
                defaults=dict(description=desc, posted_by=author, industry=industry, job_type=jtype, location=loc, salary_range=salary, target_roles=['student', 'alumni'], is_active=True, application_deadline=timezone.now() + timedelta(days=30)),
            )
        self.stdout.write(f'  Jobs: {len(jobs_data)}')

        # ── Campus Locations ───────────────────────────────────────────────
        campus_data = [
            ('CoICT Main Building', 'college', 'College of Information and Communication Technologies', -6.7724, 39.2083),
            ('University Library', 'library', 'Main university library with 24-hour reading room.', -6.7710, 39.2070),
            ('Student Health Centre', 'health', 'Free medical services for registered students.', -6.7730, 39.2090),
            ('University Cafeteria', 'cafeteria', 'Main cafeteria serving breakfast, lunch and dinner.', -6.7720, 39.2075),
            ('Sports Complex', 'sports', 'Football pitch, basketball courts and gymnasium.', -6.7740, 39.2060),
        ]
        for name, cat, desc, lat, lng in campus_data:
            CampusLocation.objects.get_or_create(
                name=name,
                defaults=dict(category=cat, description=desc, latitude=lat, longitude=lng, created_by=admin, is_active=True),
            )
        self.stdout.write(f'  Campus Locations: {len(campus_data)}')

        # ── Academics ─────────────────────────────────────────────────────
        deadlines_data = [
            (cadmin, 'Assignment 2 Submission', 'Submit via the LMS portal by midnight.', timezone.now() + timedelta(days=5), 'CS 301', 'assignment'),
            (cadmin, 'Project Proposal Deadline', 'Final year project proposals due to supervisors.', timezone.now() + timedelta(days=12), 'FYP', 'project'),
            (cadmin, 'Semester 2 Exam Registration', 'Register for exams on the student portal.', timezone.now() + timedelta(days=7), '', 'registration'),
        ]
        for author, title, desc, date, course, cat in deadlines_data:
            Deadline.objects.get_or_create(
                title=title,
                defaults=dict(description=desc, deadline_date=date, course=course, category=cat, created_by=author, college='CoICT', target_roles=['student'], is_active=True),
            )

        AlmanacEvent.objects.get_or_create(
            title='Semester 2 Examinations',
            defaults=dict(description='Final examinations for all undergraduate programmes.', start_date=timezone.now() + timedelta(days=45), end_date=timezone.now() + timedelta(days=60), category='exams', academic_year='2025/2026', is_public=True, created_by=admin),
        )
        AlmanacEvent.objects.get_or_create(
            title='Graduation Ceremony 2026',
            defaults=dict(description='Annual graduation ceremony for all graduating students.', start_date=timezone.now() + timedelta(days=90), end_date=timezone.now() + timedelta(days=91), category='graduation', academic_year='2025/2026', is_public=True, created_by=admin),
        )
        self.stdout.write('  Deadlines & Almanac: done')

        # ── Emergency Contacts ─────────────────────────────────────────────
        ec_data = [
            ('UDSM Security Office', '+255222410500', 'security', 'Campus security — available 24/7.', 1),
            ('Student Health Centre', '+255222410600', 'health', 'On-campus clinic for students.', 2),
            ('Fire & Rescue (Tanzania)', '114', 'fire', 'National fire emergency number.', 3),
            ('Police Emergency', '112', 'police', 'National police emergency line.', 4),
        ]
        for name, phone, cat, desc, priority in ec_data:
            EmergencyContact.objects.get_or_create(
                name=name,
                defaults=dict(phone=phone, category=cat, description=desc, priority=priority, visible_to=['student', 'alumni', 'college_admin', 'system_admin']),
            )
        self.stdout.write(f'  Emergency Contacts: {len(ec_data)}')

        # ── Notifications ─────────────────────────────────────────────────
        for student in students:
            Notification.objects.get_or_create(
                user=student, title='Welcome to UCIS',
                defaults=dict(body='Your account is set up. Explore announcements, events and the feed.', source_type='system'),
            )
        self.stdout.write('  Notifications: done')

        # ── Connections & Messages ─────────────────────────────────────────
        conn, _ = Connection.objects.get_or_create(
            sender=students[0], receiver=alumni[0],
            defaults={'status': 'accepted'},
        )
        Connection.objects.get_or_create(
            sender=students[1], receiver=alumni[0],
            defaults={'status': 'pending'},
        )
        if conn.status == 'accepted':
            Message.objects.get_or_create(
                sender=students[0], recipient=alumni[0],
                content='Hi David! Thanks for accepting my connection. Do you have any tips for finding internships?',
                defaults={'is_read': True},
            )
            Message.objects.get_or_create(
                sender=alumni[0], recipient=students[0],
                content="Hey Alice! Sure — start by updating your LinkedIn and applying early. I'm happy to review your CV.",
                defaults={'is_read': False},
            )
        self.stdout.write('  Connections & Messages: done')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  system_admin  -> username: admin          password: Admin1234!')
        self.stdout.write('  college_admin -> username: college_admin  password: Admin1234!')
        self.stdout.write('  student       -> username: alice          password: Pass1234!')
        self.stdout.write('  student       -> username: bob            password: Pass1234!')
        self.stdout.write('  student       -> username: carol          password: Pass1234!')
        self.stdout.write('  alumni        -> username: david_alumni   password: Pass1234!')
        self.stdout.write('  alumni        -> username: eve_alumni     password: Pass1234!')
