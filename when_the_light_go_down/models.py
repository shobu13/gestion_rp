from django.db import models


class Fiche(models.Model):
    user = models.CharField(max_length=150)
    nom_perso = models.CharField(max_length=100, blank=True)
    prenom_perso = models.CharField(max_length=100, blank=True)
    description_perso = models.TextField(default="", blank=True)
    photo = models.ImageField(upload_to='wtlgd/perso', blank=True, null=True)
    connaissance = models.IntegerField(default=10)

    validation = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} de {}'.format(self.nom_perso, self.prenom_perso, self.user)


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()


class Inventaire(models.Model):
    perso = models.ForeignKey(Fiche, on_delete=models.CASCADE)
    objet = models.ForeignKey(Objet, on_delete=models.CASCADE)
    quantite = models.IntegerField()


class Bourse(models.Model):
    perso = models.ForeignKey(Fiche, on_delete=models.CASCADE)
    cuivrons = models.IntegerField(default=0, blank=True)
    argentions = models.IntegerField(default=0, blank=True)
    orions = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return 'bourse de {} {}'.format(self.perso.nom_perso, self.perso.prenom_perso)


class Echange(models.Model):
    receveur = models.ForeignKey(Fiche, on_delete=models.SET_NULL, null=True)
    donneur = models.ForeignKey(Fiche, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='donneur')
    type = models.CharField(max_length=100)
    orions = models.IntegerField()
    argentions = models.IntegerField()
    cuivrons = models.IntegerField()

    def __str__(self):
        if self.receveur and self.donneur:
            return '{} entre {} et {}'.format(self.type, self.receveur.prenom_perso,
                                          self.donneur.prenom_perso)
        elif self.donneur:
            return '{} entre {} et {}'.format(self.type, 'None',
                                              self.donneur.prenom_perso)
        elif self.receveur:
            return '{} entre {} et {}'.format(self.type, self.receveur.prenom_perso,
                                              'None')
        else:
            return '{} entre {} et {}'.format(self.type, 'None',
                                              'None')


class Hash(models.Model):
    hash = models.CharField(max_length=128)
    fiche = models.ForeignKey('Fiche', on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.hash[0:50], self.fiche.user)
