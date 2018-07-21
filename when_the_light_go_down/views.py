from django.shortcuts import render, HttpResponse, redirect, reverse

from when_the_light_go_down.models import Hash, Fiche
from when_the_light_go_down.forms import FicheForm


def fiche_hash(request):
    hash_digit = request.GET.get('hash')
    edit = request.GET.get('edit')
    hash_object = Hash.objects.get(hash=hash_digit)
    fiche = hash_object.fiche
    hash_object.delete()
    request.session['fiche'] = fiche.id
    request.session['edit'] = edit

    return redirect(reverse('fiche_render'))


def fiche_render(request):
    fiche_id = request.session['fiche']
    edit = request.session['edit']
    fiche = Fiche.objects.get(id=fiche_id)
    if bool(edit == 'True'):
        data = {
            'user': fiche.user,
            'nom_perso': fiche.nom_perso,
            'prenom_perso': fiche.prenom_perso,
            'description_perso': fiche.description_perso,
            'photo': fiche.photo,
            'connaissance': fiche.connaissance
        }
        form = FicheForm(data)
        return render(request, 'when_the_light_go_down/fiche_edit.html', locals())
    else:
        return render(request, 'when_the_light_go_down/fiche_render.html', locals())
