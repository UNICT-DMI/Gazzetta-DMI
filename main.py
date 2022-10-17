from utils.factory import get_site_from_settings_file
from utils.resources import read_all_sent_announcements, write_all_sent_announcements

sites = get_site_from_settings_file("data/settings.yaml")

def send_wrapper(site, announcement):
    try:
        site.send_announcement(announcement['pointer'], announcement['data'])
    except ValueError as err:
        site.bot.send_documents_error_message(err)

def main():
    sent_announcements = read_all_sent_announcements('data/sent_announcements.yaml')
    first_run = sent_announcements is None or len(sent_announcements) != len(sites)
    dump_announcements = {}

    for site in sites:
        try:
            new_announcements = site.get_all_announcements()
            dump_announcements[site.name] = [x['data'] for x in new_announcements]
            if not first_run:
                relevant_sent_announcements = sent_announcements[site.name]
                for announcement in new_announcements:
                    needs_sending = site.already_sent(announcement['data'], relevant_sent_announcements)
                    if  any(needs_sending.values()):
                        send_wrapper(site, announcement)
            
        except Exception as e:
            site.handle_error(e)

    write_all_sent_announcements('data/sent_announcements.yaml', dump_announcements)


if __name__ == '__main__':
    main()
