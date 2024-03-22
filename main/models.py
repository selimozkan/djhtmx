from django.db import models
from django.utils import timezone
import uuid

GENDER_CHOICES = [
  ("Female", "Female"),
  ("Male", "Male"),
  ("Other", "Other")
]

# Upload the file under related table seperated folder
# with unique uuid file name
def upload_to(instance, filename):
  if instance.related_table == "":
    folder = "misc"
  else:
    folder = instance.related_table
  ext = filename.split('.')[-1]
  fname = uuid.uuid4()

  return '{}/{}.{}'.format(folder,fname,ext)


# STORAGE

class Media(models.Model):
  title = models.CharField("Title", max_length=150)
  related_table = models.CharField("Related Table", max_length=50, blank=True, default="misc")
  related_id = models.IntegerField("Related Id", blank=True, default=0)
  file_url = models.FileField(upload_to=upload_to, blank=True, null=True)

  def delete(self, using=None, keep_parents=False):
    self.file_url.storage.delete(self.file_url.name)
    super().delete()

  class Meta:
    db_table = "media"
    managed = True
    verbose_name = "Media"
    verbose_name_plural = "Medias"

  def __str__(self):
    return "%s" % self.title


# CONSTANTS

class Airline(models.Model):
  title = models.CharField(max_length=75, unique=True)

  class Meta:
    db_table = "airline"
    managed = True
    verbose_name = "Airline"
    verbose_name_plural = "Airlines"

  def __str__(self):
    return "%s" % self.title

class Hotel(models.Model):
  title = models.CharField("Title", max_length=100)
  description = models.TextField("Description", blank=True)
  city = models.CharField("City", max_length=50)
  region = models.CharField("Region", max_length=50)
  contact_name = models.CharField("Contact Name", max_length=75)
  contact_phone = models.CharField("Contact Phone", max_length=20, blank=True)
  contact_email = models.CharField("Contact Email", max_length=250, blank=True)

  class Meta:
    db_table = "hotel"
    managed = True
    verbose_name = "Hotel"
    verbose_name_plural = "Hotels"

  def __str__(self):
    return "{}-{}/{}".format(self.title,self.city,self.region)

class Hospital(models.Model):
  title = models.CharField("Title", max_length=100)
  description = models.TextField("Description", blank=True, null=True)
  city = models.CharField("City", max_length=50)
  region = models.CharField("Region", max_length=50)
  contact_name = models.CharField("Contact Name", max_length=75, blank=True, null=True)
  contact_phone = models.CharField("Contact Phone", max_length=20, blank=True, null=True)
  contact_email = models.CharField("Contact Email", max_length=250, blank=True, null=True)

  class Meta:
    db_table = 'hospital'
    managed = True
    verbose_name = 'Hospital'
    verbose_name_plural = 'Hospitals'

  def __str__(self):
    return "{}-{}/{}".format(self.title,self.city,self.region)

class Clinic(models.Model):
  title = models.CharField("Title", max_length=100)
  description = models.TextField("Description", blank=True)
  contact_name = models.CharField("Contact name", max_length=75)
  contact_phone = models.CharField("Contact Phone", max_length=20, blank=True)
  contact_email = models.CharField("Contact Email", max_length=250, blank=True)

  class Meta:
    db_table = "clinic"
    managed = True
    verbose_name = "Clinic"
    verbose_name_plural = "Clinics"

  def __str__(self):
    return "%s" % self.title

class Doctor(models.Model):
  abbr = models.CharField("Abbreviation", max_length=30)
  name = models.CharField("Name", max_length=70)
  expertise = models.CharField("Expertise", max_length=75)
  phone = models.CharField("Phone", max_length=20, blank=True)
  email = models.CharField("Email", max_length=250, blank=True)

  class Meta:
    db_table = "doctor"
    managed = True
    verbose_name = "Doctor"
    verbose_name_plural = "Doctors"

  def __str__(self):
    return self.abbr + " - " + self.name

class Process(models.Model):
  title = models.CharField("Title", max_length=150)
  description = models.TextField("Description", blank=True)

  class Meta:
    db_table = "process"
    managed = True
    verbose_name = "Process"
    verbose_name_plural = "Processes"

  def __str__(self):
    return "%s" % self.title



# CRM

class Client(models.Model):
  name = models.CharField("Name", max_length=75)
  gender = models.CharField("Gender", max_length=10, default="Female", choices=GENDER_CHOICES)
  nationality = models.CharField("Nationality", max_length=50)
  passport_no = models.CharField("Passport No", max_length=25)
  phone = models.CharField("Phone", max_length=20)
  email = models.CharField("Email", max_length=250, blank=True)
  city = models.CharField("City", max_length=50)
  region = models.CharField("Region", max_length=50, blank=True)
  address = models.TextField("Address", blank=True)

  class Meta:
    db_table = 'client'
    managed = True
    verbose_name = 'Client'
    verbose_name_plural = 'Clients'

  def __str__(self):
    return "%s" % self.name

class ClientCurrent(models.Model):
  client = models.ForeignKey("Client", verbose_name="Client", on_delete=models.CASCADE)
  date = models.DateField("Date", default=timezone.now)
  description = models.CharField("Description", max_length=250, blank=True)
  debt = models.DecimalField("Debt", max_digits=9, decimal_places=2, default=0)
  credit = models.DecimalField("Credit", max_digits=9, decimal_places=2, default=0)

  class Meta:
    db_table = 'client_current'
    managed = True
    verbose_name = 'Client Current'
    verbose_name_plural = 'Client Currents'

  def __str__(self):
    return self.client.name

class Companion(models.Model):
  request = models.ForeignKey("Request", verbose_name="Request", on_delete=models.CASCADE)
  name = models.CharField("Name", max_length=75)
  gender = models.CharField("Gender", max_length=10, default="Female", choices=GENDER_CHOICES)
  phone = models.CharField("Phone", max_length=20, blank=True)
  nationality = models.CharField("Nationality", max_length=50, blank=True)
  passport_no = models.CharField("Passport No", max_length=25, blank=True)

  class Meta:
    db_table = 'companion'
    managed = True
    verbose_name = 'Companion'
    verbose_name_plural = 'Companions'

  def __str__(self):
    return "{}-{}-{}-{}".format(self.request,self.name,self.phone,self.passport_no)


# LOGISTICS

class Flight(models.Model):
  request = models.ForeignKey("Request", verbose_name="Request", on_delete=models.CASCADE)
  direction = models.CharField("Direction", max_length=10, choices=[("Arrival", "Arrival"), ("Departure", "Departure")])
  date = models.DateField("Date", default=timezone.now)
  time = models.TimeField("Time", default=timezone.now)
  airline = models.ForeignKey("Airline", verbose_name="Airline", on_delete=models.SET_NULL, null=True)
  flight_no = models.CharField("Flight No", max_length=25)

  class Meta:
    db_table = 'flight'
    managed = True
    verbose_name = 'Flight'
    verbose_name_plural = 'Flights'

  def __str__(self):
    return self.request.request_date + " - " + self.airline.title + " - " + self.flight_no

class Accomodation(models.Model):
  request = models.ForeignKey("Request", verbose_name="Request", on_delete=models.CASCADE)
  hotel = models.ForeignKey("Hotel", verbose_name="Hotel", on_delete=models.SET_NULL, null=True)
  checkin_date = models.DateField("Checkin Date", null=True)
  checkout_date = models.DateField("Checkout Date", null=True)
  room_type = models.CharField("Room Type", max_length=25, choices=[
    ("Single", "Single"), ("Double", "Double"),
    ("Triple", "Triple"), ("Apart", "Apart"), ("Suit", "Suit")
  ])
  accomodation_type = models.CharField("Accomodation Type", max_length=50, choices=[
    ("Half Board", "Half Board"), ("Full Board", "Full Board"),
    ("All Inclusive", "All Inclusive")
  ])
  notes = models.TextField("Notes", blank=True)

  class Meta:
    db_table = 'accomodation'
    managed = True
    verbose_name = 'Accomodation'
    verbose_name_plural = 'Accomodations'

  def __str__(self):
    return "{}-{}-{}-{}".format(self.request,self.hotel,self.checkin_date,self.checkout_date)

class Transfer(models.Model):
  client = models.ForeignKey("Client", verbose_name="Client", on_delete=models.CASCADE)
  pickup_date = models.DateField("Pickup Date", default=timezone.now)
  pickup_time = models.TimeField("Pickup Time", default=timezone.now)
  pickup_address = models.TextField("Pickup Address", default="-")
  pickup_lat = models.CharField("Pickup Lattitude", max_length=10, blank=True)
  pickup_lon = models.CharField("Pickup Longtitude", max_length=10, blank=True)
  car_plate = models.CharField("Car Plate", max_length=20, blank=True)
  car_type = models.CharField("Car Type", max_length=20, blank=True, choices=[("Car", "Car"), ("Minibus", "Minibus"), ("Bus", "Bus")])
  driver_name = models.CharField("Driver Name", max_length=75, blank=True)
  driver_phone = models.CharField("Driver Phone", max_length=20, blank=True)
  rented_company = models.CharField("Rented Company", max_length=75, blank=True)
  status = models.CharField("Status", max_length=10, default="Open", choices=[
    ("Open", "Open"), ("Reserved", "Reserved"),
    ("Finished", "Finished"), ("Cancelled", "Cancelled")
  ])

  class Meta:
    db_table = 'transfer'
    managed = True
    verbose_name = 'Transfer'
    verbose_name_plural = 'Transfers'

  def __str__(self):
    return "{}-{}-{}-{}-{}".format(self.client,self.pickup_date,self.pickup_time,self.driver_name,self.driver_phone)


# ACTIONS

class Request(models.Model):
  client = models.ForeignKey("Client", verbose_name="Client", on_delete=models.CASCADE)
  request_date = models.DateField("Request Date", default=timezone.now)
  process = models.ForeignKey("Process", verbose_name="Process", on_delete=models.PROTECT)
  process_date = models.DateField("Process Date", null=True, blank=True)
  notes = models.TextField("Notes", blank=True, null=True)
  status = models.CharField("Status", max_length=10, default="Open", choices=[
    ("Open", "Open"),
    ("Planned", "Planned"),
    ("Ongoing", "Ongoing"),
    ("Finished", "Finished"),
    ("Cancelled", "Cancelled")
  ])

  class Meta:
    db_table = 'request'
    managed = True
    verbose_name = 'Request'
    verbose_name_plural = 'Requests'

  def __str__(self):
    return self.client + " - " + self.request_date + " - " + self.status

class Transaction(models.Model):
  request = models.ForeignKey("Request", verbose_name="Request", on_delete=models.CASCADE)
  date = models.DateField("Transaction Date", default=timezone.now)
  time = models.TimeField("Transaction Time", default=timezone.now)
  hospital = models.ForeignKey("Hospital", verbose_name="Hospital", on_delete=models.SET_NULL, null=True)
  clinic = models.ForeignKey("Clinic", verbose_name="Clinic", on_delete=models.SET_NULL, null=True)
  doctor = models.ForeignKey("Doctor", verbose_name="Doctor", on_delete=models.SET_NULL, null=True)
  price = models.DecimalField("Price", max_digits=9, decimal_places=2, default=0)
  notes = models.TextField("Notes", blank=True, null=True)
  status = models.CharField("Status", max_length=50, default="Open", choices=[
    ("Open", "Open"),
    ("Finished", "Finished"),
    ("Cancelled", "Cancelled")
  ])

  class Meta:
    db_table = 'transaction'
    managed = True
    verbose_name = 'Transaction'
    verbose_name_plural = 'Transactions'

  def __str__(self):
    pass
