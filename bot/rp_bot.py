# -*- coding: utf-8  -*-

# A lire si vous faîtes une mise à jour et si vous avez ajouté ou modifié les commandes du bot :
# 1) Copiez vos commandes (pas les commandes par défaut) que vous avez créer dans votre ancienne
#    version dans la nouvelle version.
# 2) Si vous avez modifié une commande de NextBot par défaut, supprimez la commande de la nouvelle
#    version puis copiez le code de la commande de l'ancienne version dans la nouvelle version.

import asyncio
import discord
import os
import requests
import random
import sys

import django
from django.core.files import File

sys.path[:0] = ['../']
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rp.settings')
django.setup()

from when_the_light_go_down.models import Fiche, Hash, Bourse, Echange

# Mettez dans cette variable le token du bot
token = "NDY0OTA0MjQ5NTg4MDU2MDg0.DiFv7A.W205oT9inFjc1kH2iMeu-V-E4Ig"
# Mettez dans cette variable les utilisateurs pouvant utiliser les commandes restreintes
trust = ["Shobu13#3927", "Utilisateur 2"]
trust_roles = ["464859622180782080"]
ranks = False

client = discord.Client()
ver = "1.3.0"
lang = "fr"

site_host = 'gestion-rp.ezo2.eu'


@client.event
@asyncio.coroutine
def on_ready():
    print('LOUND AND CLEAR !')
    print("NextBot " + ver + " " + lang)


@client.event
@asyncio.coroutine
def on_message(message):
    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    user_bot_client = client.user.name
    user_bot = user_bot_client.split("#")[0]
    role_trusted = False
    if type(message.server) is discord.server.Server:
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        for role_name in trust_roles:
            if ":" in role_name and role_name.split(":")[0] == server_msg:
                rank_role = discord.utils.get(message.server.roles,
                                              name=":".join(role_name.split(":")[1:]))
            else:
                rank_role = discord.utils.get(message.server.roles, id=role_name)
            if type(rank_role) is discord.role.Role and rank_role.id in \
                    [r.id for r in message.author.roles]:
                role_trusted = True
        pm = False
    else:
        server_msg = user
        chan_msg = user
        pm = True
    trusted = user in trust or role_trusted
    print(trusted)
    try:
        command = rep2[0].lower()
        params = rep2[1:]
    except IndexError:
        command = ""
        params = ""

    print(str(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep))

    if ranks and not pm:
        open("msgs_user_" + server_msg + ".txt", "a").close()
        msgs = open("msgs_user_" + server_msg + ".txt", "r")
        msgs_r = msgs.read()
        if user not in msgs_r or user != user_bot_client:
            msgs_w = open("msgs_user_" + server_msg + ".txt", "a")
            msgs_w.write(user + ":0\n")
            msgs_w.close()
            msgs.close()
            msgs = open("msgs_user_" + server_msg + ".txt", "r")
            msgs_r = msgs.read()
        msgs_user = msgs_r.split(user + ":")[1]
        msgs.close()
        user_msgs_n = int(msgs_user.split("\n")[0])
        user_msgs_n += 1
        msgs_r = msgs_r.replace(user + ":" + str(user_msgs_n - 1), user + ":" + str(user_msgs_n))
        msgs = open("msgs_user_" + server_msg + ".txt", "w")
        msgs.write(msgs_r)
        msgs.close()

    # Début des commandes
    if command == "!commandtest":  # Copiez ce code pour créer une commande
        yield from client.send_message(message.channel, "Texte à envoyer.")

    if command == "!ban" and trusted and not pm:  # Cette commande n'est pas utilisable en MP
        # La variable params[1] est le premier paramètre entré par l'utilisateur. Si le premier paramètre est une mention
        if "<@" in params[0] and ">" in params[0]:
            # l'ID de l'utilisateur de la mention est récupéré
            id_user = message.server.get_member(params[0].replace("<@", "").replace(">", ""))
        else:  # sinon
            id_user = message.server.get_member_named(
                params[0])  # le pseudo entré en premier paramètre est recherché
        try:
            # bannissement de l'utilisateur avec l'ID de l'utilisateur avec le nombre de messages à
            # effacer
            yield from client.ban(id_user, int(params[1]))
        except IndexError:  # si le 2ème paramètre n'est pas mis (erreur)
            # bannissement de l'utilisateur avec l'ID de l'utilisateur sans le nombre de messages à
            # effacer
            yield from client.ban(id_user, 0)

    if command == "!bing":  # Cette commande sert à rechercher sur Bing
        # "+".join(params[1:]) sert à séparer les paramètres de la commande par des + pour que l'URL
        # de recherche soit accessible, par exemple, en tapant !bing test 2, le bot renverra
        # https://www.bing.com/search?q=test+2
        yield from client.send_message(message.channel, "https://www.bing.com/search?q=" +
                                       "+".join(params[0:]))

    # Cette commande sert à créer un channel sur le serveur, " ".join(params[1:]) est le nom du
    # channel et " ".join() sert à mettre les mots de params[1:] qui est une partie de la liste
    # params qui contient tous les mots du message (à part la commande qui est params[0]).
    if command == "!create_channel" and trusted and not pm:
        yield from client.create_channel(message.server, " ".join(params[0:]))

    # Cette commande sert à créer un channel vocal, voir la commande précédente.
    if command == "!create_channel_voice" and trusted and not pm:
        yield from client.create_channel(message.server, " ".join(params[0:]),
                                         type=discord.ChannelType.voice)

    if command == "!google":  # Voir la commande !bing
        yield from client.send_message(message.channel, "https://www.google.com/#q=" +
                                       "+".join(params[0:]))

    # Cette commande sert à joindre un channel vocal.
    if command == "!join_channel_voice" and trusted:
        yield from client.join_voice_channel(
            discord.utils.get(message.server.channels, name=" ".join(params[0:])))

    if command == "!kick" and trusted and not pm:  # Voir la commande !ban
        if "<@" in params[0] and ">" in params[0]:
            id_user = message.server.get_member(params[0].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[0])
        yield from client.kick(id_user)

    # Cette commande sert à lire de la musique, la premier paramètre est l'id du channel
    # et le second est l'URL de la musique.
    if command == "!music" and trusted:
        # Cette ligne sert à joindre le channel vocal.
        voice_chan = yield from client.join_voice_channel(discord.utils.get(
            message.server.channels, name=" ".join(params[1:len(params) - 1])
        ))
        # Cette ligne sert à obtenir la musique de l'URL.
        music = yield from voice_chan.create_ytdl_player(params[-1])
        music.start()  # Cette ligne sert à diffuser la musique.

    # Ici, on a une commande qui change le nom du bot
    if command == "!nick" and trusted and not pm:
        yield from client.change_nickname(client.user, " ".join(params[0:]))

    # Cette commande sert à purger les membres inactifs.
    if (command == "!prune_members" or command == "!purge_members") and trusted and not pm:
        try:
            yield from client.prune_members(message.server, days=int(params[0]))
        # params[1] est le nombre de jours depuis la dernière connexion des membres, si le paramètre
        # n'est pas mis, le bot purgera les membres qui ne sont pas connectés depuis 30 jours
        except IndexError:
            yield from client.prune_members(message.server, days=30)

    # Cette commande sert à effacer les messages, en tapant !purge 10, le bot supprimera les 10
    # derniers messages.
    if (command == "!purge" or command == "!clear") and trusted and not pm:
        # Cette ligne sert à supprimer les messages avec params[1] qui est le premier paramètre
        # (le nombre de messages), il y a int(params[1]) car le paramètre doit
        # être converti en un nombre.
        yield from client.purge_from(message.channel, limit=int(params[0]))

    # Cette commande sert à fermer le bot
    if (command == "!quit" or command == "!exit") and trusted:
        yield from client.close()

    # Cette commande sert à quitter un channel vocal.
    if command == "!quit_channel_voice" and trusted:
        for voice_chan in client.voice_clients:
            if voice_chan.channel == discord.utils.get(
                    message.server.channels, name=" ".join(params[0:])
            ) and voice_chan.is_connected():
                yield from voice_chan.disconnect()

    # Ici, il y a une commande qui renomme le channel où le message est envoyé
    if (command == "!rename_channel" or command == "!nick_channel") and trusted and not pm:
        yield from client.edit_channel(message.channel, name=" ".join(params[0:]))

    # Cette commande sert à ajouter un rôle à un utilisateur
    if command == "!role_user_add" and trusted and not pm:
        if "<@" in params[0] and ">" in params[0]:
            member = message.server.get_member(params[0].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[0])
        # cette ligne sert à récupérer le rôle de l'utilisateur à ajouter, " ".join(params[2:])
        # est le nom du rôle
        role = discord.utils.get(message.server.roles, name=" ".join(params[1:]))
        # cette ligne sert à appliquer l'ajout du rôle à l'utilisateur et member est l'identifiant
        # de l'utilisateur et role est l'identifiant du rôle
        yield from client.add_roles(member, role)

    # Cette commande sert à retirer un rôle à un utilisateur
    if command == "!role_user_remove" and trusted and not pm:
        if "<@" in params[0] and ">" in params[0]:
            member = message.server.get_member(params[0].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[0])
        role = discord.utils.get(message.server.roles, name=" ".join(params[1:]))
        # cette ligne sert à retirer le rôle d'un utilisateur, son fonctionnement est
        # quasi-identique à part qu'elle fait l'inverse (elle retire le rôle au lieu de l'ajouter)
        yield from client.remove_roles(member, role)

    # Cette commande sert à lister les rôles sur le serveur
    if command == "!roles" and trusted and not pm:
        # cette ligne est une boucle et sert à mettre dans la variable role la liste des rôles
        # du serveur avec message.server.roles
        for role in message.server.roles:
            yield from client.send_message(message.channel, role.id + " : " + role.name)

    if command == "!unban" and trusted and not pm:  # Cette commande sert à débannir un utilisateur
        if "<@" in params[0] and ">" in params[0]:
            id_user = message.server.get_member(params[0].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[0])
        # pour débannir un utilisateur, il faut l'identifiant du serveur avec message.serveur et
        # l'identifiant de l'utilisateur (voir !ban)
        yield from client.unban(message.server, id_user)

    # Cette commande sert à envoyer un message sur un channel du serveur, le paramètre 1 doit être
    # l'identifiant du channel et après, on doit mettre le message
    # (exemple : !say 1234567890 Bonjour !)
    if command == "!say" and trusted:
        yield from client.send_message(client.get_channel(params[0]), " ".join(params[1:]))

    if command == "!say_user" and trusted:
        if params[1].lower() == params[1].upper():
            yield from client.send_message(client.get_server(params[0]).get_member(params[1]),
                                           " ".join(params[2:]))
        else:
            yield from client.send_message(client.get_server(params[0]).get_member_named(params[1]),
                                           " ".join(params[2:]))

    # Cette commande sert à mettre que le client joue à un jeu, " ".join(params[1:])
    # est le nom du jeu.
    if command == "!status_game" and trusted:
        yield from client.change_presence(game=discord.Game(name=" ".join(params[0:])))

    # Ici, on a une commande qui change le sujet du channel où est tapée la commande
    if (command == "!topic" or command == "!topic_channel") and trusted and not pm:
        yield from client.edit_channel(message.channel, topic=" ".join(params[0:]))

    if command == "!ver":  # Cette commande envoit la version du bot.
        yield from client.send_message(message.channel, "NextBot " + ver + " " + lang)

    # Cette commande sert à envoyer un lien vers un article de Vikidia.
    if command == "!viki" or command == "!vikidia":
        yield from client.send_message(message.channel, "https://" + params[0] +
                                       ".vikidia.org/wiki/" + "_".join(params[1:]))

    # Cette commande sert à envoyer un lien vers un article de Wikipédia.
    if command == "!wp" or command == "!wikipedia":
        yield from client.send_message(message.channel, "https://" + params[0] +
                                       ".wikipedia.org/wiki/" + "_".join(params[1:]))

    # Ici, le bot peut répondre a des phrases, par exemple, en disant "Il est cool NextBot",
    # le bot répondra "Merci du compliment, vous aussi vous êtes cool !".
    if "il est cool " + user_bot.lower() in rep.lower():
        yield from client.send_message(message.channel,
                                       "Merci du compliment, vous aussi vous êtes cool ! :)")

    # commandes custom
    if command == "!fiche_get":  # Copiez ce code pour créer une commande
        if params:
            author = params[0]
        else:
            author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            if fiche.validation or (pm and author == fiche.user) or trusted:
                reply = '```' + \
                        'joueur : {}\r'.format(author.split('#')[0]) + \
                        'nom : {}\r'.format(fiche.nom_perso) + \
                        'prenom : {}\r'.format(fiche.prenom_perso) + \
                        'description : {}\r'.format(fiche.description_perso) + \
                        '```'
            else:
                reply = 'fiche non validée'
        except:
            reply = 'fiche non trouvé'

        yield from client.send_message(message.channel, reply)
        os.chdir('..')
        try:
            image_file = open(os.getcwd() + fiche.photo.url, mode='rb')
            yield from client.send_file(message.channel, image_file)
        except:
            pass

    if command == "!fiche_web" and pm:
        if params:
            author = params[0]
            edit = False
        else:
            author = str(message.author)
            edit = True
        try:
            fiche = Fiche.objects.get(user=author)
            if fiche.validation or (pm and author == fiche.user) or trusted:
                hash_digit = random.getrandbits(128)
                hash_object = Hash(hash=hash_digit, fiche=fiche)
                hash_object.save()
                reply = 'http://{}/fiche_hash?hash={}&edit={}'.format(site_host, hash_digit, edit)
            else:
                reply = 'fiche non validée'
        except:
            reply = 'fiche non trouvée'
        yield from client.send_message(message.channel, reply)

    if command == "!fiche_create":
        author = str(message.author)
        created, is_created = Fiche.objects.get_or_create(user=author)
        if is_created:
            reply = 'fiche crée'
            Bourse(perso=created).save()
        else:
            reply = 'fiche déjà existente'
        yield from client.send_message(message.channel, reply)
        yield from client.delete_message(message)

    if command == "!fiche_nom":
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            ancien_nom = fiche.nom_perso
            fiche.nom_perso = " ".join(params)
            fiche.save()
            reply = 'modification effectuée\r' \
                    'ancien : {}\r'.format(ancien_nom) + \
                    'nouveau : {}\r'.format(fiche.nom_perso)
        except:
            reply = 'fiche non trouvée'
        yield from client.send_message(message.channel, reply)

    if command == "!fiche_prenom":
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            ancien_prenom = fiche.prenom_perso
            fiche.prenom_perso = " ".join(params)
            fiche.save()
            reply = 'modification effectuée\r' \
                    'ancien : {}\r'.format(ancien_prenom) + \
                    'nouveau : {}\r'.format(fiche.prenom_perso)
        except:
            reply = 'fiche non trouvée'
        yield from client.send_message(message.channel, reply)

    if command == "!fiche_description":
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            ancienne_description = fiche.description_perso
            fiche.description_perso = " ".join(params)
            fiche.save()
            reply = 'modification effectuée\r' \
                    'ancien : {}\r'.format(ancienne_description) + \
                    'nouveau : {}\r'.format(fiche.description_perso)
        except:
            reply = 'fiche non trouvée'
        yield from client.send_message(message.channel, reply)

    if command == '!fiche_image':
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            if fiche.photo:
                ancienne_photo = fiche.photo.url
            else:
                ancienne_photo = ""
            os.chdir('..')
            image = message.attachments[0]
            down_link = requests.get(image['url'])
            with open(os.getcwd() + '/temp.jpg', "wb") as img_obj:
                img_obj.write(down_link.content)
            file = open('{}'.format('temp.jpg'), 'rb')
            image = File(file)
            fiche.photo = image
            fiche.save()
            reply = 'modification effectuée\r' \
                    'ancien : http://{}{}\r'.format(site_host, ancienne_photo) + \
                    'nouveau : http://{}{}\r'.format(site_host, fiche.photo.url)
        except:
            reply = 'fiche non trouvée'
        yield from client.send_message(message.channel, reply)

    if command == "!bourse_get":  # Copiez ce code pour créer une commande
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            bourse = fiche.bourse_set.all()[0]
            reply = '```' + \
                    'joueur : {}\r'.format(author.split('#')[0]) + \
                    'orions : {}\r'.format(bourse.orions) + \
                    'argentions : {}\r'.format(bourse.argentions) + \
                    'cuivrons : {}\r'.format(bourse.cuivrons) + \
                    '```'
        except BaseException as e:
            print(e)
            reply = 'bourse non trouvé'

        yield from client.send_message(message.channel, reply)

    if command == "!bourse_set":  # Copiez ce code pour créer une commande
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            bourse = fiche.bourse_set.all()[0]
            reply = '```' + \
                    'avant : \r' + \
                    'joueur : {}\r'.format(author.split('#')[0]) + \
                    'orions : {}\r'.format(bourse.orions) + \
                    'argentions : {}\r'.format(bourse.argentions) + \
                    'cuivrons : {}\r'.format(bourse.cuivrons) + \
                    '```'
            bourse.orions = params[0]
            bourse.argentions = params[1]
            bourse.cuivrons = params[2]
            bourse.save()
            Echange(
                receveur=fiche,
                donneur=fiche,
                type='set',
                orions=params[0],
                argentions=params[1],
                cuivrons=params[2],
            ).save()
            reply += \
                '```' + \
                'après : \r' + \
                'joueur : {}\r'.format(author.split('#')[0]) + \
                'orions : {}\r'.format(bourse.orions) + \
                'argentions : {}\r'.format(bourse.argentions) + \
                'cuivrons : {}\r'.format(bourse.cuivrons) + \
                '```'
        except BaseException as e:
            print(e)
            reply = 'bourse non trouvé'

        yield from client.send_message(message.channel, reply)

    if command == "!bourse_operation":  # Copiez ce code pour créer une commande
        author = str(message.author)
        try:
            fiche = Fiche.objects.get(user=author)
            bourse = fiche.bourse_set.all()[0]
            reply = '```' + \
                    'avant : \r' + \
                    'joueur : {}\r'.format(author.split('#')[0]) + \
                    'orions : {}\r'.format(bourse.orions) + \
                    'argentions : {}\r'.format(bourse.argentions) + \
                    'cuivrons : {}\r'.format(bourse.cuivrons) + \
                    '```'
            bourse.orions += int(params[0])
            bourse.argentions += int(params[1])
            bourse.cuivrons += int(params[2])
            bourse.save()
            Echange(
                receveur=fiche,
                donneur=fiche,
                type='operation',
                orions=params[0],
                argentions=params[1],
                cuivrons=params[2],
            ).save()
            reply += \
                '```' + \
                'après : \r' + \
                'joueur : {}\r'.format(author.split('#')[0]) + \
                'orions : {}\r'.format(bourse.orions) + \
                'argentions : {}\r'.format(bourse.argentions) + \
                'cuivrons : {}\r'.format(bourse.cuivrons) + \
                '```'
        except BaseException as e:
            print(e)
            reply = 'bourse non trouvé'

        yield from client.send_message(message.channel, reply)

    if command == "!bourse_exchange":  # Copiez ce code pour créer une commande
        receveur = str(message.mentions[0])
        author = str(message.author)
        try:
            fiche_receveur = Fiche.objects.get(user=receveur)
            fiche_donneur = Fiche.objects.get(user=author)
            bourse_donneur = fiche_donneur.bourse_set.all()[0]
            bourse_receveur = fiche_receveur.bourse_set.all()[0]
            reply = '```' + \
                    'avant : \r' + \
                    'donneur : {}\r'.format(author.split('#')[0]) + \
                    'orions : {}\r'.format(bourse_donneur.orions) + \
                    'argentions : {}\r'.format(bourse_donneur.argentions) + \
                    'cuivrons : {}\r'.format(bourse_donneur.cuivrons) + \
                    '\r' + \
                    'receveur : {}\r'.format(author.split('#')[0]) + \
                    'orions : {}\r'.format(bourse_receveur.orions) + \
                    'argentions : {}\r'.format(bourse_receveur.argentions) + \
                    'cuivrons : {}\r'.format(bourse_receveur.cuivrons) + \
                    '```'
            bourse_donneur.orions -= int(params[1])
            bourse_donneur.argentions -= int(params[2])
            bourse_donneur.cuivrons -= int(params[3])

            bourse_receveur.orions += int(params[1])
            bourse_receveur.argentions += int(params[2])
            bourse_receveur.cuivrons += int(params[3])

            bourse_donneur.save()
            bourse_receveur.save()
            Echange(
                receveur=fiche_receveur,
                donneur=fiche_donneur,
                type='échange',
                orions=params[1],
                argentions=params[2],
                cuivrons=params[3],
            ).save()
            reply += \
                '```' + \
                'après : \r' + \
                'donneur : {}\r'.format(author.split('#')[0]) + \
                'orions : {}\r'.format(bourse_donneur.orions) + \
                'argentions : {}\r'.format(bourse_donneur.argentions) + \
                'cuivrons : {}\r'.format(bourse_donneur.cuivrons) + \
                '\r' + \
                'receveur : {}\r'.format(author.split('#')[0]) + \
                'orions : {}\r'.format(bourse_receveur.orions) + \
                'argentions : {}\r'.format(bourse_receveur.argentions) + \
                'cuivrons : {}\r'.format(bourse_receveur.cuivrons) + \
                '```'
        except BaseException as e:
            print(e)
            reply = 'bourse non trouvé'

        yield from client.send_message(message.channel, reply)


# Fin des commandes

client.run(token)
