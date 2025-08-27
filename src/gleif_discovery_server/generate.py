# -*- encoding: utf-8 -*-
"""
vLEI module

"""

import argparse
import json
import os
from pathlib import Path

from keri.core import coring, scheming


def populate_saids(
    d: dict, idage: str = coring.Saids.dollar, code: str = coring.MtrDex.Blake3_256
):
    if "properties" in d:
        props = d["properties"]

        # check for top level ids
        for v in ["a", "e", "r"]:
            if v in props and "$id" in props[v]:
                vals = props[v]
                vals[idage] = coring.Saider(sad=vals, code=code, label=idage).qb64
            elif v in props and "oneOf" in props[v]:
                if isinstance(props[v]["oneOf"], list):
                    # check each 'oneOf' for an id
                    ones = props[v]["oneOf"]
                    for o in ones:
                        if isinstance(o, dict) and idage in o:
                            o[idage] = coring.Saider(sad=o, code=code, label=idage).qb64

    d[idage] = coring.Saider(sad=d, code=code, label=idage).qb64

    return d


def main():
    parser = argparse.ArgumentParser(description="SAIDidy VRD Schema")
    args = parser.parse_args()

    path = Path(__file__).parent.parent.parent

    for p in [f"{path}/discovery-schema.json"]:
        s = __load(p)
        s["properties"]["e"]["oneOf"][1]["properties"]["le"]["properties"]["s"][
            "const"
        ] = args.le
        s = populate_saids(s)
        __save(p, s)


def __load(p):
    ff = open(p, "r")
    jsn = json.load(ff)
    ff.close()
    return jsn


def __save(p, d):
    schemer = scheming.Schemer(sed=d)
    f = open(schemer.said, "wb")
    f.write(schemer.raw)
    f.close()

    s = open(p, "w")
    s.write(json.dumps(schemer.sed, indent=2))

    # for github pages
    p = "publish"
    os.makedirs(os.path.join(p, schemer.said), exist_ok=True)
    f = open(os.path.join(p, schemer.said, "index.json"), "wb")
    f.write(schemer.raw)
    f.close()


if __name__ == "__main__":
    main()