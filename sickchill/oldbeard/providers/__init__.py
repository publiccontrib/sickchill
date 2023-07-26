import sys
from random import shuffle
from typing import List, Union

from sickchill.oldbeard.providers.newznab import NewznabProvider
from sickchill.oldbeard.providers.rsstorrent import TorrentRssProvider
from sickchill.providers.GenericProvider import GenericProvider
from sickchill.providers.torrent import TorrentProvider
from sickchill.providers.nzb import NZBProvider

import sickchill.oldbeard.helpers
from sickchill import settings
from sickchill.oldbeard.providers import (
    abnormal,
    alpharatio,
    archetorrent,
    binsearch,
    bitcannon,
    bjshare,
    btn,
    cpasbien,
    danishbits,
    demonoid,
    elitetorrent,
    eztv,
    filelist,
    gimmepeers,
    hd4free,
    hdbits,
    hdspace,
    hdtorrents,
    hdtorrents_it,
    horriblesubs,
    hounddawgs,
    ilcorsaronero,
    immortalseed,
    iptorrents,
    kat,
    limetorrents,
    magnetdl,
    morethantv,
    ncore,
    nebulance,
    newpct,
    norbits,
    nyaa,
    omgwtfnzbs,
    pretome,
    rarbg,
    scc,
    scenetime,
    shazbat,
    skytorrents,
    speedcd,
    thepiratebay,
    tntvillage,
    tokyotoshokan,
    torrent9,
    torrent911,
    torrent_paradise,
    torrentbytes,
    torrentday,
    torrentleech,
    torrentproject,
    torrentz,
    tvchaosuk,
    xthor,
    yggtorrent,
)

__all__ = [
    "abnormal",
    "alpharatio",
    "archetorrent",
    "binsearch",
    "bitcannon",
    "bjshare",
    "btn",
    "cpasbien",
    "danishbits",
    "demonoid",
    "elitetorrent",
    "eztv",
    "filelist",
    "gimmepeers",
    "hd4free",
    "hdbits",
    "hdspace",
    "hdtorrents",
    "hdtorrents_it",
    "horriblesubs",
    "hounddawgs",
    "ilcorsaronero",
    "immortalseed",
    "iptorrents",
    "kat",
    "limetorrents",
    "magnetdl",
    "morethantv",
    "ncore",
    "nebulance",
    "newpct",
    "norbits",
    "nyaa",
    "omgwtfnzbs",
    "pretome",
    "rarbg",
    "scc",
    "scenetime",
    "shazbat",
    "skytorrents",
    "speedcd",
    "thepiratebay",
    "tntvillage",
    "tokyotoshokan",
    "torrent9",
    "torrent911",
    "torrent_paradise",
    "torrentbytes",
    "torrentday",
    "torrentleech",
    "torrentproject",
    "torrentz",
    "tvchaosuk",
    "xthor",
    "yggtorrent",
]

broken_providers = [
    # 'torrentz', 'yggtorrent'
]


def sorted_provider_list(randomize=False) -> List[Union[TorrentProvider, NZBProvider, TorrentRssProvider, NZBProvider, GenericProvider]]:
    initialList = settings.providerList + settings.newznab_provider_list + settings.torrent_rss_provider_list
    provider_dict = {x.get_id(): x for x in initialList}

    new_provider_list = []

    # add all modules in the priority list, in order
    for current_module in settings.PROVIDER_ORDER:
        if current_module in provider_dict:
            new_provider_list.append(provider_dict[current_module])

    # add all enabled providers first
    for current_module in provider_dict:
        if provider_dict[current_module] not in new_provider_list and provider_dict[current_module].is_enabled:
            new_provider_list.append(provider_dict[current_module])

    # add any modules that are missing from that list
    for current_module in provider_dict:
        if provider_dict[current_module] not in new_provider_list:
            new_provider_list.append(provider_dict[current_module])

    if randomize:
        shuffle(new_provider_list)

    return new_provider_list


def makeProviderList():
    # noinspection PyUnresolvedReferences
    return [x.Provider() for x in (getProviderModule(y) for y in __all__ if y not in broken_providers) if x]


def getProviderModule(name):
    name = name.lower()
    prefix = "sickchill.oldbeard.providers."
    if name in __all__ and prefix + name in sys.modules:
        return sys.modules[prefix + name]
    else:
        raise Exception("Can't find " + prefix + name + " in " + "Providers")


def getProviderClass(provider_id):
    provider_match = [x for x in settings.providerList + settings.newznab_provider_list + settings.torrent_rss_provider_list if x and x.get_id() == provider_id]

    if len(provider_match) != 1:
        return None
    else:
        return provider_match[0]


def check_enabled_providers():
    if not settings.DEVELOPER:
        backlog_enabled, daily_enabled = False, False
        for provider in sorted_provider_list():
            if provider.is_active:
                if provider.enable_daily and provider.can_daily:
                    daily_enabled = True

                if provider.enable_backlog and provider.can_backlog:
                    backlog_enabled = True

                if backlog_enabled and daily_enabled:
                    break

        if not (daily_enabled and backlog_enabled):
            searches = ((_("daily searches and backlog searches"), _("daily searches"))[backlog_enabled], _("backlog searches"))[daily_enabled]
            formatted_msg = _(
                "No NZB/Torrent providers found or enabled for {searches}.<br/>" 'Please <a href="{web_root}/config/providers/">check your settings</a>.'
            )
            sickchill.oldbeard.helpers.add_site_message(
                formatted_msg.format(searches=searches, web_root=settings.WEB_ROOT), tag="no_providers_enabled", level="danger"
            )
        else:
            sickchill.oldbeard.helpers.remove_site_message(tag="no_providers_enabled")
