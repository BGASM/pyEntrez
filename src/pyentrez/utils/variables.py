APPSETTING = [
    {
        'args': ['-c', '--credentials'],
        'kwargs': {
            'action': 'store_true',
            'default': False,
            'help': 'Allow user to set DB credentials on application start.',
        },
        # 'setting': {'envar': <envar>, 'text': <text>}
    },
    {
        'args': ['--version'],
        'kwargs': {
            'action': 'store_true',
            'default': False,
            'help': 'Print pyEntrez version information',
        },
        # 'setting': {'envar': <envar>, 'text': <text>}
    },
    {
        'args': ['-I', '--INIT'],
        'kwargs': {
            'action': 'store_true',
            'default': False,
            'help': 'First time run, set workspace path.',
        },
        # 'setting': {'envar': <envar>, 'text': <text>}
    },
    {
        'args': ['--TUI'],
        'kwargs': {
            'type': str,
            'choices': ['on', 'off'],
            'default': 'on',
            'help': '''Start in TUI mode
        or commandline. Default = off.''',
        },
        # 'setting': {'envar': <envar>, 'text': <text>}
    },
    {
        'args': ['--mongo'],
        'kwargs': {
            'action': 'store_true',
            'default': False,
            'help': '''Use mongoDB
        or commandline. Default = off.''',
        },
        'setting': {'envar': 'PYENT_MONGO', 'text': 'mongo'},
    },
    {
        'args': ['--cloud'],
        'kwargs': {
            'action': 'store_true',
            'default': False,
            'help': '''Use mongoDB
        on cloud or local. Default = False.''',
        },
        'setting': {'envar': 'PYENT_CLOUD', 'text': 'cloud'},
    },
    {
        'args': ['--uri'],
        'kwargs': {
            'type': str,
            'help': '''If using cloud mongoDB
       enter uri.''',
        },
        'setting': {'envar': 'PYENT_URI', 'text': 'uri'},
    },
    {
        'args': ['--host'],
        'kwargs': {
            'type': str,
            'help': '''MongoDB host.''',
        },
        'setting': {'envar': 'PYENT_HOST', 'text': 'host'},
    },
    {
        'args': ['--port'],
        'kwargs': {
            'type': str,
            'help': '''MongoDB port.''',
        },
        'setting': {'envar': 'PYENT_PORT', 'text': 'port'},
    },
    {
        'args': ['--verbose', '-v'],
        'kwargs': {
            'action': 'count',
            'default': 0,
            'help': '''Set verbosity of log output.''',
        },

    },
    {
        'args': ['-o', '--output'],
        'kwargs': {
            'type': str,
            'default': 'stderr',
            'help': '''Set path for log output.''',
        },

    },
]
ENTREZSETTINGS = [
    {
        'args': ['--email'],
        'kwargs': {'type': str, 'help': 'E-mail is required.'},
        'setting': {'envar': 'PYENT_EMAIL', 'text': 'email'},
    },
    {
        'args': ['--db'],
        'kwargs': {'type': str, 'default': 'pubmed', 'help': 'NCBI database, default = pubmed'},
        'setting': {'envar': 'PYENT_DB', 'text': 'db'},
    },
    {
        'args': ['--sort'],
        'kwargs': {
            'type': str,
            'default': 'relevance',
            'help': '''Specifies the method used to sort UIDs in the
        ESearch output. The available values vary by database (db) and may be found in the Display
        Settings menu on an Entrez search results page. Default = relevance''',
        },
        'setting': {'envar': 'PYENT_SORT', 'text': 'sort'},
    },
    {
        'args': ['--retmax'],
        'kwargs': {
            'type': int,
            'default': 20,
            'help': '''Total number of records from the input set to be
        retrieved, up to a maximum of 10,000. Optionally, for a large set the value of
        retstart can be iterated while holding retmax constant, thereby downloading
        the entire set in batches of size retmax. Default = 20''',
        },
        'setting': {'envar': 'PYENT_RETMAX', 'text': 'retmax'},
    },
    {
        'args': ['--retmode'],
        'kwargs': {
            'type': str,
            'default': 'txt',
            'help': '''Retrieval type. Determines the format of the
        returned output. XML and JSON are supported on ESearch. Default = txt''',
        },
        'setting': {'envar': 'PYENT_RETMODE', 'text': 'retmode'},
    },
    {
        'args': ['--rettype'],
        'kwargs': {
            'type': str,
            'default': 'medline',
            'help': '''Retrieval type. This parameter specifies the
        record view returned, such as Abstract or MEDLINE from PubMed, or GenPept or FASTA from protein.
        Default = medline''',
        },
        'setting': {'envar': 'PYENT_RETTYPE', 'text': 'rettype'},
    },
    {
        'args': ['--usehistory'],
        'kwargs': {
            'type': str,
            'default': None,
            'help': 'set to "y" to use ESearch History server. Default = "n"',
        },
        'setting': {'envar': 'PYENT_USEHISTORY', 'text': 'usehistory'},
    },
    {
        'args': ['--field'],
        'kwargs': {
            'type': str,
            'default': None,
            'help': '''if used the entire search'
         term will be limited to this field. Default = "None"''',
        },
        'setting': {'envar': 'PYENT_FIELD', 'text': 'field'},
    },
    {
        'args': ['--datetype'],
        'kwargs': {
            'type': str,
            'default': 'edat',
            'help': '''Type of date used to limit a search.
         The allowed values vary between Entrez databases, but common values are 'mdat' (modification date),
          'pdat' (publication date) and 'edat' (Entrez date). Default = edat''',
        },
        'setting': {'envar': 'PYENT_DATETYPE', 'text': 'datetype'},
    },
    {
        'args': ['--reldate'],
        'kwargs': {
            'type': int,
            'default': None,
            'help': '''When reldate is set to an integer n, the
        search returns only those items that have a date specified by datetype within the last n days.
        Default is = -1.''',
        },
        'setting': {'envar': 'PYENT_RELDATE', 'text': 'reldate'},
    },
    {
        'args': ['--mindate'],
        'kwargs': {
            'type': str,
            'default': None,
            'help': '''Date range used to limit a search result by
        the date specified by datetype. Format is YYYY/MM/DD, YYYY, YYYY/MM. Must be used with maxdate.
        Default = None''',
        },
        'setting': {'envar': 'PYENT_MINDATE', 'text': 'mindate'},
    },
    {
        'args': ['--maxdate'],
        'kwargs': {
            'type': str,
            'default': None,
            'help': '''Date range used to limit a search result by
        the date specified by datetype. Format is YYYY/MM/DD, YYYY, YYYY/MM. Must be used with mindate.
        Default = None''',
        },
        'setting': {'envar': 'PYENT_MAXDATE', 'text': 'maxdate'},
    },
    {
        'args': ['--webenv'],
        'kwargs': {
            'type': str,
            'default': None,
            'help': '''If using history, this will be the webenv''',
        },
        'setting': {'envar': 'PYENT_WEBENV',  'text': 'webenv'},
    },
    {'setting': {'envar': 'PYENT_QUERYKEY', 'text': 'query_key'}},
    {'setting': {'envar': 'PYENT_RETSTART', 'text': 'retstart'}},
    {'setting': {'envar': 'PYENT_USER', 'text': 'user'}},
]

DBSETTINGS = [
    {
        'args': ['--dbURI'],
        'kwargs': {'type': str, 'help': 'Mongo URI'},
        # 'setting': {'envar': 'PYENT_DBURI', 'text': 'uri'}
    },
    {
        'args': ['--dbuser'],
        'kwargs': {'type': str, 'help': 'DB username.'},
        # 'setting': {'envar': 'PYENT_DBUSER', 'text': 'dbuser'}
    },
]

setting_vars = {
    'APPSETTING': APPSETTING,
    'ENTREZSETTINGS': ENTREZSETTINGS,
    'DBSETTINGS': DBSETTINGS,
}


def get_settings():
    return setting_vars
