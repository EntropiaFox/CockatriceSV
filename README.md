## CockatriceSV

A script to generate a valid [Cockatrice](https://cockatrice.github.io/) database out of a JSON file containing Shadowverse card data.

### Requirements

* Python 2.7+
* A JSON file specifying all the relevant card data. See the included file for the required format.

### Usage

`python json2cockatrice_db.py inputfile.json outputfile.xml`

### Credits

* [ElDynamite](http://sv.bagoum.com/) for providing the original JSON file and saving me a crapload of time.

### Roadmap

* Add not just the evolved version of a card, but also any associated tokens/cards brought into play by a given card so they're easily accessed from within Cockatrice.

### License

The code itself is under the GNU General Public License v3 whereas the card data belongs to Cygames.