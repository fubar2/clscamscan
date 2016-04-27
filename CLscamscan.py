# code to grab new cl urls
# and stow them so no need to hit CL
# parse out wickr ids if possible
# rml me fecit march 2016
# maybe wickr is a better search term than 420
# far fewer hits - need a combo

from feedparser import parse
from bs4 import BeautifulSoup
from bs4 import element
import urllib2
import string
import re
import html2text
import logging
import logging.handlers
import datetime
import time
import sqlite3 as lite
import sys
import os
import urllib2
import copy

TIMEOUT=30
VERBOSE = False
DROP = True
allurl = "https://www.craigslist.org/about/sites"
# BASE_URL = "%ssearch/sss?format=rss&query=%s"
BASE_URL = "%ssearch/sss?query=%s"
SEARCH_TERMS = ['420','kush'] # better than kush...
tod = datetime.datetime.today()
PAGE_STORE = '/data/CL'
US_URLS=[ 'http://auburn.craigslist.org/', 'http://bham.craigslist.org/', 'http://dothan.craigslist.org/', 'http://shoals.craigslist.org/', 'http://gadsden.craigslist.org/',
'http://huntsville.craigslist.org/', 'http://mobile.craigslist.org/', 'http://montgomery.craigslist.org/', 'http://tuscaloosa.craigslist.org/', 'http://anchorage.craigslist.org/',
'http://fairbanks.craigslist.org/', 'http://kenai.craigslist.org/', 'http://juneau.craigslist.org/', 'http://flagstaff.craigslist.org/', 'http://mohave.craigslist.org/',
'http://phoenix.craigslist.org/', 'http://prescott.craigslist.org/', 'http://showlow.craigslist.org/', 'http://sierravista.craigslist.org/', 'http://tucson.craigslist.org/',
'http://yuma.craigslist.org/', 'http://fayar.craigslist.org/', 'http://fortsmith.craigslist.org/', 'http://jonesboro.craigslist.org/', 'http://littlerock.craigslist.org/',
'http://texarkana.craigslist.org/', 'http://bakersfield.craigslist.org/', 'http://chico.craigslist.org/', 'http://fresno.craigslist.org/', 'http://goldcountry.craigslist.org/',
'http://hanford.craigslist.org/', 'http://humboldt.craigslist.org/', 'http://imperial.craigslist.org/', 'http://inlandempire.craigslist.org/', 'http://losangeles.craigslist.org/',
'http://mendocino.craigslist.org/', 'http://merced.craigslist.org/', 'http://modesto.craigslist.org/', 'http://monterey.craigslist.org/', 'http://orangecounty.craigslist.org/',
'http://palmsprings.craigslist.org/', 'http://redding.craigslist.org/', 'http://sacramento.craigslist.org/', 'http://sandiego.craigslist.org/', 'http://sfbay.craigslist.org/',
'http://slo.craigslist.org/', 'http://santabarbara.craigslist.org/', 'http://santamaria.craigslist.org/', 'http://siskiyou.craigslist.org/', 'http://stockton.craigslist.org/',
'http://susanville.craigslist.org/', 'http://ventura.craigslist.org/', 'http://visalia.craigslist.org/', 'http://yubasutter.craigslist.org/', 'http://boulder.craigslist.org/',
'http://cosprings.craigslist.org/', 'http://denver.craigslist.org/', 'http://eastco.craigslist.org/', 'http://fortcollins.craigslist.org/', 'http://rockies.craigslist.org/',
'http://pueblo.craigslist.org/', 'http://westslope.craigslist.org/', 'http://newlondon.craigslist.org/', 'http://hartford.craigslist.org/', 'http://newhaven.craigslist.org/',
'http://nwct.craigslist.org/', 'http://delaware.craigslist.org/', 'http://washingtondc.craigslist.org/', 'http://miami.craigslist.org/brw', 'http://daytona.craigslist.org/',
'http://keys.craigslist.org/', 'http://fortlauderdale.craigslist.org/', 'http://fortmyers.craigslist.org/', 'http://gainesville.craigslist.org/', 'http://cfl.craigslist.org/',
'http://jacksonville.craigslist.org/', 'http://lakeland.craigslist.org/', 'http://miami.craigslist.org/mdc', 'http://lakecity.craigslist.org/', 'http://ocala.craigslist.org/',
'http://okaloosa.craigslist.org/', 'http://orlando.craigslist.org/', 'http://panamacity.craigslist.org/', 'http://pensacola.craigslist.org/', 'http://sarasota.craigslist.org/',
'http://miami.craigslist.org/', 'http://spacecoast.craigslist.org/', 'http://staugustine.craigslist.org/', 'http://tallahassee.craigslist.org/', 'http://tampa.craigslist.org/',
'http://treasure.craigslist.org/', 'http://miami.craigslist.org/pbc', 'http://albanyga.craigslist.org/', 'http://athensga.craigslist.org/', 'http://atlanta.craigslist.org/',
'http://augusta.craigslist.org/', 'http://brunswick.craigslist.org/', 'http://columbusga.craigslist.org/', 'http://macon.craigslist.org/', 'http://nwga.craigslist.org/',
'http://savannah.craigslist.org/', 'http://statesboro.craigslist.org/', 'http://valdosta.craigslist.org/', 'http://honolulu.craigslist.org/', 'http://boise.craigslist.org/',
'http://eastidaho.craigslist.org/', 'http://lewiston.craigslist.org/', 'http://twinfalls.craigslist.org/', 'http://bn.craigslist.org/', 'http://chambana.craigslist.org/',
'http://chicago.craigslist.org/', 'http://decatur.craigslist.org/', 'http://lasalle.craigslist.org/', 'http://mattoon.craigslist.org/', 'http://peoria.craigslist.org/',
'http://rockford.craigslist.org/', 'http://carbondale.craigslist.org/', 'http://springfieldil.craigslist.org/', 'http://quincy.craigslist.org/', 'http://bloomington.craigslist.org/',
'http://evansville.craigslist.org/', 'http://fortwayne.craigslist.org/', 'http://indianapolis.craigslist.org/', 'http://kokomo.craigslist.org/', 'http://tippecanoe.craigslist.org/',
'http://muncie.craigslist.org/', 'http://richmondin.craigslist.org/', 'http://southbend.craigslist.org/', 'http://terrehaute.craigslist.org/', 'http://ames.craigslist.org/',
'http://cedarrapids.craigslist.org/', 'http://desmoines.craigslist.org/', 'http://dubuque.craigslist.org/', 'http://fortdodge.craigslist.org/', 'http://iowacity.craigslist.org/',
'http://masoncity.craigslist.org/', 'http://quadcities.craigslist.org/', 'http://siouxcity.craigslist.org/', 'http://ottumwa.craigslist.org/', 'http://waterloo.craigslist.org/',
'http://lawrence.craigslist.org/', 'http://ksu.craigslist.org/', 'http://nwks.craigslist.org/', 'http://salina.craigslist.org/', 'http://seks.craigslist.org/', 'http://swks.craigslist.org/',
'http://topeka.craigslist.org/', 'http://wichita.craigslist.org/', 'http://bgky.craigslist.org/', 'http://eastky.craigslist.org/', 'http://lexington.craigslist.org/',
'http://louisville.craigslist.org/', 'http://owensboro.craigslist.org/', 'http://westky.craigslist.org/', 'http://batonrouge.craigslist.org/', 'http://cenla.craigslist.org/',
'http://houma.craigslist.org/', 'http://lafayette.craigslist.org/', 'http://lakecharles.craigslist.org/', 'http://monroe.craigslist.org/', 'http://neworleans.craigslist.org/',
'http://shreveport.craigslist.org/', 'http://maine.craigslist.org/', 'http://annapolis.craigslist.org/', 'http://baltimore.craigslist.org/', 'http://easternshore.craigslist.org/',
'http://frederick.craigslist.org/', 'http://smd.craigslist.org/', 'http://westmd.craigslist.org/', 'http://boston.craigslist.org/', 'http://capecod.craigslist.org/',
'http://southcoast.craigslist.org/', 'http://westernmass.craigslist.org/', 'http://worcester.craigslist.org/', 'http://annarbor.craigslist.org/', 'http://battlecreek.craigslist.org/',
'http://centralmich.craigslist.org/', 'http://detroit.craigslist.org/', 'http://flint.craigslist.org/', 'http://grandrapids.craigslist.org/', 'http://holland.craigslist.org/',
'http://jxn.craigslist.org/', 'http://kalamazoo.craigslist.org/', 'http://lansing.craigslist.org/', 'http://monroemi.craigslist.org/', 'http://muskegon.craigslist.org/',
'http://nmi.craigslist.org/', 'http://porthuron.craigslist.org/', 'http://saginaw.craigslist.org/', 'http://swmi.craigslist.org/', 'http://thumb.craigslist.org/', 'http://up.craigslist.org/',
'http://bemidji.craigslist.org/', 'http://brainerd.craigslist.org/', 'http://duluth.craigslist.org/', 'http://mankato.craigslist.org/', 'http://minneapolis.craigslist.org/',
'http://rmn.craigslist.org/', 'http://marshall.craigslist.org/', 'http://stcloud.craigslist.org/', 'http://gulfport.craigslist.org/', 'http://hattiesburg.craigslist.org/',
'http://jackson.craigslist.org/', 'http://meridian.craigslist.org/', 'http://northmiss.craigslist.org/', 'http://natchez.craigslist.org/', 'http://columbiamo.craigslist.org/',
'http://joplin.craigslist.org/', 'http://kansascity.craigslist.org/', 'http://kirksville.craigslist.org/', 'http://loz.craigslist.org/', 'http://semo.craigslist.org/',
'http://springfield.craigslist.org/', 'http://stjoseph.craigslist.org/', 'http://stlouis.craigslist.org/', 'http://billings.craigslist.org/', 'http://bozeman.craigslist.org/',
'http://butte.craigslist.org/', 'http://greatfalls.craigslist.org/', 'http://helena.craigslist.org/', 'http://kalispell.craigslist.org/', 'http://missoula.craigslist.org/',
'http://montana.craigslist.org/', 'http://grandisland.craigslist.org/', 'http://lincoln.craigslist.org/', 'http://northplatte.craigslist.org/', 'http://omaha.craigslist.org/',
'http://scottsbluff.craigslist.org/', 'http://elko.craigslist.org/', 'http://lasvegas.craigslist.org/', 'http://reno.craigslist.org/', 'http://nh.craigslist.org/', 'http://cnj.craigslist.org/',
'http://jerseyshore.craigslist.org/', 'http://newjersey.craigslist.org/', 'http://southjersey.craigslist.org/', 'http://albuquerque.craigslist.org/', 'http://clovis.craigslist.org/',
'http://farmington.craigslist.org/', 'http://lascruces.craigslist.org/', 'http://roswell.craigslist.org/', 'http://santafe.craigslist.org/', 'http://albany.craigslist.org/',
'http://binghamton.craigslist.org/', 'http://buffalo.craigslist.org/', 'http://catskills.craigslist.org/', 'http://chautauqua.craigslist.org/', 'http://elmira.craigslist.org/',
'http://fingerlakes.craigslist.org/', 'http://glensfalls.craigslist.org/', 'http://hudsonvalley.craigslist.org/', 'http://ithaca.craigslist.org/', 'http://longisland.craigslist.org/',
'http://newyork.craigslist.org/', 'http://oneonta.craigslist.org/', 'http://plattsburgh.craigslist.org/', 'http://potsdam.craigslist.org/', 'http://rochester.craigslist.org/',
'http://syracuse.craigslist.org/', 'http://twintiers.craigslist.org/', 'http://utica.craigslist.org/', 'http://watertown.craigslist.org/', 'http://asheville.craigslist.org/',
'http://boone.craigslist.org/', 'http://charlotte.craigslist.org/', 'http://eastnc.craigslist.org/', 'http://fayetteville.craigslist.org/', 'http://greensboro.craigslist.org/',
'http://hickory.craigslist.org/', 'http://onslow.craigslist.org/', 'http://outerbanks.craigslist.org/', 'http://raleigh.craigslist.org/', 'http://wilmington.craigslist.org/',
'http://winstonsalem.craigslist.org/', 'http://bismarck.craigslist.org/', 'http://fargo.craigslist.org/', 'http://grandforks.craigslist.org/', 'http://nd.craigslist.org/',
'http://akroncanton.craigslist.org/', 'http://ashtabula.craigslist.org/', 'http://athensohio.craigslist.org/', 'http://chillicothe.craigslist.org/', 'http://cincinnati.craigslist.org/',
'http://cleveland.craigslist.org/', 'http://columbus.craigslist.org/', 'http://dayton.craigslist.org/', 'http://limaohio.craigslist.org/', 'http://mansfield.craigslist.org/',
'http://sandusky.craigslist.org/', 'http://toledo.craigslist.org/', 'http://tuscarawas.craigslist.org/', 'http://youngstown.craigslist.org/', 'http://zanesville.craigslist.org/',
'http://lawton.craigslist.org/', 'http://enid.craigslist.org/', 'http://oklahomacity.craigslist.org/', 'http://stillwater.craigslist.org/', 'http://tulsa.craigslist.org/',
'http://bend.craigslist.org/', 'http://corvallis.craigslist.org/', 'http://eastoregon.craigslist.org/', 'http://eugene.craigslist.org/', 'http://klamath.craigslist.org/',
'http://medford.craigslist.org/', 'http://oregoncoast.craigslist.org/', 'http://portland.craigslist.org/', 'http://roseburg.craigslist.org/', 'http://salem.craigslist.org/',
'http://altoona.craigslist.org/', 'http://chambersburg.craigslist.org/', 'http://erie.craigslist.org/', 'http://harrisburg.craigslist.org/', 'http://lancaster.craigslist.org/',
'http://allentown.craigslist.org/', 'http://meadville.craigslist.org/', 'http://philadelphia.craigslist.org/', 'http://pittsburgh.craigslist.org/', 'http://poconos.craigslist.org/',
'http://reading.craigslist.org/', 'http://scranton.craigslist.org/', 'http://pennstate.craigslist.org/', 'http://williamsport.craigslist.org/', 'http://york.craigslist.org/',
'http://providence.craigslist.org/', 'http://charleston.craigslist.org/', 'http://columbia.craigslist.org/', 'http://florencesc.craigslist.org/', 'http://greenville.craigslist.org/',
'http://hiltonhead.craigslist.org/', 'http://myrtlebeach.craigslist.org/', 'http://nesd.craigslist.org/', 'http://csd.craigslist.org/', 'http://rapidcity.craigslist.org/',
'http://siouxfalls.craigslist.org/', 'http://sd.craigslist.org/', 'http://chattanooga.craigslist.org/', 'http://clarksville.craigslist.org/', 'http://cookeville.craigslist.org/',
'http://jacksontn.craigslist.org/', 'http://knoxville.craigslist.org/', 'http://memphis.craigslist.org/', 'http://nashville.craigslist.org/', 'http://tricities.craigslist.org/',
'http://abilene.craigslist.org/', 'http://amarillo.craigslist.org/', 'http://austin.craigslist.org/', 'http://beaumont.craigslist.org/', 'http://brownsville.craigslist.org/',
'http://collegestation.craigslist.org/', 'http://corpuschristi.craigslist.org/', 'http://dallas.craigslist.org/', 'http://nacogdoches.craigslist.org/', 'http://delrio.craigslist.org/',
'http://elpaso.craigslist.org/', 'http://galveston.craigslist.org/', 'http://houston.craigslist.org/', 'http://killeen.craigslist.org/', 'http://laredo.craigslist.org/',
'http://lubbock.craigslist.org/', 'http://mcallen.craigslist.org/', 'http://odessa.craigslist.org/', 'http://sanangelo.craigslist.org/', 'http://sanantonio.craigslist.org/',
'http://sanmarcos.craigslist.org/', 'http://bigbend.craigslist.org/', 'http://texoma.craigslist.org/', 'http://easttexas.craigslist.org/', 'http://victoriatx.craigslist.org/',
'http://waco.craigslist.org/', 'http://wichitafalls.craigslist.org/', 'http://logan.craigslist.org/', 'http://ogden.craigslist.org/', 'http://provo.craigslist.org/',
'http://saltlakecity.craigslist.org/', 'http://stgeorge.craigslist.org/', 'http://burlington.craigslist.org/', 'http://charlottesville.craigslist.org/', 'http://danville.craigslist.org/',
'http://fredericksburg.craigslist.org/', 'http://norfolk.craigslist.org/', 'http://harrisonburg.craigslist.org/', 'http://lynchburg.craigslist.org/', 'http://blacksburg.craigslist.org/',
'http://richmond.craigslist.org/', 'http://roanoke.craigslist.org/', 'http://swva.craigslist.org/', 'http://winchester.craigslist.org/', 'http://bellingham.craigslist.org/',
'http://kpr.craigslist.org/', 'http://moseslake.craigslist.org/', 'http://olympic.craigslist.org/', 'http://pullman.craigslist.org/', 'http://seattle.craigslist.org/',
'http://skagit.craigslist.org/', 'http://spokane.craigslist.org/', 'http://wenatchee.craigslist.org/', 'http://yakima.craigslist.org/', 'http://charlestonwv.craigslist.org/',
'http://martinsburg.craigslist.org/', 'http://huntington.craigslist.org/', 'http://morgantown.craigslist.org/', 'http://wheeling.craigslist.org/', 'http://parkersburg.craigslist.org/',
'http://swv.craigslist.org/', 'http://wv.craigslist.org/', 'http://appleton.craigslist.org/', 'http://eauclaire.craigslist.org/', 'http://greenbay.craigslist.org/',
'http://janesville.craigslist.org/', 'http://racine.craigslist.org/', 'http://lacrosse.craigslist.org/', 'http://madison.craigslist.org/', 'http://milwaukee.craigslist.org/',
'http://northernwi.craigslist.org/', 'http://sheboygan.craigslist.org/', 'http://wausau.craigslist.org/', 'http://wyoming.craigslist.org/', 'http://micronesia.craigslist.org/',
'http://puertorico.craigslist.org/', 'http://virgin.craigslist.org/']
CA_URLS=['http://calgary.craigslist.ca/', 'http://edmonton.craigslist.ca/', 'http://ftmcmurray.craigslist.ca/', 'http://lethbridge.craigslist.ca/', 'http://hat.craigslist.ca/',
'http://peace.craigslist.ca/', 'http://reddeer.craigslist.ca/', 'http://cariboo.craigslist.ca/', 'http://comoxvalley.craigslist.ca/', 'http://abbotsford.craigslist.ca/',
'http://kamloops.craigslist.ca/', 'http://kelowna.craigslist.ca/', 'http://cranbrook.craigslist.ca/', 'http://nanaimo.craigslist.ca/', 'http://princegeorge.craigslist.ca/',
'http://skeena.craigslist.ca/', 'http://sunshine.craigslist.ca/', 'http://vancouver.craigslist.ca/', 'http://victoria.craigslist.ca/', 'http://whistler.craigslist.ca/',
'http://winnipeg.craigslist.ca/', 'http://newbrunswick.craigslist.ca/', 'http://newfoundland.craigslist.ca/', 'http://territories.craigslist.ca/', 'http://yellowknife.craigslist.ca/',
'http://halifax.craigslist.ca/', 'http://barrie.craigslist.ca/', 'http://belleville.craigslist.ca/', 'http://brantford.craigslist.ca/', 'http://chatham.craigslist.ca/',
'http://cornwall.craigslist.ca/', 'http://guelph.craigslist.ca/', 'http://hamilton.craigslist.ca/', 'http://kingston.craigslist.ca/', 'http://kitchener.craigslist.ca/',
'http://londonon.craigslist.ca/', 'http://niagara.craigslist.ca/', 'http://ottawa.craigslist.ca/', 'http://owensound.craigslist.ca/', 'http://peterborough.craigslist.ca/',
'http://sarnia.craigslist.ca/', 'http://soo.craigslist.ca/', 'http://sudbury.craigslist.ca/', 'http://thunderbay.craigslist.ca/', 'http://toronto.craigslist.ca/', 'http://windsor.craigslist.ca/',
'http://pei.craigslist.ca/', 'http://montreal.craigslist.ca/', 'http://quebec.craigslist.ca/', 'http://saguenay.craigslist.ca/', 'http://sherbrooke.craigslist.ca/',
'http://troisrivieres.craigslist.ca/', 'http://regina.craigslist.ca/', 'http://saskatoon.craigslist.ca/', 'http://whitehorse.craigslist.ca/']
EU_URLS=['http://vienna.craigslist.at/',
'http://brussels.craigslist.org/', 'http://bulgaria.craigslist.org/', 'http://zagreb.craigslist.org/', 'http://prague.craigslist.cz/', 'http://copenhagen.craigslist.org/',
'http://helsinki.craigslist.fi/', 'http://bordeaux.craigslist.org/', 'http://rennes.craigslist.org/', 'http://grenoble.craigslist.org/', 'http://lille.craigslist.org/',
'http://loire.craigslist.org/', 'http://lyon.craigslist.org/', 'http://marseilles.craigslist.org/', 'http://montpellier.craigslist.org/', 'http://cotedazur.craigslist.org/',
'http://rouen.craigslist.org/', 'http://paris.craigslist.org/', 'http://strasbourg.craigslist.org/', 'http://toulouse.craigslist.org/', 'http://berlin.craigslist.de/',
'http://bremen.craigslist.de/', 'http://cologne.craigslist.de/', 'http://dresden.craigslist.de/', 'http://dusseldorf.craigslist.de/', 'http://essen.craigslist.de/',
'http://frankfurt.craigslist.de/', 'http://hamburg.craigslist.de/', 'http://hannover.craigslist.de/', 'http://heidelberg.craigslist.de/', 'http://kaiserslautern.craigslist.de/',
'http://leipzig.craigslist.de/', 'http://munich.craigslist.de/', 'http://nuremberg.craigslist.de/', 'http://stuttgart.craigslist.de/', 'http://athens.craigslist.gr/',
'http://budapest.craigslist.org/', 'http://reykjavik.craigslist.org/', 'http://dublin.craigslist.org/', 'http://bologna.craigslist.it/', 'http://florence.craigslist.it/',
'http://genoa.craigslist.it/', 'http://milan.craigslist.it/', 'http://naples.craigslist.it/', 'http://perugia.craigslist.it/', 'http://rome.craigslist.it/', 'http://sardinia.craigslist.it/',
'http://sicily.craigslist.it/', 'http://torino.craigslist.it/', 'http://venice.craigslist.it/', 'http://luxembourg.craigslist.org/', 'http://amsterdam.craigslist.org/',
'http://oslo.craigslist.org/', 'http://warsaw.craigslist.pl/', 'http://faro.craigslist.pt/', 'http://lisbon.craigslist.pt/', 'http://porto.craigslist.pt/', 'http://bucharest.craigslist.org/',
'http://moscow.craigslist.org/', 'http://stpetersburg.craigslist.org/', 'http://alicante.craigslist.es/', 'http://baleares.craigslist.es/', 'http://barcelona.craigslist.es/',
'http://bilbao.craigslist.es/', 'http://cadiz.craigslist.es/', 'http://canarias.craigslist.es/', 'http://granada.craigslist.es/', 'http://madrid.craigslist.es/', 'http://malaga.craigslist.es/',
'http://sevilla.craigslist.es/', 'http://valencia.craigslist.es/', 'http://stockholm.craigslist.se/', 'http://basel.craigslist.ch/', 'http://bern.craigslist.ch/', 'http://geneva.craigslist.ch/',
'http://lausanne.craigslist.ch/', 'http://zurich.craigslist.ch/', 'http://istanbul.craigslist.com.tr/', 'http://ukraine.craigslist.org/']
BRIT_URLS=['http://aberdeen.craigslist.co.uk/',
'http://bath.craigslist.co.uk/', 'http://belfast.craigslist.co.uk/', 'http://birmingham.craigslist.co.uk/', 'http://brighton.craigslist.co.uk/', 'http://bristol.craigslist.co.uk/',
'http://cambridge.craigslist.co.uk/', 'http://cardiff.craigslist.co.uk/', 'http://coventry.craigslist.co.uk/', 'http://derby.craigslist.co.uk/', 'http://devon.craigslist.co.uk/',
'http://dundee.craigslist.co.uk/', 'http://norwich.craigslist.co.uk/', 'http://eastmids.craigslist.co.uk/', 'http://edinburgh.craigslist.co.uk/', 'http://essex.craigslist.co.uk/',
'http://glasgow.craigslist.co.uk/', 'http://hampshire.craigslist.co.uk/', 'http://kent.craigslist.co.uk/', 'http://leeds.craigslist.co.uk/', 'http://liverpool.craigslist.co.uk/',
'http://london.craigslist.co.uk/', 'http://manchester.craigslist.co.uk/', 'http://newcastle.craigslist.co.uk/', 'http://nottingham.craigslist.co.uk/', 'http://oxford.craigslist.co.uk/',
'http://sheffield.craigslist.co.uk/']
EA_URLS=['http://bangladesh.craigslist.org/', 'http://beijing.craigslist.com.cn/', 'http://chengdu.craigslist.com.cn/', 'http://chongqing.craigslist.com.cn/',
'http://dalian.craigslist.com.cn/', 'http://guangzhou.craigslist.com.cn/', 'http://hangzhou.craigslist.com.cn/', 'http://nanjing.craigslist.com.cn/', 'http://shanghai.craigslist.com.cn/',
'http://shenyang.craigslist.com.cn/', 'http://shenzhen.craigslist.com.cn/', 'http://wuhan.craigslist.com.cn/', 'http://xian.craigslist.com.cn/', 'http://micronesia.craigslist.org/',
'http://hongkong.craigslist.hk/']
IN_URLS=['http://ahmedabad.craigslist.co.in/', 'http://bangalore.craigslist.co.in/', 'http://bhubaneswar.craigslist.co.in/', 'http://chandigarh.craigslist.co.in/',
'http://chennai.craigslist.co.in/', 'http://delhi.craigslist.co.in/', 'http://goa.craigslist.co.in/', 'http://hyderabad.craigslist.co.in/', 'http://indore.craigslist.co.in/',
'http://jaipur.craigslist.co.in/', 'http://kerala.craigslist.co.in/', 'http://kolkata.craigslist.co.in/', 'http://lucknow.craigslist.co.in/', 'http://mumbai.craigslist.co.in/',
'http://pune.craigslist.co.in/', 'http://surat.craigslist.co.in/']
W2_URLS= ['http://jakarta.craigslist.org/', 'http://tehran.craigslist.org/', 'http://baghdad.craigslist.org/',
'http://haifa.craigslist.org/', 'http://jerusalem.craigslist.org/', 'http://telaviv.craigslist.org/', 'http://ramallah.craigslist.org/']
JAP_URLS=['http://fukuoka.craigslist.jp/',
'http://hiroshima.craigslist.jp/', 'http://nagoya.craigslist.jp/', 'http://okinawa.craigslist.jp/', 'http://osaka.craigslist.jp/', 'http://sapporo.craigslist.jp/', 'http://sendai.craigslist.jp/',
'http://tokyo.craigslist.jp/']
W1_URLS=[ 'http://seoul.craigslist.co.kr/', 'http://kuwait.craigslist.org/', 'http://beirut.craigslist.org/']
SEA_URLS=[ 'http://malaysia.craigslist.org/',
'http://pakistan.craigslist.org/', 'http://bacolod.craigslist.com.ph/', 'http://naga.craigslist.com.ph/', 'http://cdo.craigslist.com.ph/', 'http://cebu.craigslist.com.ph/',
'http://davaocity.craigslist.com.ph/', 'http://iloilo.craigslist.com.ph/', 'http://manila.craigslist.com.ph/', 'http://pampanga.craigslist.com.ph/', 'http://zamboanga.craigslist.com.ph/',
'http://singapore.craigslist.com.sg/', 'http://taipei.craigslist.com.tw/', 'http://bangkok.craigslist.co.th/', 'http://dubai.craigslist.org/', 'http://vietnam.craigslist.org/']
AU_URLS=[
'http://adelaide.craigslist.com.au/', 'http://brisbane.craigslist.com.au/', 'http://cairns.craigslist.com.au/', 'http://canberra.craigslist.com.au/', 'http://darwin.craigslist.com.au/',
'http://goldcoast.craigslist.com.au/', 'http://melbourne.craigslist.com.au/', 'http://ntl.craigslist.com.au/', 'http://perth.craigslist.com.au/', 'http://sydney.craigslist.com.au/',
'http://hobart.craigslist.com.au/', 'http://wollongong.craigslist.com.au/']
NZ_URLS=['http://auckland.craigslist.org/', 'http://christchurch.craigslist.org/', 'http://dunedin.craigslist.co.nz/',
'http://wellington.craigslist.org/']
LA_URLS=['http://buenosaires.craigslist.org/', 'http://lapaz.craigslist.org/', 'http://belohorizonte.craigslist.org/', 'http://brasilia.craigslist.org/',
'http://curitiba.craigslist.org/', 'http://fortaleza.craigslist.org/', 'http://portoalegre.craigslist.org/', 'http://recife.craigslist.org/', 'http://rio.craigslist.org/',
'http://salvador.craigslist.org/', 'http://saopaulo.craigslist.org/', 'http://caribbean.craigslist.org/', 'http://santiago.craigslist.org/', 'http://colombia.craigslist.org/',
'http://costarica.craigslist.org/', 'http://santodomingo.craigslist.org/', 'http://quito.craigslist.org/', 'http://elsalvador.craigslist.org/', 'http://guatemala.craigslist.org/',
'http://acapulco.craigslist.com.mx/', 'http://bajasur.craigslist.com.mx/', 'http://chihuahua.craigslist.com.mx/', 'http://juarez.craigslist.com.mx/', 'http://guadalajara.craigslist.com.mx/',
'http://guanajuato.craigslist.com.mx/', 'http://hermosillo.craigslist.com.mx/', 'http://mazatlan.craigslist.com.mx/', 'http://mexicocity.craigslist.com.mx/', 'http://monterrey.craigslist.com.mx/',
'http://oaxaca.craigslist.com.mx/', 'http://puebla.craigslist.com.mx/', 'http://pv.craigslist.com.mx/', 'http://tijuana.craigslist.com.mx/', 'http://veracruz.craigslist.com.mx/',
'http://yucatan.craigslist.com.mx/', 'http://managua.craigslist.org/', 'http://panama.craigslist.org/', 'http://lima.craigslist.org/', 'http://puertorico.craigslist.org/',
'http://montevideo.craigslist.org/', 'http://caracas.craigslist.org/']
SA_URLS=['http://virgin.craigslist.org/', 'http://cairo.craigslist.org/', 'http://addisababa.craigslist.org/',
'http://accra.craigslist.org/', 'http://kenya.craigslist.org/', 'http://casablanca.craigslist.org/', 'http://capetown.craigslist.co.za/', 'http://durban.craigslist.co.za/',
'http://johannesburg.craigslist.co.za/', 'http://pretoria.craigslist.co.za/', 'http://tunis.craigslist.org/']
tok = string.letters + string.digits + ' '

def get_cl(cc='au'):
    res = []
    allsites = urllib2.urlopen(allurl).read()
    soup = BeautifulSoup(allsites,'html.parser')
    for a in soup.find_all('a', href=True):
        url = a['href']
        if cc == None or url.endswith('%s/' % cc): # by country or (god help us) all
            res.append('http:%s' % url) # drop trailing url
    return res



class craigsList():
    """
    """

    def __init__(self,resetdb = False):
        tod = datetime.datetime.today()
        self.startt = time.time()
        self.PAGE_STORE = '%s/%s' % (PAGE_STORE,tod.strftime('%Y%m%d')) # where to store fresh url contents by date
        try:
            os.makedirs(self.PAGE_STORE)
        except:
            pass
        self.ul = len(urls)
        self.urlseen = 0
        self.wickrseen = 0
        self.urlnew = 0
        self.wickrnew = 0
        self.feeds = []
        self.wickrs = {}
        self.titles = {}
        self.pagesseen = {}
        self.partitlist = ['wickr','wicker','wikr','wicr']
        # various mis-spellings
        # ugly hack warning - potential wickr ids but common words
        # eg messenger from plays store or App Store and get to me within seconds
        self.ignore = ['account', 'application', 'apps','appstore','available','avoid','asap','best','below','beware','brisbane',
                   'canberra','chat',
                   'city','contact', 'create', 'delivery','central','deal','deals',
                  'deliveries','detail','details','email','have', 'here','hook',
                  'dispensary', 'dope','download', 'free', 'friend','from','green','great','hash', 'hydro', 'interested', 'interest',
                  'interesting','local','locally','look','looks','make','menu','message','messages','messenger', 'messengers',
                  'more', 'number','id','have','name','names','info','help',
                  'medical','medicine','medicinal','offers','only', 'phone', 'play', 'plays','sale','sales','scams','scam',
                  'post','posted','posting','price','sale','sales','seconds','send', 'service','services', 'store','soon',
                  'southyarra','text', 'then','time', 'tree','trees','unsolicited','updated','update','wicka',
                  'username','userid','whatsapp', 'weed','white','what', 'wick','wicker','wickrid','wickr', 'wicr', 'wikr',
                  'with', 'within','your','youre']
        # hand tuned when crap appears in outputs

        self.con = lite.connect('clscanscam.db')
        self.cur = self.con.cursor()

        if resetdb:
            self.cur.execute("DROP TABLE IF EXISTS wickrs")
            self.cur.execute("DROP TABLE IF EXISTS urls")
            self.cur.execute("CREATE TABLE wickrs(Id INTEGER PRIMARY KEY, Wickr TEXT UNIQUE, Places TEXT, Firstseen timestamp, Lastseen timestamp)")
            self.cur.execute("CREATE TABLE urls(Id INTEGER PRIMARY KEY, Url TEXT, Wickrs TEXT, Titles TEXT, Firstseen timestamp, Lastseen timestamp)")
            self.refill_db()
            self.con.commit()
        # should fill db from all urls saved so far under PAGE_STORE
        ku = self.cur.execute("SELECT Url FROM urls")
        ku = self.cur.fetchall()
        ku = [x[0] for x in ku]
        print '## known urls[:3] =',ku[:10]
        self.knownurls = dict(zip(ku,ku))
        kw = self.cur.execute("SELECT Wickr,Places FROM wickrs")
        kw = self.cur.fetchall()
        kwl = [x[0] for x in kw]
        print '## known wickrs[:10] =',kwl[:10]
        self.knownwickrs = dict(zip(kwl,kwl))
        import socket
        if hasattr(socket, 'setdefaulttimeout'):
            logging.debug('socket has a timeout parameter. w00t!')
            socket.setdefaulttimeout(20)

    def refill_db(self):
        now = datetime.datetime.now()
        for directory, dirnames, filenames in os.walk(PAGE_STORE):
            filenames = [x for x in filenames if (x.endswith('.html'))]
            if len(filenames) > 0:
               for fn in filenames:
                    fname = os.path.join(directory,fn)
                    iurl = 'http://%s' % '/'.join(fn.split('_'))
                    try:
                        page = open(fname).read()
                    except:
                        logging.debug('page %s timed out?' % iurl)
                        continue
                    psoup = BeautifulSoup(page, 'html.parser')
                    pall = psoup.findAll(text=True)
                    town = fn.split('.')[0]
                    w = self.get_wickr(pall)
                    try:
                        t = self.get_atitle(psoup.title.string)
                    except:
                        t = None
                        continue
                    if w:
                        oldrecs = self.cur.execute('SELECT Wickr, Places, Lastseen AS "[timestamp]" from wickrs WHERE Wickr = ? ', (w,))
                        oldrec = self.cur.fetchone()
                        if oldrec:
                            oldplaces = oldrec[1].split(',')
                            olddt = oldrec[2]
                            oldseen = datetime.datetime.strptime(olddt, "%Y-%m-%d %H:%M:%S.%f")
                            if now > oldseen:
                                nr = (now,w)
                                self.cur.execute("UPDATE wickrs SET Lastseen = ? WHERE Wickr = ? ",nr)
                                self.con.commit()
                            both = copy.copy(oldplaces)
                            both.append(town)
                            p = set(both)
                            if len(p) > len(oldplaces):
                                nr = (','.join(p), w)
                                s = '## updating wickr id %s seen in places %s' % (w,nr[0])
                                print s
                                logging.debug(s)
                                self.cur.execute("UPDATE wickrs SET Places = ? WHERE Wickr = ? ",nr)
                                self.con.commit()
                        else:
                            nr = (None,w,town,now,now)
                            self.cur.execute("INSERT INTO wickrs VALUES(?, ?, ?, ?, ?)", nr)
                            self.con.commit()
                            self.wickrnew += 1
                            self.knownwickrs[w] = w
                        self.wickrseen += 1
                    nr = (None,iurl,w,t,now,now)
                    self.cur.execute("INSERT INTO urls VALUES(?, ?, ?, ?, ?, ?)", nr)
                    self.knownurls[iurl] = iurl
                    self.con.commit()
                    self.urlnew += 1




    def get_wickr(self,rawv):
        # tricky - fugly and still not right

        def is_visible(e):
            if e.parent.name in ['style', 'script', '[document]', 'head', 'meta']:
                return False
            elif isinstance(e,element.Comment):
                return False
            return True

        punctregex = re.compile('[%s]' % re.escape(string.punctuation))

        visib = filter(is_visible, rawv)
        pd = ' '.join(visib)
        pd = pd.lower()
        pd = punctregex.sub(' ', pd)
        pd = ''.join([x for x in pd if x in tok])

        rawin = ' '.join(pd.split())

        w = None
        ## print '## in get_wickr on rawv = "%s"' % rawin
        for partit in self.partitlist:
            rest = rawin
            while rest > '' and not w:
                pre,wkey,rest = rest.partition(partit)
                rest = rest.strip()
                if rest > '':
                    restw = rest.split(' ')
                    for i in range(len(restw)):
                        w = restw[i].strip()
                        # print('### partit %s at i=%d seeing %s in "%s" ###' % (partit,i,w,rest))
                        if w[0] in string.digits or len(w) < 4 or len(w) > 16 or w in self.ignore: # wickr id rules
                            # https://wickr.desk.com/customer/en/portal/articles/2341565-what-is-a-wickr-id-can-i-change-my-wickr-id-
                            w = None
                            continue
                        else:
                            break
            if w:
                break
        if not w and VERBOSE:
            logging.debug( '### no wickr found in entire text %s ###' % rawin)
        return w


    def process_url(self,iurl):
        """ process new url - read and save"""
        now = datetime.datetime.now()
        try:
            page = urllib2.urlopen(iurl).read()
        except:
            logging.debug('process_url urlopen page %s timed out?' % iurl)
            return(None,None)
        fname = iurl.split('http://')[1]
        fname = fname.replace('/','_') # sanitise
        outf = '%s/%s' % (self.PAGE_STORE,fname)
        o = open(outf,'w')
        o.write(page)
        o.close()
        logging.debug('# wrote out %s to %s' % (iurl,outf))
        psoup = BeautifulSoup(page, 'html.parser')
        pall = psoup.findAll(text=True)
        w = self.get_wickr(pall)
        logging.debug('process url: w = %s' % w)
        t = str(psoup.html.head.title).decode('utf-8')
        t = t[7:-8]
        return (w,t)

    def add_awickr(self,w,town,titl):
        if not w in self.titles[titl]['wickrs']:
            self.titles[titl]['wickrs'].append(w)
        self.wickrs.setdefault(w,None)
        if self.wickrs[w] == None:
            self.wickrs[w] = {'towns': [town,],'titles': ['"%s"' % titl,]}
        else:
            if not town in self.wickrs[w]['towns']:
                self.wickrs[w]['towns'].append(town)
            if not titl in self.wickrs[w]['titles']:
                self.wickrs[w]['titles'].append('"%s"' % titl)

    def get_atitle(self,titl):
        tsoup = BeautifulSoup(titl, 'html.parser')
        t = tsoup.get_text()
        t = ''.join(x for x in t if x in tok)
        t = re.sub(' +',' ', t)
        t = re.sub('\n+',' ', t)
        t = t.lower()
        return t

    def add_atitle(self,titl,town):
        self.titles.setdefault(titl,None)
        if self.titles[titl] == None:
            self.titles[titl] = {'towns':[town,],'wickrs':[]}
        else:
            if not town in self.titles[titl]['towns']:
                self.titles[titl]['towns'].append(town)


    def process_urls(self,searchurls):
        # search a list of cl search urls rss feeds for new posting urls and save
        # process new urls and add their content to the
        self.searchurls = searchurls
        nurl = len(searchurls)
        now = datetime.datetime.now()
        for i,ur in enumerate(searchurls):
            town = ur.split('http://')[1].split('.')[0]
            logging.debug('Town = %s' % town)
            hrefs = []
            for s in SEARCH_TERMS:
                url = BASE_URL % (ur,s)
                try:
                    page = urllib2.urlopen(url).read()
                    soup = BeautifulSoup(page, 'html.parser')
                except:
                    logging.debug('process_urls rss parse page %s timed out?' % url)
                    continue

                # rows = soup.body.find('p', attrs={'class': 'row'})
                cont = soup.body.find('div', attrs={'class': 'content'})
                for url in cont.find_all('a'):
                    h = url.attrs['href']
                    if (not h.startswith('http')):
                        hr = '%s%s' % (ur,h[1:])
                        hrefs.append(hr)
                    else:
                        hrefs.append(h)
            alls = list(set(hrefs)) # remove redundance
            print('%s gave %d urls - %s' % (url,len(alls),alls[:10]))

            print '@ %d secs, %s searches returned %d urls with %d to go' % (int(time.time()-self.startt),town,
              len(alls),nurl-i-1)
            for iurl in alls:
                iurl = iurl.decode()
                self.urlseen += 1
                if self.knownurls.setdefault(iurl,None) == None:
                    w,t = self.process_url(iurl)
                    print '##new url',iurl,'w = ',w,'t=',t
                    now = datetime.datetime.now()
                    newrec = (None,iurl,w,t,now,now)
                    self.cur.execute("INSERT INTO urls VALUES(?, ?, ?, ?, ?, ?)", newrec)
                    self.urlnew += 1
                    self.knownurls[iurl] = iurl
                else:
                    print '##old url',iurl
                    oldurls = self.cur.execute("SELECT Wickrs,Titles FROM urls WHERE Url = ?", (iurl,))
                    oldurl = self.cur.fetchone()
                    w = oldurl[0]
                    t = oldurl[1]
                    print '##old url',iurl,'w = ',w,'t=',t

                self.add_atitle(t,town)
                if w > '':
                    if len(w) >= 4:
                        if self.knownwickrs.setdefault(w,None) == None:
                            now = datetime.datetime.now()
                            newrec = (None,w,town,now,now)
                            self.cur.execute("INSERT INTO wickrs VALUES(?, ?, ?, ?, ?)", newrec)
                            self.wickrnew += 1
                            self.add_awickr(w,town,t)
                            self.knownwickrs[w] = w
                        else:
                            oldrecs = self.cur.execute('SELECT Wickr, Places, Lastseen AS "[timestamp]" from wickrs WHERE Wickr = ? ', (w,))
                            oldrec = self.cur.fetchall()
                            if oldrec:
                                oldplaces = oldrec[0][1].split(',')
                                oldseen = oldrec[0][2]
                                oldseen = datetime.datetime.strptime(oldseen, "%Y-%m-%d %H:%M:%S.%f")
                                if now > oldseen:
                                    nr = (now,w)
                                    self.cur.execute("UPDATE wickrs SET Lastseen = ? WHERE Wickr = ? ",nr)
                                both = oldplaces
                                both.append(town)
                                p = set(both)
                                if len(p) > len(oldplaces):
                                    nr = (','.join(p), w)
                                    self.cur.execute("UPDATE wickrs SET Places = ? WHERE Wickr = ? ",nr)
                                    print 'updating',w,'with places',nr[0]
                                for platz in both: # make sure we have the historical record, not just today
                                    self.add_awickr(w,platz,t)
                                self.wickrseen += 1
                            else:
                                logging.debug('## odd. no db entry for wickr %s' % w)

                        self.add_awickr(w,town,t)
                    else:
                        s = '### adding wickr %s but len < 4 - wtf' % w
                        print s
                        logging.warning(s)
            self.con.commit()


logfileName = 'clScamScan.log'

logging.basicConfig(filename=logfileName,level=0,format='%(levelname)-8s @ %(asctime)s: %(message)s')
logging.info('### clscamscan starting ### ')
# NO wickr in Latin American sites 420 search!
# hardly any in EU
urls = AU_URLS# AU_URLS # EU_URLS # US_URLS # AU_URLS # get_cl('au')
# ['http://sydney.craigslist.com.au/',]
# try 'org' to get banned quickly)
print 'urls=',urls
cl = craigsList(resetdb = False)
cl.process_urls(urls)
cl.con.close()
logging.debug('Saw %d wickrs and %d urls. Added %d wickrs and %d urls' % (cl.urlseen,cl.wickrseen,cl.urlnew,cl.wickrnew))


res = [(len(cl.wickrs[w]['towns']),w,','.join(cl.wickrs[w]['towns']),\
         ','.join(set(cl.wickrs[w]['titles']))) for w in cl.wickrs.keys()]
res.sort(reverse=True)
wres = ['    wickr id %s is on %d CL cities (%s)\n' % \
        (x[1],x[0],x[2]) for x in res if x[1] <> 'None']

print '\n\n### found wickr ids in cities:'
print ''.join(wres)
tres = []
print 'cl.titles.keys()=',cl.titles.keys()[:10]
for t in cl.titles.keys():
    try:
        nt = len(cl.titles[t]['towns'])
        ts = t.encode("ascii", "ignore")
        towns = ','.join(cl.titles[t]['towns'])
        titles = cl.titles[t]['wickrs']
        tres.append((nt,ts,towns,titles))
    except:
        print 'failed for t=',t
        pass

if False:
    for i,t in enumerate(tres):
        if t:
            if len(t[3]) < 1:
                tres[i][3] = 'not found'
            if len(t[1]) > 40:
                tres[i][1] = '%s...' % tres[i][1][:40]
tres.sort(reverse=True)
tres = ['%s is on %d CL towns %s wickr id = "%s"\n' % \
        (x[1],x[0],x[2],x[3]) for x in tres]
print '\n\nTitles by city and wickr'
print ''.join(tres)

