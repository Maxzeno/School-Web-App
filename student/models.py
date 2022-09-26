from django.db import models
from shortuuid import ShortUUID
from management.models import User

# Create your models here.


class ClassRoom(models.Model):
	name = models.CharField(max_length=255, blank=True)


class Session(models.Model):
	session = models.CharField(max_length=50, unique=True)
	
	def __str__(self):
		return self.session

class Subject(models.Model):
	name = models.CharField(max_length=150, unique=True, null=False)

	def __str__(self):
		return self.name


class Exam(models.Model):
	exam_name = models.CharField(max_length=150)
	exam_session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
	exam_term = models.CharField(max_length=150)
	exam_starts = models.CharField(max_length=150)
	exam_ends = models.CharField(max_length=150)
	next_term_begins = models.CharField(max_length=150)
	next_term_ends = models.CharField(max_length=150)
	comment = models.CharField(max_length=150, blank=True)

	def next_term_begins_dash(self):
		if self.next_term_begins:
			month, day, year = self.next_term_begins.split('/')
			return f'{day}-{month}-{year}'
		return ''

	def __str__(self):
		return self.exam_name + ' ' + self.exam_session.session + ' ' + self.exam_term


class PassMark(models.Model):
	mark = models.IntegerField()
	period = models.CharField(max_length=150)
	category = models.CharField(max_length=150)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
	session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)

	def get_subject(self):
		if self.subject:
			return self.subject.name
		return None

	def __str__(self):
		return self.mark + ' ' + self.period + ' ' + self.category + ' ' + self.subject.name + ' ' + self.session.session


class JustClass(models.Model):
	#### the_section = models.CharField(max_length=255, blank=True) ##models.ManyToManyField(Section, blank=True, null=True)
	the_class = models.CharField(primary_key=True, max_length=150, blank=True)
	subject = models.ManyToManyField(Subject, blank=True)

	def __str__(self):
		return '<'+ self.the_class +'>'


class Class(models.Model):
	the_section = models.CharField(max_length=255, blank=True)
	the_class = models.ForeignKey(JustClass, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return (self.the_class.the_class if self.the_class else 'N/A') + ' ' + self.the_section 

	class Meta:
		unique_together = ('the_section', 'the_class')


class HowDidYouHearAboutCDSSE(models.Model):
	how = models.CharField(max_length=255, blank=True)
	referrer_name = models.CharField(max_length=150, blank=True)
	referrer_phone_number = models.CharField(max_length=150, blank=True)


class PreviousSchoolDetail(models.Model):
	name_of_school = models.CharField(max_length=150, blank=True)
	email_address = models.CharField(max_length=150, blank=True)
	phone_number = models.CharField(max_length=150, blank=True)
	address = models.CharField(max_length=150, blank=True)
	head_teacher_name = models.CharField(max_length=150, blank=True)


class EmergencyContactDetail(models.Model):
	title = models.CharField(max_length=150, blank=True)
	name = models.CharField(max_length=150, blank=True)
	mobile_phone = models.CharField(max_length=150, blank=True)
	office_phone = models.CharField(max_length=150, blank=True)
	full_postal_address = models.CharField(max_length=150, blank=True)
	email_address = models.CharField(max_length=150, blank=True)
	business_address = models.CharField(max_length=150, blank=True)


class Guardian(models.Model):
	title = models.CharField(max_length=150, blank=True)
	name = models.CharField(max_length=150, blank=True)
	mobile_phone = models.CharField(max_length=150, blank=True)
	occupation = models.CharField(max_length=150, blank=True)
	office_phone = models.CharField(max_length=150, blank=True)
	full_postal_address = models.CharField(max_length=150, blank=True)
	email_address = models.CharField(max_length=150, blank=True)
	business_address = models.CharField(max_length=150, blank=True)
	relationship_to_child = models.CharField(max_length=150, blank=True)


class Parent(models.Model):
	title = models.CharField(max_length=150, blank=True)
	name = models.CharField(max_length=150, blank=True)
	password = models.CharField(max_length=150, blank=True, null=True)
	gender = models.CharField(max_length=150, blank=True)
	state_of_origin = models.CharField(max_length=150, blank=True)
	birth_day = models.CharField(max_length=150, blank=True)
	birth_month = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	occupation = models.CharField(max_length=150, blank=True)
	office_phone = models.CharField(max_length=150, blank=True)
	address = models.CharField(max_length=150, blank=True)
	email_address = models.CharField(max_length=150, blank=True)
	business_address = models.CharField(max_length=150, blank=True)
	blood_group = models.CharField(max_length=150, blank=True)


class EntryDetails(models.Model):
	proposed_date_of_entry = models.CharField(max_length=150, blank=True)
	session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
	term = models.CharField(max_length=150, blank=True)
	medical_conditions = models.CharField(max_length=150, blank=True)


class Siblings(models.Model):
	name1 = models.CharField(max_length=150, blank=True)
	student_class1 = models.CharField(max_length=150, blank=True)
	date_of_birth1 = models.DateField(blank=True)
	name2 = models.CharField(max_length=150, blank=True)
	student_class2 = models.CharField(max_length=150, blank=True)
	date_of_birth2 = models.DateField(blank=True)
	name3 = models.CharField(max_length=150, blank=True)
	student_class3 = models.CharField(max_length=150, blank=True)
	date_of_birth3 = models.DateField(blank=True)


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student')
	student_id = models.CharField(primary_key=True, max_length=100, unique=True)
	passport_photo = models.ImageField(upload_to='images/', blank=True, null=True)
	student_class_room = models.ForeignKey(Class, on_delete=models.CASCADE, 
		null=True, related_name="parent", blank=True) ##to be added
	
	name = models.CharField(max_length=150, blank=True)
	# email = models.EmailField(max_length=150, blank=True)
	birthday = models.CharField(max_length=150, blank=True, null=True)
	place_of_birth = models.CharField(max_length=150, blank=True)
	nationality = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=150, blank=True)
	blood_group = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	address = models.CharField(max_length=150, blank=True)
	religion = models.CharField(max_length=150, blank=True)
	child_current_address = models.CharField(max_length=150, blank=True)
	currently_resides_with = models.CharField(max_length=150, blank=True)
	left_school = models.BooleanField(default=False)

	subject = models.ManyToManyField(Subject, blank=True)
	siblings = models.OneToOneField(Siblings, on_delete=models.CASCADE, null=True, blank=True)
	entry_details = models.OneToOneField(EntryDetails, on_delete=models.CASCADE, null=True, blank=True)
	parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, related_name="parent", blank=True)
	guardian = models.OneToOneField(Guardian, on_delete=models.CASCADE, null=True, blank=True)
	emergency_contact_detail = models.OneToOneField(EmergencyContactDetail, on_delete=models.CASCADE, null=True, blank=True)
	previous_school_detail = models.OneToOneField(PreviousSchoolDetail, on_delete=models.CASCADE, null=True, blank=True)
	how_did_you_hear_about_CDSSE = models.OneToOneField(HowDidYouHearAboutCDSSE, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return f"<{self.student_id}: {self.name}>"

	def replace_slash_with_dash(self):
		return self.pk.replace('/', '-')

	def get_photo(self):
		"""should reture student passport or placeholder image"""
		if self.passport_photo:
			return self.passport_photo.url
		return '/static/portal/uploads/users/placeholder.jpg'


