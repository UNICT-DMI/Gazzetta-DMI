import yaml

from utils.site import Site

import sites.bandi
import sites.cdd
import sites.paritetica



def get_site_from_settings_file(filename: str) -> list['Site']:
        objs = []
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            for sito in data:
                name, link, token, chat_id, dev_chat_ids = sito.values()
                if 'Bandi DMI' in name:
                    objs.append(sites.bandi.Bandi(name, link, token, chat_id, dev_chat_ids))
                elif 'Consiglio di dipartimento' in name:
                    objs.append(sites.cdd.CDD(name, link, token, chat_id, dev_chat_ids))
                elif 'Commissione paritetica' in name:
                    objs.append(sites.paritetica.Paritetica(name, link, token, chat_id, dev_chat_ids))
                else:
                    objs.append(Site(name, link, token, chat_id, dev_chat_ids))
        return objs