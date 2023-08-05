# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/aggregates_from_pote.ipynb (unless otherwise specified).

__all__ = [
    "config",
    "tc",
    "extraction_date",
    "pote_extractions_folder",
    "of_vars",
    "df_dgfip",
    "pote_var_to_dict",
    "metadata",
    "ref_pote_2018",
    "ref_pote_2019",
    "labels",
    "perimeter",
    "year",
    "liste_des_variables_csg_2018",
    "liste_des_variables_csg_2019",
    "liste_des_variables_revenus_2019",
    "pote",
    "aggregates_from_csv",
    "agm",
]

# Cell


import time
import unittest

# import numpy as np
import pandas as pd
from leximpact_socio_fisca_simu_etat.config import Configuration

from .aggregate import (
    AggregateManager,
    DataStructure,
    Perimeter,
    Reference,
    openfisca_variables,
)

# from typing import List, Union


# from leximpact_socio_fisca_simu_etat.logger import logger
# from ruamel.yaml import YAML
# from tqdm import tqdm


config = Configuration(project_folder="leximpact-aggregates")
tc = unittest.TestCase()


# yaml = YAML()  # typ='unsafe' for testing

extraction_date = time.strftime("%Y-%m-%d")

# Cell
pote_extractions_folder = config.get("DATASETS") + "20220427-ExtractionAll/data/"

# Cell
of_vars = openfisca_variables

# Cell

df_dgfip = pd.read_excel("Colonnes_POTE_2019.xlsx", skiprows=1)
df_dgfip["Variable"] = df_dgfip["Variable"].str.lower()
df_dgfip["Libellé"] = df_dgfip["Libellé"].str.lower()
df_dgfip.query("Variable == 'revkire'")

# Cell

metadata = {}


def pote_var_to_dict(row):
    """On contruit un dictionnaire `metadata` à partir du fichier de
    description de POTE Si la variable existe dans le dictionnaire d'OpenFisca
    (OF), on utilise le libelllé OF."""
    pote_var = row["Variable"].lower()
    if of_vars.get(pote_var):
        # The name from pote exist in OpenFisca
        metadata[pote_var] = {
            "openfisca_variable": pote_var,
            "ux_name": of_vars[pote_var]["label"],
            "description": of_vars[pote_var]["label"],
        }
    elif of_vars.get("f" + pote_var[1:]):
        # The name exist in OFF with a f instead of a z as first letter
        metadata[pote_var] = {
            "openfisca_variable": "f" + pote_var[1:],
        }
        if of_vars["f" + pote_var[1:]].get("label"):
            metadata[pote_var]["ux_name"] = of_vars["f" + pote_var[1:]]["label"]
            metadata[pote_var]["description"] = of_vars["f" + pote_var[1:]]["label"]
    else:
        # The name from pote don't exist in OpenFisca
        metadata[pote_var] = {
            "ux_name": row["Libellé"],
            "description": row["Libellé"],
        }
    return row


_ = df_dgfip.apply(pote_var_to_dict, axis=1)

# Cell

ref_pote_2018 = Reference(
    title="POTE 2018 (DGFIP)",
    href="https://www.casd.eu/source/declarations-dimpot-sur-le-revenu-des-foyers-fiscaux-formulaire-2042-et-annexes/",
)
ref_pote_2019 = Reference(
    title="POTE 2019 (DGFIP)",
    href="https://www.casd.eu/source/declarations-dimpot-sur-le-revenu-des-foyers-fiscaux-formulaire-2042-et-annexes/",
)
labels = {
    "V": "Veuf(ve)",
    "C": "Célibataire",
    "O": "Pacsé(e)s",
    "D": "Divorcé(e)/séparé(e)",
    "M": "Marié(e)s",
}
perimeter = Perimeter(entity="foyer", period="year", geographic="France entière")

# Cell

metadata["mat"] = {
    "ux_name": "Situation matrimoniale",
    "description": "Situation matrimoniale du foyer fiscal",
    "openfisca_variable": "statut_marital",
    "ux_template": "Parmi les foyers français {value} sont {label}.",
    "labels": labels,
}
metadata["n"] = {
    "ux_name": "NOMBRE D'ENFANTS MARIÉS RATTACHÉS".lower(),
    "description": "Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille",
    "short_name": "nb_enfants_maries",
    "openfisca_variable": "nbN",
    "ux_template": "Parmi les foyers français {value} ont fait le choix de rattacher {label} enfants mariés ou chargés de famille.",
}
metadata["nbefi"] = {
    "ux_name": "NB TOTAL ENFANT A CHARGE I".lower(),
    "description": "Nombre d'enfants à charge non mariés, qui ne sont pas en résidence alternée, de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge",
    "openfisca_variable": "nbF",
    "short_name": "nb_enfants_a_charge",
    "ux_template": "Parmi les foyers français {value} sont {label}.",
}
metadata["revkire"] = {
    "ux_name": "Revenu fiscal de référence",
    "description": "Revenu fiscal de référence",
    "openfisca_variable": "rfr",
}

year = "2019"

# Cell
pd.set_option("display.max_colwidth", 80)
pd.options.display.float_format = "{:,.7f}".format

liste_des_variables_csg_2018 = pd.read_csv(
    config.get("DATASETS") + "agregats_des_variables_csg-POTE_2018.csv"
)
liste_des_variables_csg_2019 = pd.read_csv(
    pote_extractions_folder + "/agregats_POTE_2019.csv"
)
liste_des_variables_revenus_2019 = pd.read_csv(
    pote_extractions_folder + "/agregats_POTE_revenus_rici_2019.csv"
)

pote = {
    "2019": [liste_des_variables_csg_2019, liste_des_variables_revenus_2019],
    "2018": [liste_des_variables_csg_2018],
}

# Cell
aggregates_from_csv = []
for year, dfs in pote.items():
    for df in dfs:
        if year == "2019":
            ref = ref_pote_2019
        elif year == "2018":
            ref = ref_pote_2018
        # df.columns
        df["name"] = df["name"].str.lower()
        _ = df.apply(
            AggregateManager.get_aggregats_from_row,
            args=[
                aggregates_from_csv,
                year,
                df.columns.to_list(),
                ref,
                metadata,
                perimeter,
            ],
            axis=1,
        )
aggregates_from_csv[19]

# Cell
agm = AggregateManager()
agm.load_aggregate("POTE", "rfr", "2019", str(DataStructure.COPULAS_100))
tc.assertEqual(agm.aggregate.openfisca_variable, "rfr")
tc.assertEqual(agm.aggregate.description, metadata["revkire"]["description"])
tc.assertEqual(
    agm.aggregate.data[-1].values[-1]["buckets"][-1]["mean_above_upper_bound"], 0
)
