# import glob
#
# import pandas as pd
# from keras.models import load_model
# from bioservices import UniProt
# import pandas as pd
# import types
# import io
# import sys
# from ipywidgets import FloatProgress, HTML, HBox
# from IPython.display import display

multiv = [
    'Interacts with',
    'Gene ontology (biological process)',
    'Gene ontology (cellular component)',
    'Gene ontology (GO)',
    'Gene ontology (molecular function)',
    'Gene ontology IDs',
]

stupid_list = [
    'Mass',
    'Non-adjacent residues',
    'Non-standard residue',
    'Non-terminal residue',
    'Absorption',
    'Temperature dependence',
    'Signal peptide',
    'Transit peptide',
    'Entry name',
]

stuff_list = [
    'Domain [FT]',
    'Protein families',
    'Sequence similarities',
    'Length',
    'Chain_structure',
    'Chain_Nr',
]

cols = ['Domain [FT]', 'Protein families', 'Sequence similarities', 'Chain_Nr']

stupid_list2 = [
    'Length',
    'Chain_Nr',
    'Protein families',
    'Domain [FT]',
    'Sequence similarities',
    'Chain_structure',
]


def take_dataframe(path):
    df = pd.read_excel(path, sheet_name=0)
    return df


def take_dataframe_blogas(path):
    df = pd.read_csv(path, sep='\t', index_col='Entry')
    return df


# def preprocess(df):
#     # Sutvarkoma chain dalis
#     df['Chain_Nr'] = df['Chain'].str.split(' ').str[1]
#     df['Chain_structure'] = df['Chain'].str.split(' ', 2).str[2]
#     df['Chain_structure'] = (
#         df['Chain_structure']
#         .str.split(' ', 1)
#         .str[1]
#         .str.split('. /', 1)
#         .str[0]
#     )
#
#     df = df.drop('Chain', axis=1)
#
#     # Sutvarkoma Sequence similarities dalis
#     df['Sequence similarities'] = (
#         df['Sequence similarities']
#         .str.split('to the ', 1)
#         .str[1]
#         .str.split('family.', 1)
#         .str[0]
#     )
#
#     # Sutvarkoma Domain [FT] dalis
#     df['Domain [FT]'] = (
#         df['Domain [FT]'].str.split(' ', 3).str[3].str.split('.', 1).str[0]
#     )
#
#     # Sutvarkoma Protein families dalis
#     df['Protein families'] = (
#         df['Protein families'].str.split('family', 1).str[1]
#     )
#
#     #     # Sutvarkoma chain dalis
#     #     dvb, data['Chain_Nr'], data['Chain_structure'] = (
#     #         data['Chain'].str.split(' ', 2).str
#     #     )
#     #     data['Chain_structure_bl'], data['Chain_structure1'] = (
#     #         data['Chain_structure'].str.split(' ', 1).str
#     #     )
#     #     data['Chain_structure'], data['Chain_structure_bl'] = (
#     #         data['Chain_structure1'].str.split('. /', 1).str
#     #     )
#
#     #     # Sutvarkoma Sequence similarities dalis
#     #     data['1'], data['2'] = (
#     #         data['Sequence similarities'].str.split('to the ', 1).str
#     #     )
#     #     data['Sequence similarities'], data['2'] = (
#     #         data['2'].str.split('family.', 1).str
#     #     )
#
#     #     # Sutvarkoma Domain [FT] dalis
#     #     data['1'], data['2'], data['3'], data['Domain [FT]'] = (
#     #         data['Domain [FT]'].str.split(' ', 3).str
#     #     )
#     #     data['Domain [FT]'], data['4'] = data['Domain [FT]'].str.split('.', 1).str
#
#     #     # Sutvarkoma Protein families dalis
#     #     data['Protein families'], data['2'] = (
#     #         data['Protein families'].str.split('family', 1).str
#     #     )
#
#     # Numetami nereikalingi stulpeliai
#     # bl = [
#     #     'Chain_structure_bl',
#     #     'Chain_structure1',
#     #     '1',
#     #     '2',
#     #     '3',
#     #     '4',
#     #     'Chain',
#     # ]
#     # data = data.drop(bl, axis=1)
#
# # Visi stulpeliai išskyrus stuff list yra užkoduojami True/False
#     df[df.columns.difference(stuff_list)] = df[
#         df.columns.difference(stuff_list)
#     ].notnull()
#
#
#     df = df.drop(multiv, axis=1)
#     df = df.drop(stupid_list, axis=1)
#     # ?????
#     # df = df.drop(stupid_list2, axis=1)
#
#     return df

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
    df['Chain_Nr'] = df['Chain'].str.split(' ').str[1]
    df['Chain_structure'] = df['Chain'].str.split(' ', 2).str[2]
    df['Chain_structure'] = (
        df['Chain_structure']
        .str.split(' ', 1)
        .str[1]
        .str.split('. /', 1)
        .str[0]
    )

    df = df.drop('Chain', axis=1)

        # Sutvarkoma Sequence similarities dalis
    df['Sequence similarities'] = (
        df['Sequence similarities']
        .str.split('to the ', 1)
        .str[1]
        .str.split('family.', 1)
        .str[0]
    )

        # Sutvarkoma Domain [FT] dalis
    df['Domain [FT]'] = (
        df['Domain [FT]'].str.split(' ', 3).str[3].str.split('.', 1).str[0]
    )

        # Sutvarkoma Protein families dalis
    df['Protein families'] = (
        df['Protein families'].str.split('family', 1).str[1]
    )

    return df

def code_non_strings(df):
    # Visi stulpeliai išskyrus stuff list yra užkoduojami True/False
    df[df.columns.difference(stuff_list)] = df[
        df.columns.difference(stuff_list)
    ].notnull()
    return df

# dar sutvarkyti
# def parse_uniprot(df):
#
#     entries = df.Accession.values.tolist()
#     u = UniProt(verbose=True)
#     data = pd.DataFrame()
#
#     _valid_columns = [
#         # Names & Taxonomy
#         'entry name',
#         # Sequences
#         'length',
#         'mass',
#         'comment(MASS SPECTROMETRY)',
#         'comment(POLYMORPHISM)',
#         'feature(NON ADJACENT RESIDUES)',
#         'feature(NON STANDARD RESIDUE)',
#         'feature(NON TERMINAL RESIDUE)',
#         # Family and Domains
#         'domains',
#         'domain',
#         'comment(DOMAIN)',
#         'feature(COMPOSITIONAL BIAS)',
#         'feature(DOMAIN EXTENT)',
#         'feature(ZINC FINGER)',
#         # Function
#         'comment(ABSORPTION)',
#         'comment(CATALYTIC ACTIVITY)',
#         'comment(COFACTOR)',
#         'comment(ENZYME REGULATION)',
#         'comment(FUNCTION)',
#         'comment(KINETICS)',
#         'comment(PATHWAY)',
#         'comment(REDOX POTENTIAL)',
#         'comment(TEMPERATURE DEPENDENCE)',
#         'comment(PH DEPENDENCE)',
#         'feature(ACTIVE SITE)',
#         'feature(BINDING SITE)',
#         'feature(DNA BINDING)',
#         'feature(METAL BINDING)',
#         'feature(NP BIND)',
#         'feature(SITE)',
#         # Gene Ontologys
#         'go',
#         'go(biological process)',
#         'go(molecular function)',
#         'go(cellular component)',
#         'go-id',
#         # Interaction
#         'interactor',
#         # Subcellular location
#         'feature(SUBCELLULAR LOCATION)',
#         'feature(INTRAMEMBRANE)',
#         'feature(TOPOLOGICAL DOMAIN)',
#         'feature(TRANSMEMBRANE)',
#         # Miscellaneous
#         'annotation score',
#         'score',
#         'features',
#         'comment(CAUTION)',
#         'comment(TISSUE SPECIFICITY)',
#         'comment(GENERAL)',
#         'keywords',
#         'context',
#         'existence',
#         'tools',
#         'reviewed',
#         'feature',
#         'families',
#         'subcellular locations',
#         'taxonomy',
#         'version',
#         'clusters',
#         'comments',
#         'database',
#         'keyword-id',
#         'pathway',
#         'score',
#         # Pathology & Biotech
#         'comment(ALLERGEN)',
#         'comment(BIOTECHNOLOGY)',
#         'comment(DISRUPTION PHENOTYPE)',
#         'comment(DISEASE)',
#         'comment(PHARMACEUTICAL)',
#         'comment(TOXIC DOSE)',
#         # PTM / Processsing
#         'comment(PTM)',
#         'feature(CHAIN)',
#         'feature(CROSS LINK)',
#         'feature(DISULFIDE BOND)',
#         'feature(GLYCOSYLATION)',
#         'feature(INITIATOR METHIONINE)',
#         'feature(LIPIDATION)',
#         'feature(MODIFIED RESIDUE)',
#         'feature(PEPTIDE)',
#         'feature(PROPEPTIDE)',
#         'feature(SIGNAL)',
#         'feature(TRANSIT)',
#     ]
#
#     for entry in entries:
#         try:
#             ent = 'id:' + entry
#             z = u.search(ent, frmt="tab", columns=",".join(_valid_columns))
#             df = pd.read_csv(io.StringIO(str(z)), sep="\t")
#             data = pd.concat([data, df], sort=False)
#         except:
#             print(entry)
#
#     #         remove duplicate shit
#     print(data.shape)
#     return data
#
#
# def bar(sequence):
#     from ipywidgets import FloatProgress, HTML, HBox
#     from IPython.display import display
#
#     size = len(sequence)
#     progress = FloatProgress(
#         min=0, max=size, value=0, description='?? / {}'.format(size)
#     )
#     label = HTML()
#     box = HBox(children=[progress, label])
#     display(box)
#
#     try:
#         for index, record in enumerate(sequence, 1):
#             progress.description = '{0} / {1}'.format(index, size)
#             progress.value = index
#             label.value = '{:6.2f} %'.format(100.0 * index / size)
#             yield record
#     except:
#         progress.bar_style = 'danger'
#         label.value = '<b>Error</b>'
#         raise
#
#     if size != 0 & size != None:
#         if index == size:
#             progress.bar_style = 'success'
#             progress.value = index
#             label.value = '<b>Done</b>'
#     else:
#         progress.max = 1
#         progress.value = 1
#         progress.bar_style = 'warning'
