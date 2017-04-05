import json
import string
import sys
from collections import OrderedDict


#Card and card database classes to save some time
class Card(object):
    def __init__(self, d):
        for a, b in d.items():
            setattr(self, a, b)
            #if isinstance(b, (list, tuple)):
            #   setattr(self, a, [Card(x) if isinstance(x, dict) else x for x in b])
            #else:
            #   setattr(self, a, Card(b) if isinstance(b, dict) else b)

class CardDatabase(object):
    def __init__(self, d):
        self.cards = {}
        for a, b in d.items():
            self.cards.update({a: Card(b)})

#The basic template for all cards
card_template = string.Template(u'''
        <card>
            <name>$name</name>
            <set picURL="$picture">$set</set>
            <related>$evoname</related>
            <color>$faction</color>
            <manacost>$manacost</manacost>
            <cmc>$manacost</cmc>
            <type>$type $trait</type>
            <pt>$attack/$defense</pt>
            <tablerow>0</tablerow>
            <text>$description</text>
        </card>
''')

file_start = u'''<?xml version="1.0" encoding="UTF-8"?>
<cockatrice_carddatabase version="3">
    <sets>
        <set>
            <name>S</name>
            <longname>Standard Card Pack</longname>
            <settype>Base</settype>
            <releasedate></releasedate>
        </set>
        <set>
            <name>DE</name>
            <longname>Darkness Evolved</longname>
            <settype>Expansion</settype>
            <releasedate></releasedate>
        </set>
        <set>
            <name>RoB</name>
            <longname>Rise of Bahamut</longname>
            <settype>Expansion</settype>
            <releasedate></releasedate>
        </set>
        <set>
            <name>TotG</name>
            <longname>Tempest of the Gods</longname>
            <settype>Expansion</settype>
            <releasedate></releasedate>
        </set>
        <set>
            <name>B</name>
            <longname>Basic</longname>
            <settype>Base</settype>
            <releasedate></releasedate>
        </set>
        <set>
            <name>TK</name>
            <longname>Token</longname>
            <settype>Token</settype>
            <releasedate></releasedate>
        </set>
    </sets>
    <cards>
'''

file_end = u'''
    </cards>
</cockatrice_carddatabase>
'''

#A dictionary with all the expansions thus far
expansion_map = { "Basic": "B",
                  "Darkness Evolved": "DE",
                  "Rise of Bahamut": "RoB",
                  "Standard Card Pack": "S",
                  "Tempest of the Gods": "TotG",
                  "Token": "TK"}

#The parsing function
def parse_db(db):
    output = ""
    for key, value in db.cards.items():
        arguments = {'name': value.name, 'faction': value.faction, 'picture': value.baseData['img'], 'type': value.type,
                     'manacost': value.manaCost, 'attack': value.baseData['attack'],
                     'defense': value.baseData['defense'], 'description': value.baseData['description']}
        if value.race != "":
            arguments['trait'] = "- " + value.race
        else:
            arguments['trait'] = ""
        if value.expansion in expansion_map:
            arguments['set'] = expansion_map[value.expansion]
        else:
            arguments['set'] = value.expansion

        #Followers that evolve:
        if value.hasEvo:
            arguments['evoname'] = value.name + " Evolved"
            output = output + card_template.substitute(arguments)

            arguments_evo = {'name': value.name + " Evolved", 'faction': value.faction,
                             'picture': value.evoData['img'], 'type': value.type, 'manacost': value.manaCost,
                             'attack': value.evoData['attack'], 'defense': value.evoData['defense'],
                             'description': value.evoData['description'], 'evoname': value.name}
            if value.race != "":
                arguments_evo['trait'] = "- " + value.race
            else:
                arguments_evo['trait'] = ""
            if value.expansion in expansion_map:
                arguments_evo['set'] = expansion_map[value.expansion]
            else:
                arguments_evo['set'] = value.expansion

            output = output + card_template.substitute(arguments_evo)
        else:
            arguments['evoname'] = ""
            output = output + card_template.substitute(arguments)

    return output

#Beginning of the script itself
if len(sys.argv) > 2:
    file_input = sys.argv[1]
    file_output = sys.argv[2]
else:
    print("Input or output file missing!")
    exit(1)

x = ""

try:
    with open(file_input, 'r') as data:
        x = json.load(data, object_pairs_hook=OrderedDict)
        x = OrderedDict(sorted(x.items(), key=lambda t: t[1]['expansion'])) #Sort by set, as such order matters in the Cockatrice DB
        print('Loaded ' + len(x).__str__() + ' cards.')
except Exception, Argument:
    print "An error occurred when loading the JSON file: ", Argument

try:
    x_obj = CardDatabase(x)

    xml_output = file_start + parse_db(x_obj) + file_end
    with open(file_output, 'w') as data:
        data.write(xml_output.replace('<br>', '\n').encode("utf8"))

    print "Saved database file to: " + file_output

except Exception, Argument:
    print "An error occurred when saving: ", Argument

