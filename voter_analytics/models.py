# voter_analytics/models.py
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Stores/Represents a registered vote for the election in Newton, MA. 
    Last Name, First Name, Residential Address - Street Number, Street Name
    Apartment Number, Zip Code, Date of Birth, Date of Registration, 
    Party Affiliation, Precinct Number
    '''
    # personal information 
    last_name = models.TextField()
    first_name = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # residential address information
    address_street_number = models.IntegerField()
    address_street_name = models.TextField()
    address_apt_number = models.CharField(max_length=6, null=True, blank=True)
    address_zip_code = models.IntegerField()
    
    # party Affiliation and Precinct
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.CharField(max_length=2)

    # election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # how many of the past 5 elections the voter participated in
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = '/Users/tsagaandari0604/Desktop/hicheelkk/FALL2024/CS412/django/voter_analytics/newton_voters.csv'
    f = open(filename)
    f.readline() # discard the headers
    
    for line in f:
        fields = line.split(',')

        try: 
            voter = Voter( last_name = fields[1].strip(),
                            first_name = fields[2].strip(),
                            date_of_birth = fields[7].strip(),
                            date_of_registration = fields[8].strip(),
                            
                            address_street_number = fields[3].strip(),
                            address_street_name = fields[4].strip(),
                            address_apt_number = fields[5].strip(),
                            address_zip_code = fields[6].strip(),
                            
                            party_affiliation = fields[9].strip(),
                            precinct_number = fields[10].strip(),
                            
                            v20state = fields[11].strip().upper() == "TRUE",
                            v21town = fields[12].strip().upper() == "TRUE",
                            v21primary = fields[13].strip().upper() == "TRUE",
                            v22general = fields[14].strip().upper() == "TRUE",
                            v23town = fields[15].strip().upper() == "TRUE",
                            
                            voter_score = fields[16].strip(),
                        )
            voter.save() # commit to database
            print(f"Created voter: {voter}")

        except:
            print(f"Skipped: {fields}")
    
    print(f"Done, Created {len(Voter.objects.all())} Voters.")

