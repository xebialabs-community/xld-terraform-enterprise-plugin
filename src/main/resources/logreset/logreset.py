import logging
import logging.config


def reset_logging(conf=None):
    """ Reset logging.
    
    Removes any configured handlers and filters.
    Sets new configuration (if provided).
    """
    root = logging.getLogger()
    list(map(root.removeHandler, root.handlers[:]))
    list(map(root.removeFilter, root.filters[:]))
    if not (conf is None):
        logging.config.dictConfig(conf)

