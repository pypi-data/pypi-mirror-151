"""
This module work for parse NCBI taxonomy database.

wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

usage:
#
from taxonomy_lineage import Taxon,build_taxon_database
tax_record_dict = build_taxon_database(names_dmp_file,nodes_dmp_file)
#
class:
    Taxon
function:
    build_taxon_database
parsed output in main:
    a tsv file with two column: tax_id,lineage_list
log:
    Yuxing Xu
    2018.01.17  rewrite module from old script by Yuxing Xu
"""

__author__ = 'Yuxing Xu'




if __name__ == '__main__':
    import argparse

    ###### argument parse
    parser = argparse.ArgumentParser(
        prog='TaxonTools',
    )

    subparsers = parser.add_subparsers(title='subcommands', dest="subcommand_name")

    # argparse for StoreTaxonDB
    parser_a = subparsers.add_parser('StoreTaxonDB',
                                     help='store a taxon database into a sqlite3', description='')
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("tax_db_file", help="Path for sqlite3 file", type=str)

    # argparse for ID2Lineage
    parser_a = subparsers.add_parser('ID2Lineage',
                                     help='get taxonomy lineage by taxon ID', description='')
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("-q", "--query_tax_id_file", help="The file containing the tax_id to query (default as all taxon\
                         in database)", default=None, type=str)
    parser_a.add_argument("-o", "--output_file", help="Output file name (default as $STDOUT)", default=None, type=str)

    # argparse for Name2Lineage
    parser_a = subparsers.add_parser('Name2Lineage',
                                     help='get taxonomy lineage by taxon science name', description='')

    parser_a.add_argument("query_file", help="The file containing the tax name to query", type=str)
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("-o", "--output_file", help="Output file name (default as $STDOUT)", default=None, type=str)
    parser_a.add_argument("-f", "--fuzzy_search", help="use fuzzy search for more time", action='store_true')

    # argparse for RankStat
    parser_a = subparsers.add_parser('RankStat',
                                     help='to stat a rank taxonomy under given taxonmoy, such as return all order under fungi')

    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("top_taxonomy_id", help="the top taxonomy want to search (taxon_id: 4751 for fungi)",
                          type=str)
    parser_a.add_argument("search_rank", help="rank want to search such as order", type=str)
    parser_a.add_argument("-o", "--output_file", help="Output file name (default as $STDOUT)", default=None, type=str)

    # argparse for CommonTree
    parser_a = subparsers.add_parser('CommonTree',
                                     help='get common tree by leaf taxon ID', description='')
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("tax_id_list", help="The file containing the tax_id to query", type=str)
    parser_a.add_argument("-o", "--output_file", help="Output file name (default as $STDOUT)", default=None, type=str)
    parser_a.add_argument("-id", "--ID_flag", help="output tree will writen by taxon id", action='store_true')
    parser_a.add_argument("-p", "--no_pass_node", help="remove pass node", action='store_true')

    # argparse for DiamondTaxonAssign
    parser_a = subparsers.add_parser('DiamondTaxonAssign',
                                     help='parse blast results to get protein seq taxon', description='')
    parser_a.add_argument("blast_results",
                          help="blast results need diamond output: qseqid sseqid staxids pident length mismatch gapopen qstart qend sstart send evalue bitscore",
                          type=str)
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("-n", "--num_threads", help="cpu number (default as 10)", default=10, type=int)
    parser_a.add_argument("-o", "--output_file", help="Output file name (default as taxon.assign.txt)",
                          default="taxon.assign.txt", type=str)

    # argparse for ExcludeTaxon
    parser_a = subparsers.add_parser('ExcludeTaxon',
                                     help='Exclude a taxon id, to get all taxon_id not include given taxon id',
                                     description='')
    parser_a.add_argument("taxon_id", help="taxon id which want to be excluded", type=str)
    parser_a.add_argument("tax_dir", help="Path for uncompressed taxdump.tar.gz", type=str)
    parser_a.add_argument("-r", "--root_taxon_id", help="root for excluded (default as root for all database)",
                          default='1', type=str)

    args = parser.parse_args()
    args_dict = vars(args)

    # --------------------------------------------
    #### command detail

    if args_dict["subcommand_name"] == "ID2Lineage":
        from lib.xuyuxing.evolution.taxonomy import build_taxon_database
        from lib.common.fileIO import read_list_file

        taxonomy_dir = args.tax_dir
        query_file = args.query_tax_id_file
        output_file = args.output_file

        # output as a tsv file

        tax_record_dict = build_taxon_database(taxonomy_dir)

        query_tax_id = read_list_file(query_file)
        if query_file is not None:
            query_tax_id = read_list_file(query_file)
        else:
            query_tax_id = tax_record_dict.keys()

        if output_file is not None:
            with open(output_file, 'w') as f:
                for tax_id in query_tax_id:
                    if tax_id in tax_record_dict:
                        taxon = tax_record_dict[tax_id]
                        lineage_str = ""
                        lineage_list = taxon.get_lineage(tax_record_dict)
                        for i in lineage_list:
                            tax_id_tmp, rank_tmp = i
                            lineage_str = lineage_str + tax_record_dict[tax_id_tmp].sci_name + " (" + rank_tmp + ");"
                        lineage_str = lineage_str.rstrip(";")
                        f.write(tax_id + "\t" + lineage_str + "\n")
                    else:
                        lineage_str = "error"
                        f.write(tax_id + "\t" + lineage_str + "\n")
        else:
            for tax_id in query_tax_id:
                taxon = tax_record_dict[tax_id]
                lineage_str = ""
                lineage_list = taxon.get_lineage(tax_record_dict)
                for i in lineage_list:
                    tax_id_tmp, rank_tmp = i
                    lineage_str = lineage_str + tax_record_dict[tax_id_tmp].sci_name + " (" + rank_tmp + ");"
                lineage_str = lineage_str.rstrip(";")
                print(tax_id + "\t" + lineage_str)

    elif args_dict["subcommand_name"] == "StoreTaxonDB":
        from lib.xuyuxing.evolution.taxonomy import build_taxon_database, store_tax_record_into_sqlite
        tax_record_dict = build_taxon_database(args.tax_dir)
        store_tax_record_into_sqlite(tax_record_dict, args.tax_db_file)


    # elif args_dict["subcommand_name"] == "CommonTree":
    #     from lib.evolution.taxonomy import build_taxon_database
    #     from lib.common.fileIO import read_list_file
    #     import ete3


    #     def get_common_tree(lineages, ID_flag):
    #         if ID_flag:
    #             tree = ete3.Tree(name='1')
    #         else:
    #             tree = ete3.Tree(name='root')

    #         for line_tmp in lineages:
    #             node_tmp = tree
    #             for i in line_tmp:
    #                 if ID_flag:
    #                     i = i[0]
    #                 else:
    #                     i = i[1]

    #                 if node_tmp.name == i:
    #                     continue
    #                 else:
    #                     child_flag = len([j for j in node_tmp.children if j.name == i])
    #                     if child_flag:
    #                         node_tmp = [j for j in node_tmp.children if j.name == i][0]
    #                     else:
    #                         node_tmp.add_child(name=i)
    #                         node_tmp = [j for j in node_tmp.children if j.name == i][0]
    #         return tree


    #     taxonomy_dir = args.tax_dir
    #     query_file = args.tax_id_list
    #     output_file = args.output_file
    #     id_flag = args.ID_flag

    #     query_list = read_list_file(query_file)
    #     tax_record_dict = build_taxon_database(taxonomy_dir)

    #     all_lineage = []
    #     for tax_id in query_list:
    #         taxon = tax_record_dict[tax_id]
    #         lineage_list = taxon.get_lineage(tax_record_dict)
    #         lineage_list_add = []
    #         for i in lineage_list:
    #             tax_id_tmp, rank_tmp = i
    #             lineage_list_add.append((tax_id_tmp, tax_record_dict[tax_id_tmp].sci_name, rank_tmp))
    #         all_lineage.append(lineage_list_add)

    #     tree = get_common_tree(all_lineage, id_flag)

    #     if output_file is None:
    #         print(tree)
    #     else:
    #         tree.write(format=1, outfile=output_file)


    elif args_dict["subcommand_name"] == "CommonTree":
        from lib.xuyuxing.evolution.taxonomy import build_taxon_database
        from lib.common.fileIO import read_list_file
        from lib.common.evolution.tree_operate import Tree, Clade, Phylo, draw_ascii, remove_pass_node

        def get_common_tree(lineages, ID_flag):
            if ID_flag:
                root_clade = Clade(name='1')
            else:
                root_clade = Clade(name='root')

            for line_tmp in lineages:
                node_tmp = root_clade
                for i in line_tmp:
                    if ID_flag:
                        i = i[0]
                    else:
                        i = i[1]

                    if node_tmp.name == i:
                        continue
                    else:
                        child_flag = len([j for j in node_tmp.clades if j.name == i])
                        if child_flag:
                            node_tmp = [j for j in node_tmp.clades if j.name == i][0]
                        else:
                            node_tmp.clades.append(Clade(name=i, branch_length=1.0))
                            node_tmp = [j for j in node_tmp.clades if j.name == i][0]

            tree = Tree(root_clade, True)
            return tree

        taxonomy_dir = args.tax_dir
        query_file = args.tax_id_list
        output_file = args.output_file
        id_flag = args.ID_flag
        no_pass_node = args.no_pass_node

        query_list = read_list_file(query_file)
        tax_record_dict = build_taxon_database(taxonomy_dir)

        all_lineage = []
        for tax_id in query_list:
            taxon = tax_record_dict[tax_id]
            lineage_list = taxon.get_lineage(tax_record_dict)
            lineage_list_add = []
            for i in lineage_list:
                tax_id_tmp, rank_tmp = i
                lineage_list_add.append((tax_id_tmp, tax_record_dict[tax_id_tmp].sci_name, rank_tmp))
            all_lineage.append(lineage_list_add)

        tree = get_common_tree(all_lineage, id_flag)

        if no_pass_node:
            tree = remove_pass_node(tree)

        if output_file is None:
            draw_ascii(tree)
        else:
            with open(output_file, 'w') as f:
                Phylo.write(tree, f, 'newick')


    elif args_dict["subcommand_name"] == "Name2Lineage":
        from lib.xuyuxing.evolution.taxonomy import build_taxon_database
        from lib.common.fileIO import read_list_file
        from fuzzywuzzy import process
        import sys


        taxonomy_dir = args.tax_dir
        query_file = args.query_file
        output_file = args.output_file
        fuzzy_search = args.fuzzy_search

        # build database
        tax_record_dict = build_taxon_database(taxonomy_dir, True)

        # make hash table
        tax_record_sciname_hash = {}
        tax_record_othername_hash = {}
        for tax_id in tax_record_dict:
            tax_tmp = tax_record_dict[tax_id]

            if tax_tmp.sci_name not in tax_record_sciname_hash:
                tax_record_sciname_hash[tax_tmp.sci_name] = []
            tax_record_sciname_hash[tax_tmp.sci_name].append(tax_id)

            if hasattr(tax_tmp, 'other_name'):
                for name_tmp in tax_tmp.other_name:
                    if name_tmp not in tax_record_othername_hash:
                        tax_record_othername_hash[name_tmp] = []
                    tax_record_othername_hash[name_tmp].append(tax_id)

        # read query file
        query_tax_name = read_list_file(query_file)

        # search query in hash table
        subject_list = []
        sci_name_list = list(tax_record_sciname_hash.keys())
        other_name_list = list(tax_record_othername_hash.keys())
        for search_string in query_tax_name:
            other_name_flag = False
            fuzzy_flag = False
            homonym_flag = False
            # search sci_name
            if search_string in sci_name_list:
                search_out = tax_record_sciname_hash[search_string]
            # search other_name
            elif search_string in other_name_list:
                other_name_flag = True
                search_out = tax_record_othername_hash[search_string]
            # fuzzy search all name
            elif fuzzy_search:
                fuzzy_flag = True
                search_out = tax_record_sciname_hash[
                    process.extractOne(search_string, sci_name_list + other_name_list)[0]]
            else:
                search_out = []
            # remove older taxid
            search_out = list(set([tax_record_dict[i].tax_id for i in search_out]))

            # check if homonym
            if len(search_out) > 1:
                homonym_flag = True
                print(search_out)
            # add failed info for None
            if len(search_out) == 0:
                subject_list.append((search_string,))
            # add to subject_list
            for tax_id in search_out:
                tax_tmp = tax_record_dict[tax_id]
                subject_list.append((search_string, tax_tmp.tax_id, tax_tmp.sci_name,
                                     tax_tmp.get_lineage(tax_record_dict), other_name_flag, fuzzy_flag, homonym_flag))

        if output_file is None:
            file = sys.stdout
        else:
            file = open(output_file, 'w')

        file.write("query\ttax_id\tsci_name\tlineage\tother_name_flag\tfuzzy_flag\thomonym_flag\n")
        for i in subject_list:
            if len(i) == 1:
                file.write(i[0] + "\terror\n")
            else:
                lineage_str = ""
                lineage_list = i[3]
                for j in lineage_list:
                    tax_id_tmp, rank_tmp = j
                    lineage_str = lineage_str + tax_record_dict[tax_id_tmp].sci_name + " (" + rank_tmp + ");"
                lineage_str = lineage_str.rstrip(";")
                file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (i[0], i[1], i[2], lineage_str, i[4], i[5], i[6]))

    elif args_dict["subcommand_name"] == "RankStat":
        from lib.xuyuxing.evolution.taxonomy import build_taxon_database
        from lib.common.fileIO import read_list_file
        import sys


        # build database
        tax_record_dict = build_taxon_database(args.tax_dir, True)

        # get list
        want_id_list = []
        for tax_id in tax_record_dict:
            tax_tmp = tax_record_dict[tax_id]
            if tax_tmp.rank == args.search_rank and tax_tmp.is_child_of(args.top_taxonomy_id, tax_record_dict):
                want_id_list.append(tax_id)

        # output
        if not args.output_file is None:
            sys.stdout = open(args.output_file, 'w')

        print("tax_id\tsci_name\trank\tlineage")
        for tax_id in want_id_list:
            tax_tmp = tax_record_dict[tax_id]
            lineage_str = ""
            lineage_list = tax_tmp.get_lineage(tax_record_dict)
            for j in lineage_list:
                tax_id_tmp, rank_tmp = j
                lineage_str = lineage_str + tax_record_dict[tax_id_tmp].sci_name + " (" + rank_tmp + ");"
            lineage_str = lineage_str.rstrip(";")

            print("%s\t%s\t%s\t%s" % (tax_id, tax_tmp.sci_name, tax_tmp.rank, lineage_str))

    elif args_dict["subcommand_name"] == "ExcludeTaxon":
        """
        class abc():
            pass
        
        args = abc()
        args.tax_dir = '/lustre/home/xuyuxing/Database/genome2020/genome/info/NCBI/taxonomy'
        args.root_taxon_id = '73496'
        args.taxon_id = '40553'
        """

        from lib.xuyuxing.evolution.taxonomy import build_taxon_database
        from lib.common.fileIO import read_list_file

        import copy
        from lib.common.util import printer_list

        tax_record_dict = build_taxon_database(args.tax_dir)
        root_taxon = tax_record_dict[args.root_taxon_id]
        exc_taxon = tax_record_dict[args.taxon_id]

        # get_lineage
        root_lineage = root_taxon.get_lineage(tax_record_dict)
        exc_lineage = exc_taxon.get_lineage(tax_record_dict)

        # diff lineage
        diff_lineage = copy.deepcopy(exc_lineage)
        for i in root_lineage[:-1]:
            diff_lineage.remove(i)

        output_list = []
        for i in range(len(diff_lineage) - 1):
            tax_id, rank_note = diff_lineage[i]
            next_tax_id, rank_note = diff_lineage[i + 1]

            tax_tmp = tax_record_dict[tax_id]
            output_list.extend(list(set([j for j in tax_tmp.get_sons(tax_record_dict) if j != next_tax_id])))

        print(printer_list(output_list, ','))

    elif args_dict["subcommand_name"] == "DiamondTaxonAssign":
        """
        class abc():
            pass

        args = abc()
        args.blast_results = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev1.1/gene_taxon/Cuscuta.pt.v1.1.fasta.bls'
        args.tax_dir = '/lustre/home/xuyuxing/Database/NCBI/nr/2020/taxdmp'
        args.output_file = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev1.1/gene_taxon/Cuscuta.pt.v1.1.fasta.taxon'
        args.num_threads = 56
        """
        from src.xuyuxing.tools.taxontools import DiamondTaxonAssign_main
        DiamondTaxonAssign_main(args)
