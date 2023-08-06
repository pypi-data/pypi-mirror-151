import hashlib
import json
import os
import pickle
from datetime import datetime
from decimal import Decimal
import time


def cached():
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """

    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(*args, **kwargs):  # define a wrapper that will finally call "fn" with all arguments
            path = args[0].cache_path
            active = args[0].cache
            debug = args[0].debug
            ttl = args[0].cache_ttl
            cache_file = f'{path}{hashlib.md5(json.dumps(args[1:]).encode("utf-8")).hexdigest()}.one_cache'
            # if cache exists -> load it and return its content
            if debug:
                if not os.path.exists(cache_file):
                    print(f"{cache_file} not exist")
            if os.path.exists(cache_file) and active:
                created_at = int(os.path.getctime(cache_file))
                diff = int(time.time()) - created_at
                if diff < ttl:
                    if debug:
                        print(f"Cache created {diff} seg ago, current tll {ttl} seg")
                    with open(cache_file, 'rb') as cachehandle:
                        if debug:
                            print(f"using cached result from {cache_file}")
                        return pickle.load(cachehandle)

                if debug:
                    if diff > ttl:
                        print(f"Cache created {diff} seg ago, current tll {ttl} seg, renewing cache file.")

            # execute the function with all arguments passed
            res = fn(*args, **kwargs)

            # write to cache file
            if active:
                with open(cache_file, 'wb') as cachehandle:
                    if debug:
                        print("saving result to cache '%s'" % cache_file)
                    pickle.dump(res, cachehandle)

            return res

        return wrapped

    return decorator  # return this "customized" decorator that uses "cachefile"


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def get_iso_8601_date():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
