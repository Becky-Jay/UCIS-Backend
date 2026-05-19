from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date

from apps.users.models import (
    User, UserProfile, Education, WorkExperience, Expertise, Achievement,
    Relationship, StudentEngagement, AlumniEngagement,
    Permission, UserRole, RolePermission, ExternalSystem, SystemAccess,
)
from apps.alumni.models import AlumniProfile, AlumniConnection
from apps.feed.models import Post, Reaction, Comment, Story
from apps.announcements.models import Announcement
from apps.events.models import Event, EventSubscription
from apps.jobs.models import JobOpportunity, JobApplication
from apps.campus.models import CampusLocation, LocationSearchHistory
from apps.academics.models import Deadline, AlmanacEvent
from apps.notifications.models import Notification
from apps.connections.models import Connection, Message
from apps.news.models import News
from apps.emergency_contacts.models import EmergencyContact
from apps.mentorship.models import MentorshipRequest
from apps.feedback.models import Feedback
from apps.audit_logs.models import AuditLog
from apps.dashboard.models import DashboardPreferences
from apps.organizations.models import StudentsOrganization, OrganizationMember
from apps.chat.models import ChatSession, ChatMessage


class Command(BaseCommand):
    help = 'Seed the database with dummy data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        now = timezone.now()

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
        alumni_users = []
        for uname, email, fn, ln, col in alumni_data:
            u, _ = User.objects.get_or_create(username=uname, defaults=dict(email=email, role='alumni', college=col, first_name=fn, last_name=ln))
            if not u.has_usable_password():
                u.set_password('Pass1234!')
                u.save()
            alumni_users.append(u)

        all_users = [admin, cadmin] + students + alumni_users
        self.stdout.write(f'  Users: {len(all_users)}')

        # ── User Profiles ──────────────────────────────────────────────────
        profile_data = [
            (students[0], 'CoICT', 2025, '+255711000001'),
            (students[1], 'CoET',  2025, '+255711000002'),
            (students[2], 'CoNAS', 2026, '+255711000003'),
            (alumni_users[0], 'CoICT', 2020, '+255711000004'),
            (alumni_users[1], 'CoET',  2021, '+255711000005'),
        ]
        for u, dept, grad_yr, phone in profile_data:
            UserProfile.objects.get_or_create(user=u, defaults=dict(
                first_name=u.first_name, last_name=u.last_name,
                department=dept, graduation_year=grad_yr, phone=phone,
            ))

        # ── Education & Work Experience ────────────────────────────────────
        for u in students:
            Education.objects.get_or_create(user=u, defaults=dict(
                degree_course='BSc Computer Science', college='CoICT', start_year=2021,
            ))
            Expertise.objects.get_or_create(user=u, name='Python', defaults={'proficiency': 3})

        for u in alumni_users:
            Education.objects.get_or_create(user=u, defaults=dict(
                degree_course='BSc Engineering', college=u.college, start_year=2016, end_year=2020,
            ))
            WorkExperience.objects.get_or_create(user=u, company='TechCorp Africa', defaults=dict(
                job_title='Software Engineer', industry='Technology', start_date=date(2020, 7, 1), current=True,
            ))
            Achievement.objects.get_or_create(user=u, title='Best Graduate Award', defaults=dict(
                description='Awarded for academic excellence.', date=date(2020, 11, 15),
            ))

        Relationship.objects.get_or_create(from_user=students[0], to_user=alumni_users[0], defaults={'relationship_type': 'following'})
        Relationship.objects.get_or_create(from_user=students[1], to_user=alumni_users[0], defaults={'relationship_type': 'following'})

        # ── Engagement ────────────────────────────────────────────────────
        for u in students:
            StudentEngagement.objects.get_or_create(user=u, defaults=dict(
                posts_created=2, events_registered=1, mentorship_requests=1, active_mentorships=0,
            ))
        for u in alumni_users:
            AlumniEngagement.objects.get_or_create(user=u, defaults=dict(
                posts_created=3, mentees_count=2, career_advice_sessions=1,
            ))

        self.stdout.write('  Profiles, Education, Work, Engagement: done')

        # ── Alumni Profiles ────────────────────────────────────────────────
        alumni_profiles = []
        alumni_profile_data = [
            (alumni_users[0], 2020, 'Technology', 'Google', 'Senior Engineer'),
            (alumni_users[1], 2021, 'Finance',    'CRDB Bank', 'Data Analyst'),
        ]
        for u, grad, industry, company, position in alumni_profile_data:
            ap, _ = AlumniProfile.objects.get_or_create(user=u, defaults=dict(
                graduation_year=grad, industry=industry, company=company,
                position=position, is_verified=True, joined_mentorship=True,
            ))
            alumni_profiles.append(ap)

        if len(alumni_profiles) >= 2:
            AlumniConnection.objects.get_or_create(
                alumni_1=alumni_profiles[0], alumni_2=alumni_profiles[1],
                defaults={'status': 'accepted'},
            )
        self.stdout.write('  Alumni Profiles & Connections: done')

        # ── Permissions, Roles, Role Permissions ──────────────────────────
        perm_data = [
            ('view_announcements', 'Can view announcements'),
            ('manage_users',       'Can create, edit and deactivate users'),
            ('post_news',          'Can publish news articles'),
        ]
        perms = {}
        for pname, pdesc in perm_data:
            p, _ = Permission.objects.get_or_create(permission_name=pname, defaults={'description': pdesc})
            perms[pname] = p

        for u in all_users:
            UserRole.objects.get_or_create(user=u, role_name=u.role)

        for pname, p in perms.items():
            RolePermission.objects.get_or_create(role_name='system_admin', permission=p)
        RolePermission.objects.get_or_create(role_name='college_admin', permission=perms['view_announcements'])
        RolePermission.objects.get_or_create(role_name='college_admin', permission=perms['post_news'])

        self.stdout.write('  Permissions & Role Permissions: done')

        # ── External Systems & System Access ──────────────────────────────
        ext_systems_data = [
            ('Student Portal',    'https://portal.udsm.ac.tz',   'portal',  'Official student information portal'),
            ('LMS (Moodle)',      'https://lms.udsm.ac.tz',      'book',    'Online learning management system'),
            ('Library Catalogue', 'https://library.udsm.ac.tz',  'library', 'Search and reserve books online'),
        ]
        ext_systems = []
        for sname, surl, icon, desc in ext_systems_data:
            es, _ = ExternalSystem.objects.get_or_create(system_name=sname, defaults=dict(
                system_url=surl, icon=icon, description=desc, is_active=True,
            ))
            ext_systems.append(es)

        for es in ext_systems:
            for role in ('student', 'alumni', 'college_admin', 'system_admin'):
                SystemAccess.objects.get_or_create(system=es, role_name=role)

        self.stdout.write('  External Systems & System Access: done')

        # ── Dashboard Preferences ─────────────────────────────────────────
        for u in all_users:
            DashboardPreferences.objects.get_or_create(user=u, defaults=dict(
                show_announcements=True, show_events=True, show_quick_links=True, layout_type='grid',
            ))
        self.stdout.write('  Dashboard Preferences: done')

        # ── Posts, Reactions, Comments ────────────────────────────────────
        posts_data = [
            (students[0], 'Looking for study group', 'Anyone interested in forming a DSA study group?', ['student'], ['study', 'DSA']),
            (students[1], 'CoET Lab computers down', 'Computers in Lab 3 are down. Reported to technician.', ['student', 'college_admin'], ['lab']),
            (alumni_users[0], 'Career tip: internships matter', 'Landing my first job was easier because of my internship. Start early!', ['student', 'alumni'], ['career']),
        ]
        posts = []
        for author, title, content, roles, tags in posts_data:
            p, _ = Post.objects.get_or_create(title=title, defaults=dict(
                content=content, posted_by=author, target_roles=roles, tags=tags, college=author.college,
            ))
            posts.append(p)

        if posts:
            Reaction.objects.get_or_create(post=posts[0], user=students[1], defaults={'reaction_type': 'like'})
            Reaction.objects.get_or_create(post=posts[2], user=students[0], defaults={'reaction_type': 'celebrate'})
            Comment.objects.get_or_create(post=posts[0], user=students[2], defaults={'content': "Count me in, struggling with graphs."})
            Comment.objects.get_or_create(post=posts[2], user=students[0], defaults={'content': 'Very motivating, thank you!'})

        Story.objects.get_or_create(posted_by=students[0], defaults=dict(
            content='Just submitted my final year project proposal!', media_type='text',
            background_color='#1a1a2e', expires_at=now + timedelta(hours=20),
        ))
        Story.objects.get_or_create(posted_by=alumni_users[0], defaults=dict(
            content='Attending a tech summit in Nairobi this week.', media_type='text',
            background_color='#16213e', expires_at=now + timedelta(hours=18),
        ))
        self.stdout.write(f'  Posts & Stories: done')

        # ── Announcements ─────────────────────────────────────────────────
        ann_data = [
            (admin,  'System Maintenance Saturday',   'Portal down 02:00–06:00 EAT for maintenance.', ['student', 'alumni'], 'general'),
            (cadmin, 'CoICT Final Exam Timetable',    'Semester 2 timetable is on the student portal.', ['student'], 'academic'),
            (admin,  'Mentorship Programme Open',     'Applications open until 30 May 2026.', ['student', 'alumni'], 'general'),
        ]
        for author, title, content, roles, cat in ann_data:
            Announcement.objects.get_or_create(title=title, defaults=dict(
                content=content, created_by=author, target_roles=roles,
                category=cat, is_published=True, expires_at=now + timedelta(days=30),
            ))
        self.stdout.write(f'  Announcements: done')

        # ── News ──────────────────────────────────────────────────────────
        news_data = [
            (admin,  'UDSM Ranks Top 10 in Africa',      'Ranked among the top 10 African universities in 2026 QS Rankings.', 'academics'),
            (admin,  'New Engineering Building Opens',    'The CoET building was officially opened by the Vice Chancellor.', 'academics'),
            (cadmin, 'CoICT Partners with Google',        'MoU signed to provide cloud credits and training to students.', 'technology'),
        ]
        for author, title, content, cat in news_data:
            News.objects.get_or_create(title=title, defaults=dict(
                content=content, created_by=author, category=cat, is_published=True, college=['CoICT'], target_roles=['student', 'alumni'],
            ))
        self.stdout.write('  News: done')

        # ── Events & Subscriptions ────────────────────────────────────────
        events_data = [
            (admin,  'Tech Career Fair 2026',  'Career fair connecting students with tech employers.', 'conference', 'UDSM Career Office', 'Main Hall, CoICT', 10),
            (cadmin, 'Hackathon: Smart Campus','24-hour hackathon for smart campus solutions.', 'workshop', 'CoICT', 'Innovation Hub', 20),
            (admin,  'Alumni Homecoming Day',  'Annual networking and reunion event for alumni.', 'seminar', 'Alumni Office', 'University Grounds', 30),
        ]
        events = []
        for author, title, desc, cat, organizer, loc, days in events_data:
            e, _ = Event.objects.get_or_create(title=title, defaults=dict(
                description=desc, created_by=author, category=cat, organizer=organizer,
                location=loc, date=(now + timedelta(days=days)).date(),
                start_time='09:00', max_attendees=100,
                target_roles=['student', 'alumni'], status='active',
            ))
            events.append(e)

        if events:
            events[0].attendees.add(students[0], students[1])
            for u in [students[0], students[1]]:
                EventSubscription.objects.get_or_create(event=events[0], user=u, defaults={'reminder_enabled': True})
            EventSubscription.objects.get_or_create(event=events[1], user=students[2], defaults={'reminder_enabled': False})
        self.stdout.write('  Events & Subscriptions: done')

        # ── Jobs & Applications ───────────────────────────────────────────
        jobs_data = [
            (alumni_users[0], 'Junior Software Engineer', 'Vodacom Tanzania', 'Build mobile and web apps.', 'Technology', 'full_time', 'Dar es Salaam', '800k–1.2M TZS'),
            (alumni_users[1], 'Data Analyst Intern',      'CRDB Bank',        'Analyse transactional data.', 'Finance', 'internship', 'Dar es Salaam', '400k TZS'),
            (cadmin,          'UI/UX Designer',            'Azam Media',       'Design streaming UX.',       'Media', 'contract', 'Dar es Salaam', '600k–900k TZS'),
        ]
        job_objs = []
        for author, title, company, desc, industry, jtype, loc, salary in jobs_data:
            j, _ = JobOpportunity.objects.get_or_create(title=title, company=company, defaults=dict(
                description=desc, posted_by=author, industry=industry, job_type=jtype,
                location=loc, salary_range=salary, target_roles=['student', 'alumni'],
                is_active=True, application_deadline=(now + timedelta(days=30)).date(),
            ))
            job_objs.append(j)

        if job_objs:
            JobApplication.objects.get_or_create(job=job_objs[0], applicant=students[0], defaults={'cover_letter': 'I am very interested in this role.', 'status': 'applied'})
            JobApplication.objects.get_or_create(job=job_objs[1], applicant=students[1], defaults={'cover_letter': 'Data analysis is my passion.', 'status': 'reviewed'})
        self.stdout.write('  Jobs & Applications: done')

        # ── Campus Locations & Search History ─────────────────────────────
        campus_data = [
            ('CoICT Main Building', 'academic', 'College of ICT main block.', -6.7724, 39.2083),
            ('University Library',  'library',  'Main library, 24-hr reading room.', -6.7710, 39.2070),
            ('Student Health Centre','medical', 'Free medical services for students.', -6.7730, 39.2090),
            ('University Cafeteria', 'food',    'Serves breakfast, lunch and dinner.', -6.7720, 39.2075),
            ('Sports Complex',       'sports',  'Football pitch, basketball and gym.', -6.7740, 39.2060),
        ]
        campus_locs = []
        for name, cat, desc, lat, lng in campus_data:
            cl, _ = CampusLocation.objects.get_or_create(name=name, defaults=dict(
                category=cat, description=desc, latitude=lat, longitude=lng,
                created_by=admin, is_active=True,
            ))
            campus_locs.append(cl)

        if campus_locs:
            LocationSearchHistory.objects.get_or_create(location=campus_locs[0], user=students[0], defaults={'search_query': 'CoICT building'})
            LocationSearchHistory.objects.get_or_create(location=campus_locs[1], user=students[1], defaults={'search_query': 'library'})
            LocationSearchHistory.objects.get_or_create(location=campus_locs[2], user=students[2], defaults={'search_query': 'health centre'})
        self.stdout.write('  Campus Locations & Search History: done')

        # ── Academics ────────────────────────────────────────────────────
        deadlines_data = [
            (cadmin, 'Assignment 2 Submission',      'Submit via LMS portal by midnight.', now + timedelta(days=5),  'CS 301',  'assignment'),
            (cadmin, 'Project Proposal Deadline',    'FYP proposals due to supervisors.',  now + timedelta(days=12), 'FYP',     'project'),
            (cadmin, 'Semester 2 Exam Registration', 'Register on the student portal.',    now + timedelta(days=7),  '',        'registration'),
        ]
        for author, title, desc, deadline, course, cat in deadlines_data:
            Deadline.objects.get_or_create(title=title, defaults=dict(
                description=desc, deadline_date=deadline, course=course, category=cat,
                created_by=author, college='CoICT', target_roles=['student'], is_active=True,
            ))

        AlmanacEvent.objects.get_or_create(title='Semester 2 Examinations', defaults=dict(
            description='Final exams for all undergrads.', start_date=(now + timedelta(days=45)).date(),
            end_date=(now + timedelta(days=60)).date(), category='exam_period',
            academic_year='2025/2026', is_public=True, created_by=admin,
        ))
        AlmanacEvent.objects.get_or_create(title='Graduation Ceremony 2026', defaults=dict(
            description='Annual graduation ceremony.', start_date=(now + timedelta(days=90)).date(),
            end_date=(now + timedelta(days=91)).date(), category='graduation',
            academic_year='2025/2026', is_public=True, created_by=admin,
        ))
        self.stdout.write('  Deadlines & Almanac: done')

        # ── Emergency Contacts ────────────────────────────────────────────
        ec_data = [
            ('UDSM Security Office',  '+255222410500', 'Security', 'Campus security, available 24/7.', 1),
            ('Student Health Centre', '+255222410600', 'Medical',  'On-campus clinic for students.',   2),
            ('Fire & Rescue',         '114',           'Fire',     'National fire emergency number.',  3),
        ]
        for name, phone, cat, desc, priority in ec_data:
            EmergencyContact.objects.get_or_create(name=name, defaults=dict(
                phone=phone, category=cat, description=desc, priority=priority,
                visible_to=['student', 'alumni', 'college_admin', 'system_admin'],
            ))
        self.stdout.write('  Emergency Contacts: done')

        # ── Mentorship Requests ───────────────────────────────────────────
        MentorshipRequest.objects.get_or_create(student=students[0], alumni=alumni_users[0], defaults=dict(
            status='pending', message='Hi David, I would love guidance on getting into tech.',
        ))
        MentorshipRequest.objects.get_or_create(student=students[1], alumni=alumni_users[0], defaults=dict(
            status='approved', message='I am interested in data engineering mentorship.',
        ))
        MentorshipRequest.objects.get_or_create(student=students[2], alumni=alumni_users[1], defaults=dict(
            status='pending', message='Would appreciate career advice in finance tech.',
        ))
        self.stdout.write('  Mentorship Requests: done')

        # ── Notifications ─────────────────────────────────────────────────
        for u in students:
            Notification.objects.get_or_create(user=u, title='Welcome to UCIS', defaults=dict(
                body='Your account is ready. Explore announcements, events and the feed.',
                source_type='general', source_id='0',
            ))
        Notification.objects.get_or_create(user=students[0], title='Mentorship Request Sent', defaults=dict(
            body='Your request to David Nkrumah has been sent.',
            source_type='mentorship', source_id='1',
        ))
        self.stdout.write('  Notifications: done')

        # ── Connections & Messages ────────────────────────────────────────
        conn, _ = Connection.objects.get_or_create(sender=students[0], receiver=alumni_users[0], defaults={'status': 'accepted'})
        Connection.objects.get_or_create(sender=students[1], receiver=alumni_users[0], defaults={'status': 'pending'})
        Connection.objects.get_or_create(sender=students[2], receiver=alumni_users[1], defaults={'status': 'accepted'})
        if conn.status == 'accepted':
            Message.objects.get_or_create(
                sender=students[0], recipient=alumni_users[0],
                content='Hi David! Any tips for finding internships?',
                defaults={'is_read': True},
            )
            Message.objects.get_or_create(
                sender=alumni_users[0], recipient=students[0],
                content="Update your LinkedIn and apply early. Happy to review your CV.",
                defaults={'is_read': False},
            )
        self.stdout.write('  Connections & Messages: done')

        # ── Feedback ─────────────────────────────────────────────────────
        Feedback.objects.get_or_create(user=students[0], subject='App loads slowly', defaults=dict(
            category='bug', message='The feed page takes over 5 seconds to load on mobile.', status='pending',
        ))
        Feedback.objects.get_or_create(user=students[1], subject='Add dark mode', defaults=dict(
            category='suggestion', message='A dark mode option would be very helpful at night.', status='pending',
        ))
        Feedback.objects.get_or_create(user=alumni_users[0], subject='Great platform!', defaults=dict(
            category='praise', message='The mentorship feature is excellent. Keep it up.', status='reviewed',
        ))
        self.stdout.write('  Feedback: done')

        # ── Audit Logs ────────────────────────────────────────────────────
        AuditLog.objects.get_or_create(action='USER_LOGIN', performed_by=admin, defaults=dict(
            role='system_admin', target_resource='User', target_id=str(admin.id),
            details='Admin logged in.', ip_address='127.0.0.1',
        ))
        AuditLog.objects.get_or_create(action='ANNOUNCEMENT_CREATED', performed_by=cadmin, defaults=dict(
            role='college_admin', target_resource='Announcement', target_id='1',
            details='Created exam timetable announcement.', ip_address='192.168.1.10',
        ))
        AuditLog.objects.get_or_create(action='USER_DEACTIVATED', performed_by=admin, defaults=dict(
            role='system_admin', target_resource='User', target_id='99',
            details='Deactivated test account.', ip_address='127.0.0.1',
        ))
        self.stdout.write('  Audit Logs: done')

        # ── Organizations & Members ───────────────────────────────────────
        org_data = [
            ('CoICT Programming Club',   'Club for programming enthusiasts.',       'prog@coict.ac.tz'),
            ('UDSM Robotics Society',     'Builds and competes with robots.',        'robotics@udsm.ac.tz'),
            ('Entrepreneurship Network',  'Connects student entrepreneurs.',         'entre@udsm.ac.tz'),
        ]
        orgs = []
        for oname, odesc, oemail in org_data:
            org, _ = StudentsOrganization.objects.get_or_create(org_name=oname, defaults=dict(
                description=odesc, contact_email=oemail, status='active',
            ))
            orgs.append(org)

        if orgs:
            OrganizationMember.objects.get_or_create(org=orgs[0], user=students[0], defaults={'role': 'President'})
            OrganizationMember.objects.get_or_create(org=orgs[0], user=students[1], defaults={'role': 'Member'})
            OrganizationMember.objects.get_or_create(org=orgs[1], user=students[2], defaults={'role': 'Member'})
            OrganizationMember.objects.get_or_create(org=orgs[2], user=students[0], defaults={'role': 'Secretary'})
        self.stdout.write('  Organizations & Members: done')

        # ── Chat Sessions & Messages ──────────────────────────────────────
        session1, _ = ChatSession.objects.get_or_create(
            user=students[0],
            defaults={'status': 'ended', 'ended_at': now - timedelta(minutes=30)},
        )
        ChatMessage.objects.get_or_create(session=session1, sender_type='user', message_text='What is the deadline for assignment 2?', defaults={})
        ChatMessage.objects.get_or_create(session=session1, sender_type='bot',  message_text='Assignment 2 is due in 5 days. Check the Deadlines section for details.', defaults={})

        session2, _ = ChatSession.objects.get_or_create(
            user=students[1],
            defaults={'status': 'active'},
        )
        ChatMessage.objects.get_or_create(session=session2, sender_type='user', message_text='Where is the student health centre?', defaults={})
        ChatMessage.objects.get_or_create(session=session2, sender_type='bot',  message_text='The Student Health Centre is near the main gate. See the Campus Map for directions.', defaults={})
        self.stdout.write('  Chat Sessions & Messages: done')

        # ── Summary ───────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  system_admin  -> username: admin          password: Admin1234!')
        self.stdout.write('  college_admin -> username: college_admin  password: Admin1234!')
        self.stdout.write('  student       -> username: alice          password: Pass1234!')
        self.stdout.write('  student       -> username: bob            password: Pass1234!')
        self.stdout.write('  student       -> username: carol          password: Pass1234!')
        self.stdout.write('  alumni        -> username: david_alumni   password: Pass1234!')
        self.stdout.write('  alumni        -> username: eve_alumni     password: Pass1234!')
