import pickle

import numpy as np
import pandas as pd
import os

import xgboost
import bioservices
from bioservices import UniProt
# ========================================================

# =============================================================================
# Parse uniprot using Bioservises
# =============================================================================

_valid_columns = [
    # Names & Taxonomy
    "id",
    "entry name",
    "genes",
    "genes(PREFERRED)",
    "genes(ALTERNATIVE)",
    "genes(OLN)",
    "genes(ORF)",
    "organism",
    "organism-id",
    "protein names",
    "proteome",
    "lineage(ALL)",
    "lineage-id",
    "virus hosts",
    # Sequences
    "fragement",
    "sequence",
    "length",
    "mass",
    "encodedon",
    "comment(ALTERNATIVE PRODUCTS)",
    "comment(ERRONEOUS GENE MODEL PREDICTION)",
    "comment(ERRONEOUS INITIATION)",
    "comment(ERRONEOUS TERMINATION)",
    "comment(ERRONEOUS TRANSLATION)",
    "comment(FRAMESHIFT)",
    "comment(MASS SPECTROMETRY)",
    "comment(POLYMORPHISM)",
    "comment(RNA EDITING)",
    "comment(SEQUENCE CAUTION)",
    "feature(ALTERNATIVE SEQUENCE)",
    "feature(NATURAL VARIANT)",
    "feature(NON ADJACENT RESIDUES)",
    "feature(NON STANDARD RESIDUE)",
    "feature(NON TERMINAL RESIDUE)",
    "feature(SEQUENCE CONFLICT)",
    "feature(SEQUENCE UNCERTAINTY)",
    "version(sequence)",
    # Family and Domains
    "domains",
    "domain",
    "comment(DOMAIN)",
    "comment(SIMILARITY)",
    "feature(COILED COIL)",
    "feature(COMPOSITIONAL BIAS)",
    "feature(DOMAIN EXTENT)",
    "feature(MOTIF)",
    "feature(REGION)",
    "feature(REPEAT)",
    "feature(ZINC FINGER)",
    # Function
    "ec",
    "comment(ABSORPTION)",
    "comment(CATALYTIC ACTIVITY)",
    "comment(COFACTOR)",
    "comment(ENZYME REGULATION)",
    "comment(FUNCTION)",
    "comment(KINETICS)",
    "comment(PATHWAY)",
    "comment(REDOX POTENTIAL)",
    "comment(TEMPERATURE DEPENDENCE)",
    "comment(PH DEPENDENCE)",
    "feature(ACTIVE SITE)",
    "feature(BINDING SITE)",
    "feature(DNA BINDING)",
    "feature(METAL BINDING)",
    "feature(NP BIND)",
    "feature(SITE)",
    # Gene Ontologys
    "go",
    "go(biological process)",
    "go(molecular function)",
    "go(cellular component)",
    "go-id",
    # InterPro
    "interpro",
    # Interaction
    "interactor",
    "comment(SUBUNIT)",
    # Publications
    "citation",
    "citationmapping",
    # Date of
    "created",
    "last-modified",
    "sequence-modified",
    "version(entry)",
    # Structure
    "3d",
    "feature(BETA STRAND)",
    "feature(HELIX)",
    "feature(TURN)",
    # Subcellular location
    "feature(SUBCELLULAR LOCATION)",
    "feature(INTRAMEMBRANE)",
    "feature(TOPOLOGICAL DOMAIN)",
    "feature(TRANSMEMBRANE)",
    # Miscellaneous
    "annotation score",
    "score",
    "features",
    "comment(CAUTION)",
    "comment(TISSUE SPECIFICITY)",
    "comment(GENERAL)",
    "keywords",
    "context",
    "existence",
    "tools",
    "reviewed",
    "feature",
    "families",
    "subcellular locations",
    "taxonomy",
    "version",
    "clusters",
    "comments",
    "database",
    "keyword-id",
    "pathway",
    "score",
    # Pathology & Biotech
    "comment(ALLERGEN)",
    "comment(BIOTECHNOLOGY)",
    "comment(DISRUPTION PHENOTYPE)",
    "comment(DISEASE)",
    "comment(PHARMACEUTICAL)",
    "comment(TOXIC DOSE)",
    # PTM / Processsing
    "comment(PTM)",
    "feature(CHAIN)",
    "feature(CROSS LINK)",
    "feature(DISULFIDE BOND)",
    "feature(GLYCOSYLATION)",
    "feature(INITIATOR METHIONINE)",
    "feature(LIPIDATION)",
    "feature(MODIFIED RESIDUE)",
    "feature(PEPTIDE)",
    "feature(PROPEPTIDE)",
    "feature(SIGNAL)",
    "feature(TRANSIT)",
    # Taxonomic lineage
    "lineage(all)",
    "lineage(SUPERKINGDOM)",
    "lineage(KINGDOM)",
    "lineage(SUBKINGDOM)",
    "lineage(SUPERPHYLUM)",
    "lineage(PHYLUM)",
    "lineage(SUBPHYLUM)",
    "lineage(SUPERCLASS)",
    "lineage(CLASS)",
    "lineage(SUBCLASS)",
    "lineage(INFRACLASS)",
    "lineage(SUPERORDER)",
    "lineage(ORDER)",
    "lineage(SUBORDER)",
    "lineage(INFRAORDER)",
    "lineage(PARVORDER)",
    "lineage(SUPERFAMILY)",
    "lineage(FAMILY)",
    "lineage(SUBFAMILY)",
    "lineage(TRIBE)",
    "lineage(SUBTRIBE)",
    "lineage(GENUS)",
    "lineage(SUBGENUS)",
    "lineage(SPECIES GROUP)",
    "lineage(SPECIES SUBGROUP)",
    "lineage(SPECIES)",
    "lineage(SUBSPECIES)",
    "lineage(VARIETAS)",
    "lineage(FORMA)",
    # Taxonomic identifier
    "lineage-id(all)",
    "lineage-id(SUPERKINGDOM)",
    "lineage-id(KINGDOM)",
    "lineage-id(SUBKINGDOM)",
    "lineage-id(SUPERPHYLUM)",
    "lineage-id(PHYLUM)",
    "lineage-id(SUBPHYLUM)",
    "lineage-id(SUPERCLASS)",
    "lineage-id(CLASS)",
    "lineage-id(SUBCLASS)",
    "lineage-id(INFRACLASS)",
    "lineage-id(SUPERORDER)",
    "lineage-id(ORDER)",
    "lineage-id(SUBORDER)",
    "lineage-id(INFRAORDER)",
    "lineage-id(PARVORDER)",
    "lineage-id(SUPERFAMILY)",
    "lineage-id(FAMILY)",
    "lineage-id(SUBFAMILY)",
    "lineage-id(TRIBE)",
    "lineage-id(SUBTRIBE)",
    "lineage-id(GENUS)",
    "lineage-id(SUBGENUS)",
    "lineage-id(SPECIES GROUP)",
    "lineage-id(SPECIES SUBGROUP)",
    "lineage-id(SPECIES)",
    "lineage-id(SUBSPECIES)",
    "lineage-id(VARIETAS)",
    "lineage-id(FORMA)",
    # Cross-references
    "database(db_abbrev)",
    "database(EMBL)",
]

# Not needed?
# def parse_uniprot(entries):
#
#     u = UniProt(verbose=True)
#     data = pd.DataFrame()
#
#     for entry in entries:
#         clear_output(wait=True)
#         try:
#             ent = "id:" + entry
#             z = u.search(
#                 ent, frmt="tab", columns=",".join(_valid_columns), limit=1, maxTrials=3
#             )
#             df = pd.read_csv(io.StringIO(str(z)), sep="\t")
#             data = pd.concat([data, df], sort=False)
#         except:
#             print(entry)
#         print("Progress:", np.round(entries.index(entry) / len(entries) * 100, 2), "%")
#     return data

def parse_uniprot(entries):
    ent = ['id:' + s for s in entries]
    print(ent[2])
    u = UniProt(verbose=True)
    df = u.get_df(ent)

    return df

# =============================================================================
# Data preprocessing
# =============================================================================

multiv = [
    "Interacts with",
    "Gene ontology (biological process)",
    "Gene ontology (cellular component)",
    "Gene ontology (GO)",
    "Gene ontology (molecular function)",
    "Gene ontology IDs",
]

stupid_list = [
    "Mass",
    "Non-adjacent residues",
    "Non-standard residue",
    "Non-terminal residue",
    "Absorption",
    "Temperature dependence",
    "Signal peptide",
    "Transit peptide",
    "Entry name",
]

stuff_list = [
    "Domain [FT]",
    "Protein families",
    "Sequence similarities",
    "Length",
    "Chain_structure",
    "Chain_Nr",
]

cols = ["Domain [FT]", "Protein families", "Sequence similarities", "Chain_Nr"]

stupid_list2 = [
    "Length",
    "Chain_Nr",
    "Protein families",
    "Domain [FT]",
    "Sequence similarities",
    "Chain_structure",
]

def drop_cols(df):
    df = df.drop(multiv, axis=1)
    df = df.drop(stupid_list, axis=1)
    # ?????
    # df = df.drop(stupid_list2, axis=1)
    return df


def preprocess_strings(df=None, path=None):
    #  Path thingy not working
    # if path is not None:
    #     try:
    #         df = pd.read_csv(path, sep='\t', index_col=0)
    #     except:
    #         print('Error train never stops!!! - bad path')
    # elif df is None:
    #     print('Cookie monster wants arguments')
    # else:
    # Sutvarkoma chain dalis
    df["Chain_Nr"] = df["Chain"].str.split(" ").str[1]
    df["Chain_structure"] = df["Chain"].str.split(" ", 2).str[2]
    df["Chain_structure"] = (
        df["Chain_structure"].str.split(" ", 1).str[1].str.split(". /", 1).str[0]
    )

    df = df.drop("Chain", axis=1)

    # Sutvarkoma Sequence similarities dalis
    df["Sequence similarities"] = (
        df["Sequence similarities"]
        .str.split("to the ", 1)
        .str[1]
        .str.split("family.", 1)
        .str[0]
    )

    # Sutvarkoma Domain [FT] dalis
    df["Domain [FT]"] = (
        df["Domain [FT]"].str.split(" ", 3).str[3].str.split(".", 1).str[0]
    )

    # Sutvarkoma Protein families dalis
    df["Protein families"] = df["Protein families"].str.split("family", 1).str[1]

    return df


def code_non_strings(df):
    # Visi stulpeliai isskyrus stuff list yra uzkoduojami True/False
    df[df.columns.difference(stuff_list)] = df[
        df.columns.difference(stuff_list)
    ].notnull()
    return df


# =============================================================================


# MB_dataset

try:
    if os.path.isfile("mb_data.csv"): # for when internets are down
        mb_data = pd.read_csv("mb_data.csv")
        mb_data1 = mb_data.copy()
    else:
        path_predict = "sil_proteom.xlsx"
        print('weee')
        df = pd.read_excel(path_predict, sheet_name=0)
        entries = df.Accession.values.tolist()
        mb_data_temp = parse_uniprot(entries)
        mb_data_temp.to_csv("mb_data.csv")
        print(mb_data_temp.head())
        mb_data = pd.read_csv("mb_data.csv") #Shitty workaround for string problem
        mb_data1 = mb_data.copy()
except:
    print('Stuff is not working. Sorry :( ')

# Viską į vieną funkciją preprocess?
mb_data = preprocess_strings(mb_data)
mb_data = drop_cols(mb_data)
mb_data = code_non_strings(mb_data)

df = mb_data[mb_data.T[mb_data.dtypes != np.object].index]

loaded_model = pickle.load(open("model", "rb"))
X = df.values
z = mb_data1.Entry.tolist()
zz = mb_data1["Gene names"].tolist()
y_pred = loaded_model.predict(X)



df = pd.DataFrame({"Entry": z, "Gene name": zz, "MB": y_pred})


df.to_excel("possible_MB.xlsx")
