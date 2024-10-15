from django.db import models

pilihan_waktu_kedatangan = [
    ('08:00', '08:00 AM'),
    ('09:00', '09:00 AM'),
    ('10:00', '10:00 AM'),
    ('11:00', '11:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '01:00 PM'),
    ('14:00', '02:00 PM'),
    ('15:00', '03:00 PM'),
    ('16:00', '04:00 PM'),
]

class ReserveEntry(models.Model):
    name = models.CharField(max_length=255)
    tanggal_kedatangan = models.DateField()
    waktu_kedatangan = models.CharField(max_length=5, choices=pilihan_waktu_kedatangan)
    jumlah_tamu = models.IntegerField(default=0)
    email = models.EmailField()
    no_telp = models.IntegerField()
    notes = models.CharField(max_length=255)


    
