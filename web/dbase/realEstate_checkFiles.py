#!/usr/bin/env python
'''
Script to check integrity and completness of real estate source data files
! Directories are hard coded
'''
import datetime
from tools import *
from globals import *
from output import *
import codecs

# Importing DJANGO things
import sys
import os
import django
sys.path.append('/Users/nico/Code/tasador/web/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

# Models
from realestate.models import RealEstate
from building.models import Building
from apartment.models import Apartment

from region.models import Region
from commune.models import Commune

datapath = REALSTATE_DATA_PATH+'/source'

regions = Region.objects.filter(code=13) # por ahora solo R.M.
communes = Commune.objects.all()

out = messenger(open('logs/datafiles','w'))

for region in regions:
    basepath = datapath+'/{}/'.format(slugify(region.name))
    if not os.path.isdir(basepath):
        out.warning('{} DIRECTORY DOES NOT EXIST'.format(region.name))
    else:
        out.say('{} DIR OK'.format(region.name))

    communes_region = communes.filter(region=region)
    for commune in communes_region:
        basepath = datapath+'/{}/{}/'.format(
            slugify(region.name),
            slugify(commune.name))
        if not os.path.isdir(basepath):
            out.error('{} DIRECTORY NOT FOUND'.format(commune.name))
        else:
            out.say('{} DIR OK'.format(commune.name))

        sources = ['PortalInmobiliario']

        for source in sources:
            basepath = basepath+'/'+source
            if not os.path.isdir(basepath):
                out.error('{} {} DIRECTORY NOT FOUND'.format(commune.name,source))
                continue

            out.say('{} {} OK'.format(commune.name,source))

            pfile = basepath+'/{}_urls_PI.json'.format(slugify(commune.name))
            if not os.path.isfile(pfile):
                tmp = basepath+'/{}_urls_PI.json'.format(slugify(commune.name,only_ascii=True))
                if not os.path.isfile(tmp):
                    out.error('{} {} URLS FILE NOT FOUND'.format(commune.name,source))
                    continue
                else:
                    out.warning('{} {} URLS FILE FALTA TILDE?'.format(commune.name,source))
                    pfile = tmp

            data = json.load(open(pfile))
            out.say('{} {} URLS: {}'.format(commune.name,source,len(data)))

            pfile = basepath+'/{}_properties_PI.json'.format(slugify(commune.name))
            if not os.path.isfile(pfile):
                tmp = basepath+'/{}_properties_PI.json'.format(slugify(commune.name,only_ascii=True))
                if not os.path.isfile(tmp):
                    out.error('{} {} PROPERTIES FILE DOES NOT EXIST'.format(commune.name,source))
                    continue
                else:
                    out.warning('{} {} PROPERTIES FILE FALTA TILDE?'.format(commune.name,source))
                    pfile = tmp

            data = json.load(open(pfile))
            out.say('{} {} PROPERTIES FILE PROPERTIES: {}'.format(commune.name,source,len(data)))

            dirs = [a for a in glob.glob(basepath + '/*') if os.path.isdir(a)]
            if len(dirs) == 0:
                out.warning('{} {} NO DATA DIRECTORY'.format(commune.name,source))
            for d in dirs:
                date = datetime.datetime.strptime(d[d.rfind('/')+1:],"%Y-%m-%dT%H-%M-%S")
                out.say('{} {} {} OK'.format(commune.name,source,date))

                file_suffixs = ['aptarment_appraisal_data_{}.json'.format('portali'),
                                'aptarment_data_{}.json'.format('portali'),
                                'building_data_{}.json'.format('portali'),
                                'house_data_{}.json'.format('portali')]

                for file_suffix in file_suffixs:
                    filename = d+'/{}_{}'.format(slugify(commune.name),file_suffix)
                    if not os.path.isfile(filename):
                        tmp = d+'/{}_{}'.format(slugify(commune.name,only_ascii=True),file_suffix)
                        if not os.path.isfile(tmp):
                            out.warning('{} {} {} {} NOT FOUND'.format(commune.name,source,date,file_suffix))
                            continue
                        else:
                            out.warning('{} {} {} {} FALTA TILDE?'.format(commune.name,source,date,file_suffix))
                            filename = tmp

                    data = json.load(codecs.open(filename, 'r', 'utf-8-sig'))
                    out.say('{} {} {} {} # = {}'.format(commune.name,source,date,file_suffix,len(data)))
